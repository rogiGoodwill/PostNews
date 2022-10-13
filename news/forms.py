from django.contrib.auth.models import Group
from django.forms import ModelForm, DateField
from allauth.account.forms import SignupForm
from .models import Post

class NewsModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'category', 'title', 'text', 'rating']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user