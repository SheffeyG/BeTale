from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags

import markdown

# Create your models here.
class Category(models.Model):
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    created = models.DateTimeField('创建时间', default=timezone.now)
    updated = models.DateTimeField('修改时间', auto_now=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        if self.excerpt == "":
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)