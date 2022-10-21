from nntplib import ArticleInfo
from django.shortcuts import render, redirect
from reviews.models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "작성이 완료되었습니다.")
            return redirect("reviews:index")
    else:
        form = ReviewForm()
    context = {
        "form": form,
    }
    return render(request, "reviews/create.html", context)


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/index.html", context)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        'comments': review.comment_set.all(),
        'comment_form': comment_form
    }
    return render(request, "reviews/detail.html", context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("reviews:detail", review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        "review": review,
        "form": form,
    }
    return render(request, "reviews/update.html", context)


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            messages.success(request, "글이 삭제되었습니다.")
            return redirect("reviews:index")
        return render(request, "reviews/detail.html")
    else:
        return redirect("reviews:detail", review.pk)


@login_required
def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("reviews:detail", review.pk)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
            return redirect("reviews.detail", review_pk)
    else:
        messages.warning(request, "작성자만 삭제할 수 있습니다.")
    return redirect("reviews:detail", review_pk)
