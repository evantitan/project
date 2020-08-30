from django import forms
from .models import Comment, Bookmark

class ShareForm(forms.Form):
    to_email = forms.EmailField()
    message = forms.CharField(max_length=50)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class SearchForm(forms.Form):
    query = forms.CharField()


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title',)
