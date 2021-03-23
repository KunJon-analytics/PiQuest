from django.db import models
from quiz.models import Category, Quiz
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.', verbose_name=("user friendly url"))
    description = models.TextField()
    email = models.EmailField()
    website = models.URLField(help_text='Project website', max_length=255)
    categories = models.ManyToManyField(Category, blank=True, related_name='projects')
    date_added = models.DateField('date added', auto_now_add=True)

    class Meta:
        verbose_name = 'Project'
        ordering = ['title']
        get_latest_by = 'date_added'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project:project_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('project:project_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('project:project_delete', kwargs={'slug': self.slug})

    def get_articlelink_create_url(self):
        return reverse('project:articlelink_create', kwargs={'project_slug': self.slug})
        



class ArticleLink(models.Model):
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=255)
    summary = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='articles')
    pub_date = models.DateField('date published')
    slug = models.SlugField(max_length=63, unique=True, help_text='A label for URL config.', verbose_name=("user friendly url"))
    quiz = models.ForeignKey(Quiz, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'project')

    def __str__(self):
        return "{}:{}" .format(self.project, self.title)

    def get_absolute_url(self):
        return self.project.get_absolute_url()

    def get_update_url(self):
        return reverse('project:articlelink_update', kwargs={'project_slug': self.project.slug, 'articlelink_slug': self.slug})

    def get_delete_url(self):
        return reverse('project:articlelink_delete', kwargs={'project_slug': self.project.slug, 'articlelink_slug': self.slug})
