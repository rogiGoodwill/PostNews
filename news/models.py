from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rate_posts = Post.objects.filter(author=self).aggregate(Sum('rating')).get('rating__sum')
        rate_comment_by_author = Comment.objects.filter(user=self.author).aggregate(Sum('rating')).get('rating__sum')
        rate_comment_to_author = Comment.objects.filter(post__author=self).aggregate(Sum('rating')).get('rating__sum')
        self.rating = rate_posts * 3 + rate_comment_by_author + rate_comment_to_author
        self.save()

    def __str__(self):
        return str(self.author)

class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.cat_name)


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_LIST = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_LIST, default=article)
    time_create_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Заголовок')
    text = models.TextField(default='Текст статьи/новости')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        text = self.text[:124] + '...'
        return text

    def __str__(self):
        return str(self.title)

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + str(self.post)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_txt = models.TextField()
    time_create_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def __str__(self):
        return str(self.comment_txt)