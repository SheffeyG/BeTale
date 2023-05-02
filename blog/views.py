import re
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from pure_pagination.mixins import PaginationMixin

from .models import Category, Post, Tag


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 10


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(category=cate)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return (
            super()
            .get_queryset()
            .filter(created_time__year=year, created_time__month=month)
        )


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(tags=t)


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super().get(request, *args, **kwargs)

        # 将文章阅读量 +1
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response
    
    def get_context_data(self, **kwargs):
        # 重写进行公式渲染
        context = super().get_context_data(**kwargs)

        text = context['post'].body
        # 要先对行间公式处理，然后才对行内公式处理
        pattern2 = re.compile(r'(\$\$)(.*?)(\$\$)', re.S)
        pattern1 = re.compile(r'(\$)(.*?)(\$)', re.S)
        text = re.sub(pattern2, '<div align=center><img src="http://latex.codecogs.com/svg.latex?\g<2>"></div>', text)
        text = re.sub(pattern1, '<img src="http://latex.codecogs.com/svg.latex?\g<2>">', text)

        context['post'].body = text

        return context


