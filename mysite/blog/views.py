from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Subject,Comment, Bookmark
from .forms import ShareForm,CommentForm,SearchForm,UserCommentForm, BookmarkForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.urls import reverse
from django.db.models import Count
from mysite import settings
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required


def home(request):
    form = SearchForm()
    all_tags = Tag.objects.all()
    recent_posts = Post.published.order_by('-publish')
    pp = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')
    return render(request, 'home.html', {   'all_tags':all_tags,
                                            'recent_posts':recent_posts,
                                            'pp':pp
                                        })

def post_detail(request, year, month, day, post):
    post_slug=post
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    tags_id = post.tags.values_list('id', flat=True)
    all_tags = Tag.objects.filter(id__in=tags_id)
    comments = post.comments.filter(status='active').order_by('-created_on')
    comment_form = CommentForm()
    save_form = BookmarkForm()
    user_comment_form = UserCommentForm()
    is_bookmarked = False
    if request.user.is_authenticated:
        if Bookmark.objects.filter(user=request.user, post=post).exists():
            is_bookmarked = True

    if post.subject.topic=='python-for-begginers':
        subject = Subject.objects.get(topic='python-for-begginers')
        template = 'python_for_begginers/detail.html'
        all_posts = subject.chapters.all()
        dict = {'all_tags':all_tags,
                'all_posts':all_posts,
                'post':post,
                'user_comment_form':user_comment_form,
                'comment_form':comment_form,
                'comments':comments,
                'is_bookmarked':is_bookmarked}

    else:
        template = 'random_posts/detail.html'
        similar_posts = Post.published.filter(tags__in=tags_id).exclude(id=post.id)
        dict = {'similar_posts':similar_posts,
                'post':post,
                'user_comment_form':user_comment_form,
                'comment_form':comment_form,
                'save_form':save_form,
                'comments':comments,
                'all_tags':all_tags,
                'is_bookmarked':is_bookmarked}

    return render(request, template, dict)

def share_by_email(request, post_id):
    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = cd['message']
            post = get_object_or_404(Post, id=post_id, status="published")
            post_url = post.get_absolute_url()
            send_mail(message, post_url, 'napster@gmail.com', [cd['to_email']], fail_silently=False)
            return render(request,'shared_done.html')
        else:
            return HttpResponse("Invalid input")
    else:
        form = ShareForm()
        return render(request, 'share_by_email.html', {'form':form})


def post_list_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    tag_id = tag.id
    all_tags = Tag.objects.all().exclude(id=tag_id)
    all_posts = Post.published.all().filter(tags=tag_id)
    return render(request, 'post/post_list_by_tag.html', {'all_posts':all_posts,
                                                            'all_tags':all_tags,
                                                            'tag':tag})

def learn(request):
    subjects = Subject.objects.all()
    return render(request,'post/learn.html', {'subjects':subjects})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    query = request.GET.get('search')
    results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'post/search_result.html', {'query':query,
                                                'results':results})

def bookmark_post(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        all_bookmark = Bookmark.objects.filter(user=request.user, post=post)
        if all_bookmark:
            all_bookmark.delete()
            return redirect(post.get_absolute_url())
        Bookmark.objects.create(user=request.user, post=post)
        return redirect(post.get_absolute_url())
    else:
        return redirect('account:login')


def post_comment(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = UserCommentForm(request.POST)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = None
                new_comment.save()
                return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='account:login')
def bookmark(request):
    all_bookmarks = Bookmark.objects.filter(user=request.user).order_by('-bookmarked_on')
    return render(request, 'bookmark_post.html', {'all_bookmarks':all_bookmarks})

def delete_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, user=request.user, id = id)
    if bookmark:
        bookmark.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("Selected post has been deleted!")



def comming_soon(request):
    return render(request, 'comming_soon.html')
