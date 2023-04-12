from django import template

from django.db.models.aggregates import Count

from ..models import Post, Category, Tag

register = template.Library()

@register.inclusion_tag('article/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }

@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created', 'month', order='DESC'),
    }

@register.inclusion_tag('article/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }
