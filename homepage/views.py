import time
import traceback
from .models import User, Post
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Likes
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# -----


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data.get('user_name', None)
        user_email = data.get('user_email', None)
        password = data.get('user_password', None)

        if user_name and user_email and password:
            try:
                user = User.objects.create_user(
                    user_name=user_name, user_email=user_email, password=password)
                return JsonResponse({'status': 'success', 'message': 'User created successfully.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data.get('user_name', None)
        password = data.get('user_password', None)

        if user_name and password:
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'User verified successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'User logged out successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})





@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all().values()  # get all users
        user_list = list(users)  # important: convert the QuerySet to a list
        return JsonResponse(user_list, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data.get('user_name', None)
        password = data.get('user_password', None)

        if user_name and password:
            try:
                user = authenticate(
                    request, username=user_name, password=password)
                logout(request, user)
                if user is not None:
                    user.delete()
                    return JsonResponse({'status': 'success', 'message': 'User deleted successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User does not exist.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def make_post(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                user_name = request.user.user_name
                data = json.loads(request.body.decode('utf-8'))
                post_title = data.get('post_title', None)
                post_description = data.get('post_description', None)
                post_content = data.get('post_content', None)
                post_ispublic = data.get('post_ispublic', None)

                if user_name is not None:
                    post = Post.objects.create(
                        post_title=post_title,
                        post_description=post_description,
                        post_content=post_content,
                        post_ispublic=post_ispublic,
                        user=request.user
                    )
                    return JsonResponse({'status': 'success', 'message': 'Post created successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Kindly login to post your blog/post.'})
        except:
            return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    




@csrf_exempt
def feeds(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # get all public posts and private posts of the authenticated user
            posts = Post.objects.filter(Q(post_ispublic=True) | Q(user=request.user))

            post_list = []
            for post in posts:
                post_dict = {
                    'post_id': post.post_id,
                    'post_title': post.post_title,
                    'post_description': post.post_description,
                    'post_content': post.post_content,
                    'post_creationdate': post.post_creationdate,
                    'post_ispublic': post.post_ispublic,
                    'user': post.user.user_name,
                    'like_count': Likes.objects.filter(post=post).count()  # get the like count for the post
                }
                post_list.append(post_dict)

            return JsonResponse(post_list, safe=False)
        else:
            return JsonResponse({'status': 'error', 'message': 'Please log in first.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




@csrf_exempt
def like_feeds(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            post_ids = data.get('post_ids', [])

            for post_id in post_ids:
                try:
                    post = Post.objects.get(post_id=post_id)
                    Likes.objects.create(user=request.user, post=post)
                except Post.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Post with id {post_id} does not exist.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})

            return JsonResponse({'status': 'success', 'message': 'Posts liked successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please log in first.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def dislike_feeds(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            post_ids = data.get('post_ids', [])

            for post_id in post_ids:
                try:
                    post = Post.objects.get(post_id=post_id)
                    like = Likes.objects.get(user=request.user, post=post)
                    like.delete()
                except Post.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Post with id {post_id} does not exist.'})
                except Likes.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'You have not liked post with id {post_id} yet.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})

            return JsonResponse({'status': 'success', 'message': 'Posts disliked successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please log in first.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            post_id = data.get('post_id', None)

            if post_id is not None:
                try:
                    post = Post.objects.get(post_id=post_id)
                    if post.user == request.user:
                        post.delete()
                        return JsonResponse({'status': 'success', 'message': 'Post deleted successfully.'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'You cannot delete someone else\'s post.'})
                except Post.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Post with id {post_id} does not exist.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please log in first.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
