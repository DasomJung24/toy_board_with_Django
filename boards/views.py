import json
import os

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, FormView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.db.models import F, Count, OuterRef, Subquery, Q
from django.contrib import messages

from .models import Post, Favorite, Comment, UploadFile
from .forms import PostForm, CommentForm, UploadFileForm


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.password = request.POST.get('password', None)

        if request.user.is_superuser:
            pass
        elif not self.object.user:
            if not check_password(self.password, self.object.password):
                raise PermissionDenied("no perm")
            else:
                pass
        elif self.object.user != request.user:
            raise PermissionDenied("no perm")

        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    """
    게시물 리스트 불러오기
    """
    model = Post
    template_name = 'boards/boards.html'
    http_method_names = ['get']
    context_object_name = 'posts'
    paginate_by = 15
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        page = context['page_obj']
        current_page = page.number
        total_pages = page.paginator.num_pages
        start_index = (current_page - 1) // 10 * 10

        context['previous_flag'] = True if current_page > 10 else False
        context['next_flag'] = True if ((current_page - 1) // 10 + 1) * 10 < total_pages else False
        context['page_range'] = page.paginator.page_range[start_index:start_index+10]
        context['previous_page_list'] = start_index 
        context['next_page_list'] = start_index + 11
        context['count'] = self.count
        context['order'] = self.order
        context['select'] = self.select
        context['value'] = self.value

        return context

    def get_queryset(self):
        self.select = self.request.GET.get('select', None)
        self.value = self.request.GET.get('input', None)
        self.order = self.request.GET.get('order', None)

        queryset = super(PostListView, self).get_queryset()
        queryset = queryset.select_related('user')
        
        # favorite_count : 해당 포스트를 좋아요를 누른 유저의 수
        # comment_count : 포스트에 달린 댓글 개수
        queryset = queryset.annotate(
            favorite_count=Subquery(
                Favorite.objects.filter(post=OuterRef('pk')).values('post')
                .annotate(count=Count('pk')).values('count')),
            comment_count=Subquery(
                Comment.objects.filter(post=OuterRef('pk'), is_delete=False).values('post')
                .annotate(count=Count('pk')).values('count')),
        )

        if self.select:
            values = self.value.split(' ') if ' ' in self.value else self.value

            for value in values:
                queryset = queryset.filter(Q(title__icontains=value) | Q(content_text__icontains=value) | Q(user__name__icontains=value))

        self.count = queryset.count()

        return queryset.order_by(self.order) if self.order else queryset   


class PostCreateView(CreateView):
    """
    게시물 생성하기
    """
    model = Post
    http_method_names = ['post', 'get']
    form_class = PostForm

    def get_form_kwargs(self):
        user = self.request.user
        password = self.request.POST.get('password', None)
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs["user"] = user if user.is_authenticated else None

        if not user.is_authenticated and not password:
            raise PermissionDenied(_('no password'))

        kwargs["password"] = make_password(password) if password else None
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({'id': form.instance.id}, status=201)

    def form_invalid(self, form):
        return JsonResponse({'errors': {**form.errors.get_json_data()}}, status=400)

    def get(self, request, *args, **kwargs):
        return render(request, 'boards/post_create.html')


class UploadFileView(FormView):
    """
    파일 업로드 하기
    """
    model = UploadFile
    http_method_names = ['post']
    form_class = UploadFileForm
    success_url = 'boards/post_create.html'

    def get_file_path(self, filename):
        return f"post/{timezone.now().strftime('%Y%m%D')}/{filename}"

    def form_valid(self, form):
        form.save()
        file_path = self.get_file_path(filename=self.request.FILES['file'])
        file_to_storage = default_storage.save(file_path, self.request.FILES['file'])
        return JsonResponse({'url': default_storage.url(file_to_storage)}, status=201)

    def form_invalid(self, form):
        return JsonResponse({'errors': {**form.errors.get_json_data()}}, status=400)


class PostDetailView(DetailView):
    """
    게시물 상세 페이지
    """
    model = Post
    template_name = 'boards/post_detail.html'
    http_method_names = ['get', 'post']
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        post = self.get_object()
        post.views = F('views') + 1
        post.save()
        context = {
            'favorite_count': post.favorites.count(),
            'comment_list': post.comments.filter(parent_id__isnull=True),
        }
        if self.request.user.is_authenticated:
            context['favorite'] = self.request.user.favorites.filter(post_id=post.id).exists()

        return super(PostDetailView, self).get_context_data(**context)

    def get_queryset(self):
        return Post.objects.select_related(
            'user',
        ).all()

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        password = request.POST['password']

        # 비회원이 상세페이지에서 수정하기 클릭했을 때 비밀번호 확인
        if request.GET.get('method', None) == 'UPDATE':
            if not check_password(password, post.password):
                messages.error(request, '비밀번호를 다시 확인해 주세요.')
                return redirect('/board/posts/' + str(kwargs['post_id']))
            else:
                request.password = password
                return render(request, 'boards/post_update.html', {'post': post})

        # 비회원 게시물 상세페이지 비밀번호 확인
        elif request.GET.get('method', None) == 'GET':
            if not check_password(password, post.password):
                messages.error(request, '비밀번호를 다시 확인해 주세요.')
                return redirect('/board/posts')
            else:
                return redirect('/board/posts/' + str(kwargs['post_id']))


class PostUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    게시물 수정하기
    """
    model = Post
    template_name = 'boards/post_update.html'
    http_method_names = ['post', 'get']
    form_class = PostForm
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.object.user if self.object.user else None
        kwargs["password"] = make_password(self.password) if self.password else None
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'boards/post_update.html', context)

    def form_invalid(self, form):
        messages.error(self.request, '형식에 맞지 않습니다. 다시 작성해 주세요.')
        return redirect('/board/posts/update/' + str(self.kwargs['post_id']))


class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    게시물 삭제하기
    """
    model = Post
    http_method_names = ['post']
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        post = self.object
        post.delete()
        messages.success(request, '삭제가 완료되었습니다.')
        return redirect('/board/posts')


class FavoriteView(View):
    """
    좋아요 생성/삭제하기
    """
    model = Favorite
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST
        favorite, flag = Favorite.objects.get_or_create(user=request.user, post_id=data['id'])
        if flag:
            return JsonResponse({'msg': False, 'id': data['id']}, status=200)
        else:
            favorite.delete()
            return JsonResponse({'msg': True, 'id': data['id']}, status=200)


class CommentCreateView(CreateView):
    """
    댓글 생성하기
    """
    model = Comment
    http_method_names = ['post']
    form_class = CommentForm

    def get_form_kwargs(self):
        data = self.request.POST
        user = self.request.user
        password = data.get('password', None)
        kwargs = super(CommentCreateView, self).get_form_kwargs()
        kwargs['parent_id'] = data['parent_id'] if data['parent_id'] else None
        kwargs['user'] = user if user.is_authenticated else None

        if not user.is_authenticated and not password:
            messages.error(self.request, '비밀번호를 입력해주세요.')
            raise PermissionDenied('no perm')

        kwargs["password"] = make_password(password) if password else None
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('/board/posts/' + str(form.instance.post.id))

    def form_invalid(self, form):
        messages.error(self.request, '형식에 맞지 않습니다. 다시 작성해 주세요.')
        return redirect('/board/posts/' + str(form.instance.post.id))


class CommentUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    댓글 수정
    """
    model = Comment
    http_method_names = ['post']
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_form_kwargs(self):
        data = self.request.POST
        kwargs = super(CommentUpdateView, self).get_form_kwargs()
        kwargs['parent_id'] = data['parent_id'] if data['parent_id'] else None
        kwargs['user'] = self.object.user if self.object.user else None
        kwargs['password'] = make_password(self.password) if self.password else None
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({'msg': 'ok'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'msg': {**form.errors.get_json_data()}}, status=400)


class CommentDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    댓글 삭제
    """
    model = Comment
    http_method_names = ['post']
    pk_url_kwarg = 'comment_id'

    def delete(self, request, *args, **kwargs):
        comment = self.object
        comment.is_delete = True
        comment.save()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('/board/posts/' + str(kwargs['post_id']))
