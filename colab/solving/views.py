import sys
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.static import serve
from django.conf import settings

from .models import Exercice, Solution, Category
from .forms import PostSolutionForm, PostExerciceForm, EditSolutionForm, EditExerciceForm


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
    page = request.GET.get('page')
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    exercices = Category.objects.all()
    form = PostExerciceForm()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
        exercices = Exercice.objects.filter(category=instance).order_by('-pub_date')
        category_list = instance.children.all()
        paginator = Paginator(category_list, 3)
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            categories = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            print("Form is valid", file=sys.stderr)
            categories = paginator.page(paginator.num_pages)
    except:
        instance = get_object_or_404(Exercice, slug = category_slug[-1])
        return HttpResponseRedirect(reverse('solving:detail', args=(instance.id,)))
    else:
        return render(request, 'solving/categories.html', {'category': instance, 'exercices': exercices, 'form': form, 'categories': categories})

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
            solution.file = form.cleaned_data['file']
            solution.save()
        else:
            print("Form isn't valid", file=sys.stderr)
            return render(request, 'solving/errostormshit.html', {'form': form})

    return HttpResponseRedirect(reverse('solving:detail', args=(exercice_id,)))

@login_required
def editSolution(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)
    exercice = get_object_or_404(Exercice, pk=solution.exercice.id)
    if (solution.author != request.user):
         return HttpResponseForbidden()

    if request.method == "POST":
        form = EditSolutionForm(request.POST, instance=solution)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.author = request.user
            solution.save()
            return HttpResponseRedirect(reverse('solving:detail', args=(exercice.id,)))
        else:
            print("Form isn't valid", file=sys.stderr)
            return render(request, 'solving/errostormshit.html', {'form': form})
    else:
        form = EditSolutionForm(instance=solution)

    return render(request, 'solving/edit_solution.html', {'form': form, 'solution': solution})

@login_required
def deleteSolution(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)
    exercice_id = solution.exercice.id

    if (solution.author == request.user):
        solution.delete()

    return HttpResponseRedirect(reverse('solving:detail', args=(exercice_id,)))

@login_required
def postExercice(request, category_id):
    #TODO tester la securité de l'url et voir si la category peut host des exos
    category = get_object_or_404(Category, pk=category_id)

    if(category.contain_exercice()):
        if request.method == 'POST':
            form = PostExerciceForm(request.POST, request.FILES)

            if (form.is_valid()):
                exercice = form.save(commit=False)
                exercice.author = request.user
                exercice.category = category
                exercice.pub_date = timezone.now()
                exercice.file = form.cleaned_data['file']
                if exercice.category.have_exercice:
                    exercice.save()
            else:
                return render(request, 'solving/errostormshit.html', {'form': form})

    return redirect(request.META['HTTP_REFERER'])

@login_required
def editExercice(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)

    if (exercice.author != request.user):
        print("et oui", file=sys.stderr)
        return HttpResponseForbidden()

    if request.method == "POST":
        form = EditExerciceForm(request.POST, instance=exercice)
        if form.is_valid():
            exercice = form.save(commit=False)
            exercice.author = request.user
            exercice.save()
            return HttpResponseRedirect(reverse('solving:detail', args=(exercice.id,)))
        else:
            print("Form isn't valid", file=sys.stderr)
            return render(request, 'solving/errostormshit.html', {'form': form})
    else:
        form = EditExerciceForm(instance=exercice)

    return render(request, 'solving/edit_exercice.html', {'form': form, 'exercice': exercice})

@login_required
def deleteExercice(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    exercice_category_slug = exercice.category.slug
    if (exercice.author == request.user):
        exercice.delete()

    return HttpResponseRedirect(reverse('solving:category', args=(exercice_category_slug,)))

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)
