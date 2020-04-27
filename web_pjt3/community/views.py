from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.contrib.auth import get_user_model

# Create your views here.
def review_list(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/review_list.html', context)

def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm()
        context = {
            'form': form
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('accounts:login')

def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    context = {
        'review': review
    }
    return render(request, 'community/review_detail.html', context)
