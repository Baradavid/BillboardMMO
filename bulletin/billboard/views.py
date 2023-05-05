from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin
from .models import Post, Category, Reply

from datetime import datetime

from .filters import PostFilter
from .forms import PostForm, BaseRegisterForm, ReplyForm

from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib import messages


class PostList(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class PostDetail(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'
    form_class = ReplyForm
    success_msg = 'Комментарий успешно создан, ожидайте подтверждения'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.reply_post = self.get_object()
        self.object.reply_user = self.request.user
        self.object.save()
        return super().form_valid(form)


def update_reply_status(request, pk, type):
    i = Reply.objects.get(pk=pk)
    if request.user != i.reply_post.author:
        return HttpResponse('Отклонено')
    if type == 'public':
        import operator
        i.status = operator.not_(i.status)
        i.save()
        template = 'reply_manage.html'
        context = {'i': i, 'status_reply': 'Комментарий успешно опубликован'}
        return render(request, template, context)
    elif type == 'delete':
        i.delete()
        return HttpResponse('''
        <div class="alert.alert-success">
        Комментарий удален
        </div>
        ''')
    return HttpResponse('1')


@login_required
def upgrade_me(request):
    user = request.user
    admins_group = Group.objects.get(name='admins')
    if not request.user.groups.filter(name='admins').exists():
        admins_group.user_set.add(user)
        User.objects.create(id=request.user.pk)
    return redirect('/')


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('billboard.add_post',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('billboard.update_post',)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'
    permission_required = ('billboard.delete_post',)


class PostSearch(PostList):
    template_name = 'post_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='admins').exists()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class ReplyList(ListView):
    model = Reply
    template_name = 'replies.html'
    context_object_name = 'replies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_reply'] = Reply.objects.filter(reply_user__id=self.request.user.id)
        return context




