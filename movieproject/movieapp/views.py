from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests import auth
from django.views import View

from .models import Movie, Review, Category
from .forms import MovieForm, ReviewForm,RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout

def movie_home(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})
    # return render(request, 'base.html')
def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    links = Category.objects.all()  # Fetch categories for the dropdown

    context = {
        'movies': movies,
        'categories': categories,
        'links': links,  # Include the links variable in the context
    }

    return render(request, 'movies/movie_list.html', context)
    # return render(request, 'movies/movie_list.html', {'movies': movies, 'categories': categories},context)

def category_movie_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    movies = Movie.objects.filter(category=category)
    
    context = {
        'category': category,
        'movies': movies,
    }
    
    return render(request, 'movies/category_movie_list.html', context)

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    if request.user == movie.added_by:
        editable = True
    else:
        editable = False

    return render(request, 'movies/movie_detail.html', {'movie': movie, 'editable': editable, 'reviews':reviews})



@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST,request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('/movie/list/')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


@login_required(login_url='/movie/login/')  
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, 'Review added successfully!')
            url = '/movie/mov/' + str(movie_id) + '/'
            return redirect(url)      
            # return redirect('/movie/movie/', movie_id=movie.id )
    else:
        form = ReviewForm()

    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/movie/login/')
    else:
        form = RegistrationForm()
    return render(request, 'movies/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/movie/list/')
    else:
        form = LoginForm()
    return render(request, 'movies/login.html', {'form': form})

# def user_logout(request):
#     auth.logout(request)
#     return redirect('/')
def user_logout(request):
    # Your logout logic...
    logout(request)
    return redirect('/movie/list/')

@login_required
def profile(request):
    return render(request, 'movies/profile.html')

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Check if the logged-in user is the one who added the movie
    if request.user == movie.added_by:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
               
                form.save()
                url = '/movie/mov/' + str(movie_id) + '/'
                return redirect(url)                
                
        else:
            form = MovieForm(instance=movie)
        return render(request, 'movies/edit_movie.html', {'form': form, 'movie': movie})
    else:
        # Handle unauthorized access (redirect or show an error message)
        return redirect('movie_list')

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Check if the logged-in user is the one who added the movie
    if request.user == movie.added_by:
        if request.method == 'POST':
            movie.delete()
            return redirect('/movie/list')
        return render(request, 'movies/delete_movie.html', {'movie': movie})
    else:
        # Handle unauthorized access (redirect or show an error message)
        return redirect('/movie/')
    
def search_movies(request):
    query = request.GET.get('q')
    searched_movie = None

    if query:
        movies = Movie.objects.filter(title__icontains=query)
        searched_movie = query
    else:
        movies = []

    context = {'query': query, 'movies': movies, 'searched_movie': searched_movie}
    return render(request, 'movies/search_results.html', context)

# def search_movies(request):
#     query = request.GET.get('q')
#     if query:
#         results = Movie.objects.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(actors__icontains=query)
#         )
#     else:
#         results = []
#     return render(request, 'movies/search_results.html', {'results': results, 'query': query})

# class CategoryMovieListView(View):
#     template_name = 'movie_list.html'  # Use the existing movie_list template

#     def get(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         movies = Movie.objects.filter(category=category)
#         context = {'movies': movies}
#         return render(request, self.template_name, context)

# def categories_list(request,category_id=None):
#     categories = Category.objects.all()
#     if category_id:
#         selected_category = get_object_or_404(Category, id=category_id)
#         movies = Movie.objects.filter(category=selected_category)
#         return render(request, 'movies/categories_list.html', {'categories': categories, 'movies': movies})
#     else:
#         return render(request, 'movies/categories_list.html', {'categories': categories})
    
#     # # Fetch all categories from the database
#     # categories = Category.objects.all()

#     # # Render the template with the list of categories
#     # return render(request, 'movies/categories_list.html', {'categories': categories})
# def category_detail(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     movies = Movie.objects.filter(category=category)
#     return render(request, 'movies/category_detail.html', {'category': category, 'movies': movies})