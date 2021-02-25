from django import forms

from .models import Post, Comment, UploadFile


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('user', 'title', 'content', 'password', 'content_text', )
        
    def __init__(self, user, password, *args, **kwargs):
        self.user = user
        self.password = password
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, set_password=None):
        if self.password:
            self.instance.password = self.password
        self.instance.user = self.user
        return super(PostForm, self).save(commit)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('user', 'post', 'content', 'parent', 'root', 'password', )

    def __init__(self, user, parent_id, password, *args, **kwargs):
        self.user = user
        self.parent_id = parent_id
        if self.parent_id:
            parent_comment = Comment.objects.get(pk=self.parent_id)
            self.root_id = parent_comment.root_id if parent_comment.root_id else self.parent_id
        else:
            self.root_id = None
        self.password = password
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.parent_id = self.parent_id
        self.instance.root_id = self.root_id
        if self.password:
            self.instance.password = self.password
        return super(CommentForm, self).save(commit)


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadFile
        fields = ('post', 'file')
