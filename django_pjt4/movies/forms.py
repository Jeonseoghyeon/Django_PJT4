from django import forms
from .models import *

# Create your models here.
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rank',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]