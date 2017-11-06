from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.contrib.auth.models import User

class Exercice(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField('Content')
    pub_date = models.DateTimeField('date published')
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

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
    pub_date = models.DateTimeField('date published')
    content = models.TextField('Content')
    ratings = GenericRelation(Rating, related_query_name='solutions')

    def __str__(self):
        return self.title

    """
    On pourra donc lister les commentaires d'un post via Solution.objects.filter(Exercice=self.object.id).select_related()
    """

#Solution.objects.filter(rating__isnull=False).order_by('ratings__average')
