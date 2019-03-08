from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db.models import Q

class PublishedManager(models.Manager):
   def get_queryset(self):
       return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
                        ('draft', 'Draft'),
                        ('published', 'Published'),
                        )
    CATEGORY_CHOICES = (
        ('World','World'),
        ('9ja','9ja'),
        ('Technology','Technology'),
        ('Design','Design'),
        ('Culture','Culture'),
        ('Business','Business'),
        ('Politics','Politics'),
        ('Opinion','Opinion'),
        ('Science','Science'),
        ('Health', 'Health'),
        ('Style','Style'),
        ('Travel','Travel'),
    )
    title = models.CharField(max_length=250,null=True, blank=True)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES, default='World')
    slug = models.SlugField(max_length=250, unique_for_date='publish', unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.FileField(null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blogApp:post_details', args=[self.slug])

    @property
    def comment_post(self):
        return self.comment_set.all()


    class Meta:
        ordering = ('-publish',)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    # def save(sender, instance, *args, **kwargs):
    #     slug = slugify(instance.Post)
    #     exists = Post.objects.filter(slug=slug).exists
    #     if exists:
    #         slug = "{}-{}".format(slug, instance.id)
    #     instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)






class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager, self).get_queryset().filter('post')

class Comment(models.Model):
    posts = models.ForeignKey('blogApp.Post', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-posts',)


    def __str__(self):
        return self.comments
