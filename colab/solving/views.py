import sys
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.files import File
from django.views.static import serve
from django.conf import settings

from .models import Exercice, Solution, Category
from .forms import PostSolutionForm


@login_required
def index(request):
    categories = Category.objects.filter(parent_id=None)
    latest_exercice_list = get_list_or_404(Exercice.objects.order_by('-pub_date')[:5])
    context = {
        'latest_exercice_list': latest_exercice_list,
        'categories': categories,
    }
    return render(request, 'solving/index.html', context)

@login_required
def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    form = PostSolutionForm()

    context = {
        'exercice': exercice,
        'solutions': Solution.objects.filter(exercice=exercice.id).select_related().order_by('-ratings__average'),
        'form': form,
    }

    return render(request, 'solving/detail.html', context)

@login_required
def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    exercices = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
        exercices = Exercice.objects.filter(category=instance).order_by('-pub_date')
    except:
        instance = get_object_or_404(Exercice, slug = category_slug[-1])
        return HttpResponseRedirect(reverse('solving:detail', args=(instance.id,)))
    else:
        return render(request, 'solving/categories.html', {'instance': instance, 'exercices': exercices})

@login_required
def postSolution(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)

    if request.method == 'POST':
        form = PostSolutionForm(request.POST, request.FILES)

        if form.is_valid():
            print("Form is valid", file=sys.stderr)
            #TODO Faire en sorte de verifier les donnéees avec clean_data
            solution = form.save(commit=False)
            solution.author = request.user
            solution.exercice = exercice
            solution.pub_date = timezone.now()
            solution.file = form.file
            solution.save()
        else:
            print("Form isn't valid", file=sys.stderr)
            return render(request, 'solving/errostormshit.html', {'form': form})

    return HttpResponseRedirect(reverse('solving:detail', args=(exercice_id,)))


@login_required
def deleteSolution(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)
    exercice_id = solution.exercice.id

    if (solution.author == request.user):
        solution.delete()

    return HttpResponseRedirect(reverse('solving:detail', args=(exercice_id,)))

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)
