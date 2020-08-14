from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# mixin to check if user logged in and a test on the user
from .models import NewsStory
from .forms import StoryForm, updateStoryForm
from users.models import CustomUser

class StoryView(generic.DetailView):
    # view of the story selected : DetailView
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'

class AddStoryView(LoginRequiredMixin, generic.CreateView):
    # create a new story : CreatwView
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class IndexView(generic.ListView):
    # see a lsit of the stories ListView
    template_name = 'news/index.html'

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.order_by('-pub_date')[:4]
        context['all_stories'] = NewsStory.objects.order_by('-pub_date')
        return context

class UpdateStoryView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    # update a post: UpdateView
    model = NewsStory
    form_class = updateStoryForm
    template_name = 'news/updateStory.html'
    success_url = reverse_lazy('news:story')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        # test to get the post we are updating if the user is the author of the post with the mixin UserPassesTestMixin

class DeleteStoryView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    # Delete a post: DeleteView
    model = NewsStory
    template_name = 'news/deleteStory.html'
    success_url = reverse_lazy('news:index')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class AuthorView(generic.DetailView):
    template_name = 'news/author.html'
    model = CustomUser
    context_object_name = "author"