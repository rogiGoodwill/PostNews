from django.forms import ModelForm, DateField
from .models import Post

class NewsModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'category', 'title', 'text', 'rating']

