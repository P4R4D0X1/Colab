from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
from star_ratings.models import Rating



class Exercice(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, editable=False, null=True)
    content = models.TextField('Content')
    category = TreeForeignKey('Category', null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=datetime.now())
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)
    file = models.FileField(upload_to="exercice_files/", null=True)

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Exercice.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save()

class Solution(models.Model):
    exercice = models.ForeignKey(Exercice, related_name='solutions', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, editable=False)
    pub_date = models.DateTimeField('date published', default=datetime.now())
    content = models.TextField('Content')
    ratings = GenericRelation(Rating, related_query_name='solutions')
    file = models.FileField(upload_to="solution_files/", null=True)

    def __str__(self):
        return self.title

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    have_exercice = models.BooleanField(default=1)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    slug = models.SlugField(null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def contain_exercice(self):
        return bool(self.have_exercice)

    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save()
