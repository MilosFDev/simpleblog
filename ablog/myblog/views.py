from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from .models import Post
from .forms import PostForm, EditForm, VideoSearchForm
from googleapiclient.discovery import build
from .models import Category


# ListView shows all posts
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering=['-post_date']

# DetailView shows one post's details
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

# CreateView adds a new post
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

# UpdateView updates an existing post
class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'

# DeleteView deletes a post
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = '/'  # Redirect after successful deletion

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields='__all__'




YOUTUBE_API_KEY = 'AIzaSyAyM2KKA52A16tyf2dZGKmRbKvqDtBhzr4'

def search_videos(request):
    videos = []
    form = VideoSearchForm()

    if request.method == 'GET' and 'query' in request.GET:
        form = VideoSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            youtube_request = youtube.search().list(
                q=query,
                part='snippet',
                maxResults=10,
                type='video'
            )
            response = youtube_request.execute()

            for item in response['items']:
                videos.append({
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'video_id': item['id']['videoId']
                })

    return render(request, 'video_search.html', {'form': form, 'videos': videos})






