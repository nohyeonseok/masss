from django import forms
from .models import Portfolio, Comment


class NewBlog(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('가게명', '주소','image')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('내용','평점', 'created_date')