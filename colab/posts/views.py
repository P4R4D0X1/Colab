from django.shortcuts import render

from .models import Category, Post

def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(Post, slug=category_slug[-1])
        return render(request, 'postDetail.html', {'instance':instance})
    else:
        return render(request, 'categories.html', {'instance':instance})
