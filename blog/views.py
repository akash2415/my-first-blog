from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

# Create your views here.

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
	if request.method == "POST":
		post_form = PostForm(request.POST)
		if post_form.is_valid():
			post = post_form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		post_form = PostForm()
	return render(request, 'blog/post_new.html', {'post_form': post_form})



def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		post_form = PostForm(request.POST, instance=post)
		if post_form.is_valid():
			post = post_form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		post_form = PostForm(instance=post)
	return render(request, 'blog/post_new.html', {'post_form': post_form})


