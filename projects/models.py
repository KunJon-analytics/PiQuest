from django.db import models
from quiz.models import Category 
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=31, db_index=True)
    url = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')
    description = models.TextField()
    email = models.EmailField()
    website = models.URLField(help_text='Project website', max_length=255)
    categories = models.ManyToManyField(Category, related_name='projects')
    date_added = models.DateField('date added', auto_now_add=True)

    class Meta:
        ordering = ['title']
        get_latest_by = 'date_added'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project:project_detail', kwargs={'url': self.url})
        



class ArticleLink(models.Model):
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=255)
    summary = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='articles')
    pub_date = models.DateField('date published')

    class Meta:
        verbose_name = 'article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __str__(self):
        return "{}:{}" .format(self.project, self.title)

    def get_absolute_url(self):
        return self.project.get_absolute_url()

