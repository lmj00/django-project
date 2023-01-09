from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'price',
            'category',
            'image1',
            'image2',
            'image3'
        ]


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'price',
            'category',
            'image1',
            'image2',
            'image3',
            'is_sold'
        ]