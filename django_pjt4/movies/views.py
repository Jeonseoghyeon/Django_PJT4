from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies':movies,
    }
    return render(request, 'movies/index.html', context)

@login_required
def create_movie(request):
    if request.user.is_superuser: #is_superuser 뒤에 () 쓰면 오류남
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('movies:index')
        else:
            form = MovieForm
        context = {
            'form': form,
        }
        return render(request, 'movies/form.html', context)
    return redirect('movies:index')

def detail_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail_movie.html', context)

@login_required
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:index')
    else:
        form = ReviewForm
    context = {
        'form': form,
    }
    return render(request, 'movies/form.html', context)

@require_POST
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('movies:index')

def detail_review(request, review_id):
    review = get_object_or_404(Review, id = review_id)
    form = CommentForm
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'movies/detail_review.html', context)



def update_review(request, review_id):
    pass

@login_required
@require_POST
def create_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
    return redirect('movies:detail_review', review_id)

def delete_comment(request):
    pass

@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    if user in review.like_users.all():
        review.like_users.remove(user)
    else:
        review.like_users.add(user)
    return redirect('movies:detail_review', review_id)


