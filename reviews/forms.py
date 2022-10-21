from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "content", "movie_name", "grade"]
        labels = {
            "title": "제목",
            "content": "내용",
            "movie_name": "영화 제목",
            "grade": "평점",
        }
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("review", "user")
