from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog, BlogCategory, BlogSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.
def single_slug(request, single_slug):
	categories = [c.category_slug for c in BlogCategory.objects.all()]
	if single_slug in categories:
		matching_blogs = BlogSeries.objects.filter(blog_category__category_slug = single_slug)
		series_urls = {}
		for m in matching_blogs:
			part_one = Blog.objects.filter(blog_series=m)
			for i in part_one:
				series_urls[m] = i.blog_slug
		return render(request,
					  'main/category.html',
					  context = {'blog_series':matching_blogs,'part_ones':series_urls}
					  )

	blogs = [b.blog_slug for b in Blog.objects.all()]
	if single_slug in blogs:
		this_blog = Blog.objects.filter(blog_slug = single_slug)
		return render(request,
					  'main/blog.html',
					  context = {'blogs':this_blog})


	else:
		return HttpResponse(f'{single_slug} does not correspond to anything.')



def index(request):
	return render(request = request,
			template_name ='main/categories.html',
			context = {'Blogs':BlogCategory.objects.all()}
		)


def register(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.info(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect('main:index')
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
			return render(request = request,
						  template_name='main/register.html',
						  context = {"form":form}
						)

	
	form = NewUserForm
	return render(request,
				  'main/register.html',
				  context={'form':form}
		)

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect('main:index')

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('main:index')
			else:
				messages.error(request, "Invalid username or password")
		else:
				messages.error(request, "Invalid username or password")	
	form =AuthenticationForm()
	return render(request,
				'main/login.html',
				{'form':form}
		)
