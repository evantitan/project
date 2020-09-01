from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings



class PublishedManager(models.Manager):
    def get_quaryset(self):
        return super(PublishedManager,self).get_quaryset().filter(status='published')

class Subject(models.Model):
    topic = models.CharField(max_length=30, unique=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.topic


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published', 'Published'),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters', null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()


    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                    self.publish.month,
                                                    self.publish.day, self.slug])


class Comment(models.Model):
    CHOICES = (('active','Active'),('inactive','Inactive'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=CHOICES, default='active')

    def __str__(self):
        return self.name



class Bookmark(models.Model):
    title = models.CharField(max_length=30, default='bookmark')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='all_post')
    bookmarked_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'bookmark for user {}'.format(self.user.first_name)
