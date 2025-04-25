from datetime import datetime, timedelta
import random
import re
from django.utils import timezone
import pytz
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import unidecode
from HOME.models import Post, Category, Comment, PostVersion
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.contrib import messages

# Create your views here.
# Định nghĩa BlogForm
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'image', 'content', 'category', 'status', 'section', 'Main_post']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'Main_post': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

def is_superuser(user):
    return user.is_authenticated and user.is_superuser 

@user_passes_test(is_superuser, login_url='login')
def dashboard(request):    
     # Lấy các tham số lọc từ request.GET
    period = request.GET.get('period', 'today')  # Mặc định là 'today'
    category = request.GET.get('category', '')

    # Lấy thời gian hiện tại
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today = timezone.now().astimezone(vn_tz).date()
    start_date = None
    end_date = today

    # Xác định khoảng thời gian dựa trên period
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Tuần này
        end_date = today
    elif period == 'last_week':
        last_monday = today - timedelta(days=today.weekday() + 7)  # Thứ Hai tuần trước
        last_sunday = last_monday + timedelta(days=6)  # Chủ Nhật tuần trước
        start_date = last_monday
        end_date = last_sunday
    elif period == 'month':
        start_date = today.replace(day=1)  # Ngày đầu tiên của tháng
        end_date = today
    elif period == 'last_month':  
        first_of_current_month = today.replace(day=1)
        last_day_last_month = first_of_current_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month

    # Lọc bài viết
    posts = Post.objects.all()
    users = User.objects.all()
    comments = Comment.objects.all()

    # Lọc bài viết theo danh mục
    if category:
        posts = posts.filter(category__slug=category)

    # Lọc bài viết, người dùng, và bình luận theo khoảng thời gian
    if start_date and end_date:
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        posts = posts.filter(created_at__range=[start_datetime, end_datetime])
        users = users.filter(date_joined__range=[start_datetime, end_datetime])
        comments = comments.filter(post__in=posts)  # Bình luận dựa trên bài viết đã lọc

    # Tính toán các số liệu thống kê
    total_views = posts.aggregate(total_views=Sum('views'))['total_views'] or 0
    total_comments = comments.count()  # Chỉ tính bình luận của bài viết đã lọc
    total_posts = posts.count()
    total_users = users.count()  # Dựa trên ngày tham gia của người dùng

    context = {
        'total_views': total_views,
        'total_comments': total_comments,
        'total_posts': total_posts,
        'total_users': total_users,
        'categories': Category.objects.all(),  # Để hiển thị danh sách danh mục trong form
        'selected_category': category,
        'period': period,  # Truyền period để giữ giá trị trong form
        'page_title': 'Thống kê',
    }
    return render(request, "dashboard/dash.html", context)

@user_passes_test(is_superuser, login_url='login')
def post(request):
    # Lấy danh sách danh mục để hiển thị trong filter
    categories = Category.objects.all()

    # Lấy các tham số lọc từ request.GET
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    period = request.GET.get('period', 'all')  # Thêm period, mặc định là 'all'
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    sort = request.GET.get('sort', 'newest')  # Mặc định là 'newest'

    # Lấy thời gian hiện tại
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today = timezone.now().astimezone(vn_tz).date()
    posts = Post.objects.all()

    # Xác định khoảng thời gian dựa trên period
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Tuần này
        end_date = today
    elif period == 'last_week':
        last_monday = today - timedelta(days=today.weekday() + 7)  # Thứ Hai tuần trước
        last_sunday = last_monday + timedelta(days=6)  # Chủ Nhật tuần trước
        start_date = last_monday
        end_date = last_sunday
    elif period == 'month':
        start_date = today.replace(day=1)  # Ngày đầu tiên của tháng
        end_date = today
    elif period == 'last_month':  
        first_of_current_month = today.replace(day=1)
        last_day_last_month = first_of_current_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month

    # Lọc bài viết theo khoảng thời gian nếu có period hoặc start_date/end_date
    if start_date and end_date:
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        posts = posts.filter(created_at__range=[start_datetime, end_datetime])

    # Lọc theo tìm kiếm (title hoặc category name)
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(category__name__icontains=search))

    # Lọc theo danh mục
    if category:
        posts = posts.filter(category__slug=category)

    # Sắp xếp bài viết
    if sort == 'newest':
        posts = posts.order_by('-created_at', '-post_id')
    elif sort == 'oldest':
        posts = posts.order_by('created_at', 'post_id')
    elif sort == 'title_asc':
        posts = posts.order_by('title')
    elif sort == 'title_desc':
        posts = posts.order_by('-title')
    elif sort == 'draft':
        posts = posts.filter(status='0').order_by('-created_at', '-post_id')
    elif sort == 'most_liked':
        posts = posts.order_by('-liked_by', '-post_id')  # Sắp xếp theo lượt thích giảm dần
    elif sort == 'most_viewed':
        posts = posts.order_by('-views', '-post_id')  # Sắp xếp theo lượt xem giảm dần

    # Phân trang
    paginator = Paginator(posts, 7)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'post': posts,
        'categories': categories,
        'search': search,
        'selected_category': category,
        'start_date': start_date,
        'end_date': end_date,
        'period': period,  # Truyền period để giữ giá trị trong template
        'sort': sort,
        'page_title': 'Quản lý bài viết',
    }
    return render(request, "dashboard/dash_post.html", context)

@user_passes_test(is_superuser, login_url='login')
def comment(request):
    search = request.GET.get('search', '')
    period = request.GET.get('period', 'all')  # Thêm period, mặc định là 'all'
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    sort = request.GET.get('sort', 'newest')  

    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today = timezone.now().astimezone(vn_tz).date()
    all_comments = Comment.objects.all()

    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Tuần này
        end_date = today
    elif period == 'last_week':
        last_monday = today - timedelta(days=today.weekday() + 7)  # Thứ Hai tuần trước
        last_sunday = last_monday + timedelta(days=6)  # Chủ Nhật tuần trước
        start_date = last_monday
        end_date = last_sunday
    elif period == 'month':
        start_date = today.replace(day=1)  # Ngày đầu tiên của tháng
        end_date = today
    elif period == 'last_month':  
        first_of_current_month = today.replace(day=1)
        last_day_last_month = first_of_current_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month

    # Lọc bình luận theo khoảng thời gian nếu có period hoặc start_date/end_date
    if start_date and end_date:
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        all_comments = all_comments.filter(created_at__range=[start_datetime, end_datetime])

    if sort == 'newest':
        all_comments = all_comments.order_by('-created_at')
    elif sort == 'oldest':
        all_comments = all_comments.order_by('created_at')

    paginator = Paginator(all_comments, 7)
    page_number = request.GET.get('page')
    all_comments = paginator.get_page(page_number)

    context = {
        'all_comments': all_comments,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
        'period': period,  
        'sort': sort,
        'page_title': 'Quản lý bình luận',
    }
    return render(request, "dashboard/comments.html", context)

@user_passes_test(is_superuser, login_url='login')
def user(request):
    search = request.GET.get('search', '')
    period = request.GET.get('period', 'all') 
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    sort = request.GET.get('sort', 'newest')

    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today = timezone.now().astimezone(vn_tz).date()
    users = User.objects.all()

    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Tuần này
        end_date = today
    elif period == 'last_week':
        last_monday = today - timedelta(days=today.weekday() + 7)  # Thứ Hai tuần trước
        last_sunday = last_monday + timedelta(days=6)  # Chủ Nhật tuần trước
        start_date = last_monday
        end_date = last_sunday
    elif period == 'month':
        start_date = today.replace(day=1)  # Ngày đầu tiên của tháng
        end_date = today
    elif period == 'last_month':  
        first_of_current_month = today.replace(day=1)
        last_day_last_month = first_of_current_month - timedelta(days=1)
        start_date = last_day_last_month.replace(day=1)
        end_date = last_day_last_month

    if start_date and end_date:
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        users = users.filter(date_joined__range=[start_datetime, end_datetime])

    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))

    if sort == 'newest':
        users = users.order_by('-date_joined')
    elif sort == 'oldest':
        users = users.order_by('date_joined')
    elif sort == 'active':
        users = users.filter(is_active=True).order_by('-date_joined')  
    elif sort == 'blocked':
        users = users.filter(is_active=False).order_by('-date_joined')  

    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    context = {
        'users': users_page,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
        'period': period,  
        'sort': sort,
        'page_title': 'Quản lý người dùng',
    }
    return render(request, "dashboard/users.html", context)

@user_passes_test(is_superuser, login_url='login')
def update_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền cập nhật thông tin người dùng!')
        return redirect('index')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        status = request.POST.get('status')

        updated = False
        if status:
            user.is_active = (status == 'active')
            updated = True

        if updated:
            user.save()
            messages.success(request, f"Người dùng {user.username} đã được cập nhật!")

        query_string = request.GET.urlencode()
        return redirect(f"/dashboard/users/?{query_string}" if query_string else "/dashboard/users/")
    
    return redirect('user')

# View xóa người dùng
@user_passes_test(is_superuser, login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.delete()
    messages.success(request, f"Người dùng {user.username} đã được xóa thành công!")
    return redirect('user')

# View để thêm bài viết
@user_passes_test(is_superuser, login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'page_title': 'Thêm bài viết',
    }
    return render(request, "dashboard/add_post.html", context)

@user_passes_test(is_superuser, login_url='login')
def update_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)  # Tìm bài viết theo ID
    versions = post.versions.all()  # Lấy tất cả các phiên bản trước đó
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Tạo phiên bản mới trước khi lưu thay đổi
            version_count = versions.count() + 1
            PostVersion.objects.create(
                post=post,
                title=post.title,
                author=post.author,
                content=post.content,
                category=post.category,
                version_number=version_count,
                modified_by=request.user
            )
            # Lưu cập nhật cho bài viết
            form.save()
            return redirect('post')  # Quay lại danh sách bài viết
    else:
        form = PostForm(instance=post)  # Hiển thị dữ liệu cũ để chỉnh sửa

    return render(request, 'dashboard/update_post.html', {
        'form': form, 
        'page_title': 'Chỉnh sửa bài viết',
        'post': post,
        'versions': versions
    })

@user_passes_test(is_superuser, login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    post.delete()  # Xóa bài viết
    return redirect('post') 

@user_passes_test(is_superuser, login_url='login')
def category(request):
    # Lấy các tham số lọc từ request.GET
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'newest')  # Mặc định là 'newest'

    # Lấy tất cả danh mục
    categories = Category.objects.all()

    # Lọc theo tìm kiếm (tên danh mục)
    if search:
        categories = categories.filter(name__icontains=search)

    # Sắp xếp danh mục
    if sort == 'newest':
        categories = categories.order_by('-created_at','-category_id')  # Mới nhất
    elif sort == 'oldest':
        categories = categories.order_by('created_at','category_id')  # Cũ nhất
    elif sort == 'name_asc':
        categories = categories.order_by('name')  # Tên A-Z
    elif sort == 'name_desc':
        categories = categories.order_by('-name')  # Tên Z-A

    # Phân trang
    paginator = Paginator(categories, 7)  # 7 danh mục mỗi trang
    page_number = request.GET.get('page')
    categories_page = paginator.get_page(page_number)

    context = {
        'categories': categories_page,
        'search': search,
        'sort': sort,
        'page_title': 'Quản lý danh mục bài viết',
    }
    return render(request, 'dashboard/dash_categorys.html', context)

def update_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, category_id=category_id)
        
        # Chỉ superuser mới có quyền cập nhật
        if not request.user.is_superuser:
            messages.error(request, "Bạn không có quyền cập nhật danh mục!")
            return redirect('category')

        # Lấy tên mới từ form
        new_name = request.POST.get('name')
        
        # Cập nhật tên (slug sẽ tự động cập nhật trong model)
        if new_name and new_name != category.name:
            new_slug = unidecode.unidecode(new_name).lower()
            new_slug = re.sub(r'[\W_]+', '-', new_slug).strip('-')
            category.name = new_name
            category.slug = new_slug
            category.save()
            messages.success(request, f"Danh mục {category.name} đã được cập nhật!")
        
        # Giữ lại query string để quay lại trang hiện tại
        query_string = request.GET.urlencode()
        return redirect(f"/dashboard/categorys/?{query_string}" if query_string else "/dashboard/categorys/")
    
    return redirect('category')

@user_passes_test(is_superuser, login_url='login')
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                # Tạo instance mới của Category
                category = Category(name=name)
                # Phương thức save của model sẽ tự động tạo slug
                category.save()
                messages.success(request, f"Danh mục '{category.name}' đã được thêm thành công!")
                return redirect('category')
            except Exception as e:
                messages.error(request, f"Lỗi khi thêm danh mục: {str(e)}")
        else:
            messages.error(request, "Vui lòng nhập tên danh mục!")
    
    context = {
        'page_title': 'Thêm danh mục mới',
    }
    return render(request, 'dashboard/add_category.html', context)

@user_passes_test(is_superuser, login_url='login')
def delete_category(request, category_id):
    cat = get_object_or_404(Category, category_id=category_id)
    cat.delete() 
    messages.success(request, "Danh mục đã được xóa!")
    return redirect('category')

@user_passes_test(is_superuser, login_url='login')
def delete_comment(request, comment_id):
    cmt = get_object_or_404(Comment, comment_id=comment_id)
    cmt.delete() 
    messages.success(request, "Bình luận đã được xóa!")
    return redirect('comment')

@user_passes_test(is_superuser, login_url='login')
def view_post_version(request, version_id):
    version = get_object_or_404(PostVersion, version_id=version_id)
    post = version.post
    
    # Tìm phiên bản trước đó để so sánh
    previous_version = None
    if version.version_number > 1:
        previous_version = PostVersion.objects.filter(
            post=post, 
            version_number=version.version_number - 1
        ).first()
    
    # Xác định những thay đổi
    changes = []
    if previous_version:
        if previous_version.title != version.title:
            changes.append('Tiêu đề')
        if previous_version.author != version.author:
            changes.append('Tác giả')
        if previous_version.content != version.content:
            changes.append('Nội dung')
        if previous_version.category != version.category:
            changes.append('Danh mục')
    
    context = {
        'version': version,
        'post': post,
        'previous_version': previous_version,
        'changes': changes,
        'page_title': f'{post.title} - Phiên bản {version.version_number}'
    }
    
    return render(request, 'dashboard/view_post_version.html', context)