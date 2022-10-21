from nntplib import ArticleInfo
from django.shortcuts import render, redirect
from reviews.models import Review
from .forms import ReviewForm
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
    context = {
        "review": review,
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
