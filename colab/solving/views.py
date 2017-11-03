from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Exercice, Solution
from .forms import PostSolutionForm
#for setting an access rules on a view u should use @login_required

@login_required
def index(request):
    latest_exercice_list = get_list_or_404(Exercice.objects.order_by('-pub_date')[:5])
    context = {'latest_exercice_list': latest_exercice_list}
    return render(request, 'solving/index.html', context)

@login_required
def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    form = PostSolutionForm()

    context = {
        'exercice': exercice,
        'solutions': Solution.objects.filter(exercice=exercice.id).select_related().order_by('ratings'),
        'form': form,
    }

    return render(request, 'solving/detail.html', context)

@login_required
def postSolution(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)

    if request.method == 'POST':
        form = PostSolutionForm(request.POST)

        if form.is_valid():
            solution = form.save(commit=False)
            solution.author = request.user
            solution.exercice = exercice
            solution.save()

    return HttpResponseRedirect(reverse('solving:detail', args=(exercice_id,)))
