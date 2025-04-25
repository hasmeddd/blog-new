from datetime import datetime
# import json
# from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import*
from django.shortcuts import render , get_object_or_404, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('login')
        else:
            errors = form.errors.as_data()
            
            if 'username' in errors:
                for error in errors['username']:
                    if error.code == 'unique':
                        messages.error(request, 'Tên tài khoản đã tồn tại. Vui lòng chọn tên khác!')
                    else:
                        messages.error(request, f'Lỗi tên tài khoản: {error}')
            
            if 'password2' in errors:
                for error in errors['password2']:
                    if error.code == 'password_mismatch':
                        messages.error(request, 'Mật khẩu không khớp. Vui lòng kiểm tra lại!')
                    else:
                        messages.error(request, f'Lỗi mật khẩu: {error}')

            if not errors:
                messages.error(request, 'Đăng ký thất bại. Vui lòng kiểm tra lại thông tin!')

    context = {'form': form}
    return render(request, "register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.is_active:  
                    login(request, user)
                    messages.success(request, 'Đăng nhập thành công!')
                    return redirect('index')
                else:
                    messages.error(request, 'Tài khoản của bạn đã bị khóa!')
            else:
                messages.error(request, 'Username hoặc password không đúng!')
        except User.DoesNotExist:
            messages.error(request, 'Username hoặc password không đúng!')

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    messages.success(request, 'Đã đăng xuất!')
    return redirect('index')

def get_published_posts():
    return Post.objects.filter(status='1')

def index(request):
    post = get_published_posts().order_by('-post_id')
    main_post = get_published_posts().order_by('-post_id').filter(Main_post=True)[0:1]
    recent = get_published_posts().filter(section='Recent').order_by('-post_id')[:4]
    popular = popular = get_published_posts().filter(section='Popular').order_by('-post_id')[:4]
    cat = Category.objects.all()
    latest_posts = get_published_posts().order_by('-created_at')[:3]

    bong_da_vn = get_published_posts().filter(category__slug="bong-da-viet-nam").order_by('-post_id')[:5]
    doi_song = get_published_posts().filter(category__slug="doi-song").order_by('-post_id')[:5]
    bong_da_qt = get_published_posts().filter(category__slug="bong-da-quoc-te").order_by('-post_id')[:3]
    champions_league = get_published_posts().filter(category__slug="champions-league").order_by('-post_id')[:3]
    ngoai_hang_anh = get_published_posts().filter(category__slug="ngoai-hang-anh").order_by('-post_id')[:3]
    la_liga = get_published_posts().filter(category__slug="la-liga").order_by('-post_id')[:3]
    serie_a = get_published_posts().filter(category__slug="serie-a").order_by('-post_id')[:3]

    api_url = "https://data.bongdaplus.vn/data/top-home-matches.json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        matches_data = response.json()

        # Tạo danh sách matches từ dữ liệu gốc
        matches = []
        
        # Duyệt qua từng giải đấu
        for tournament in matches_data:
            for match in tournament.get('matches', []):
                if 'start_time' in match:
                    try:
                        # Chuyển đổi start_time sang datetime
                        match['start_time'] = datetime.strptime(match['start_time'], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        match['start_time'] = None 
                matches.append(match)  # Thêm match gốc vào danh sách
                
    except requests.exceptions.RequestException as e:
        matches = []
        print(f"Lỗi khi lấy dữ liệu API: {e}")

    post_list = get_published_posts().order_by('-post_id')
    paginator = Paginator(post_list, 3) 
    print(paginator)
    page = request.GET.get('page')
    
    try:
        latest_posts = paginator.page(page)
    except PageNotAnInteger:
        latest_posts = paginator.page(1)
    except EmptyPage:
        latest_posts = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'main_post': main_post,
        'recent': recent,
        'popular': popular,
        'cat': cat,
        'latest_posts': latest_posts,
        'bong_da_vn': bong_da_vn,
        'doi_song': doi_song,
        'bong_da_qt': bong_da_qt,
        'champions_league': champions_league,
        'ngoai_hang_anh': ngoai_hang_anh,
        'la_liga': la_liga,
        'serie_a': serie_a,
        'matches': matches, 
    }
    
    return render(request, "index.html", context)


def post_detail(request,slug):
    cat = Category.objects.all()
    xu_huong = Post.objects.order_by('-views')[:4]
    post = get_object_or_404(Post, post_slug = slug)
    Post.objects.filter(post_id=post.post_id).update(views=post.views + 1) 
    post.refresh_from_db() 
    # post.save()

    comments = Comment.objects.filter(post_id = post.post_id).order_by('-created_at')

    context = {
        # 'posts': post,
        'cat': cat,
        'post' : post,
        'xu_huong': xu_huong,
        'comments': comments, 
    }

    return render (request, "post_detail.html", context)


# def category(request, slug):
#     cat = category.objects.all()
#     post_cat = category.objects.filter(slug=slug)
#     context = {
#         'cat': cat,
#         'active_category' : slug,
#         "post_cat" : post_cat,

#     }
#     return render (request, 'category.html',context)

def add_comment(request, slug):
    post = get_object_or_404(Post, post_slug=slug)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để bình luận!')
        else:
            comment_text = request.POST.get('InputComment')
            name = request.user.username
            email = request.user.email

            Comment.objects.create(
                post=post,  
                name=name,
                email=email,
                comment=comment_text,
                created_at=timezone.now()  
            )
            messages.success(request, 'Bình luận đã được thêm!')
    
    return redirect('post_detail', slug=slug)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    p_slug = comment.post.post_slug  
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Bình luận đã được xóa!')
        return redirect('post_detail', slug=p_slug)
    
    return redirect('post_detail', slug=p_slug)

@login_required
def personal(request):
    user = request.user

    if request.method == 'POST':
        if 'update' in request.POST:
            form = UpdateUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thông tin cá nhân đã được cập nhật!')
                return redirect('personal')
            else:
                print(f"Lỗi form: {form.errors}")  
                messages.error(request, 'Có lỗi khi cập nhật thông tin. Vui lòng kiểm tra lại!')
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mật khẩu đã được thay đổi!')
                return redirect('personal')
            else:
                print(f"Lỗi password_form: {password_form.errors}") 
                messages.error(request, 'Có lỗi khi đổi mật khẩu. Vui lòng kiểm tra lại!')

    form = UpdateUserForm(instance=user)
    password_form = PasswordChangeForm(user)
    for field in password_form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    
    context = {
        'user': user,
        'form': form,
        'password_form': password_form,
    }
    return render(request, "personal.html", context)

@login_required
def recent_activity(request):
    user = request.user
    saved_posts = Post.objects.filter(saved_by=user)
    liked_posts = Post.objects.filter(liked_by=user)

    context = {
        'saved_posts': saved_posts,
        'liked_posts': liked_posts,
    }
    return render(request, "recent_activity.html", context)

def save_post(request, slug):
    post = get_object_or_404(Post, post_slug=slug)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để lưu bài viết!')
        elif request.user in post.saved_by.all():
            post.saved_by.remove(request.user)
            messages.success(request, 'Đã bỏ lưu bài viết!')
        else:
            post.saved_by.add(request.user)
            messages.success(request, 'Bài viết đã được lưu!')
    return redirect('post_detail', slug=slug)

def like_post(request, slug):
    post = get_object_or_404(Post, post_slug=slug)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để thích bài viết!')
        elif request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            messages.success(request, 'Bạn đã bỏ thích bài viết!')
        else:
            post.liked_by.add(request.user)
            messages.success(request, 'Bạn đã thích bài viết!')
    return redirect('post_detail', slug=slug)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            try:
                send_mail(
                    subject=subject, 
                    message=f"Tên: {name}\nNgười gửi: {email}\nNội dung: {message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,  
                    recipient_list=[settings.EMAIL_HOST_USER], 
                    fail_silently=False,
                )
                messages.success(request, 'Tin nhắn của bạn đã được gửi thành công!')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi gửi tin nhắn: {str(e)}')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')

        return render(request, "contact.html")

    context = {}
    return render(request, "contact.html", context)

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts_list = Post.objects.filter(category=category).order_by('-created_at')
    cat = Category.objects.all() 

    paginator = Paginator(posts_list, 3) 
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {
        'category': category,
        'posts': posts,
        'cat': cat,  
    })

def search_posts(request):
    query = request.GET.get('q', '')  
    results = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(category__name__icontains=query)
            ).distinct().order_by('-created_at')

    context = {
        'searched': query,
        'results': results,
    }
    return render(request, 'search.html', context)

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:  # Nếu không có email được nhập
            messages.error(request, 'Vui lòng nhập địa chỉ email!')
            return render(request, "includes/password_reset.html")
            
        try:
            user = User.objects.get(email=email)
            # Tạo token và uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Tạo link reset password
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Nội dung email
            subject = 'Yêu cầu đặt lại mật khẩu'
            message = render_to_string('includes/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            
            # Gửi email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Link đặt lại mật khẩu đã được gửi đến email của bạn!')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy tài khoản với email này!')
            return render(request, "includes/password_reset.html")
            
    return render(request, "includes/password_reset.html")

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if not password1 or not password2:
                messages.error(request, 'Vui lòng nhập cả hai mật khẩu!')
            elif password1 != password2:
                messages.error(request, 'Mật khẩu không khớp. Vui lòng kiểm tra lại!')
            else:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Mật khẩu đã được đặt lại thành công! Vui lòng đăng nhập.')
                return redirect('login')
            
            return render(request, 'includes/password_reset_confirm.html')
        
        return render(request, 'includes/password_reset_confirm.html')
    else:
        messages.error(request, 'Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn!')
        return redirect('password_reset_request')

