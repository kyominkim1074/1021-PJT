from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "content", "movie_name", "grade", "image"]
        labels = {
            "title": "제목",
            "content": "내용",
            "movie_name": "영화 제목",
            "grade": "평점",
            "image": "이미지 파일",
        }
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("review", "user")
