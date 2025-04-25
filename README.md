# T-Blog

T-Blog là một ứng dụng blog được xây dựng bằng Django, cho phép người dùng tạo và quản lý nội dung blog cá nhân.

## Tính năng

- Đăng ký và đăng nhập người dùng
- Tạo, chỉnh sửa và xóa bài viết
- Quản lý bài viết thông qua bảng điều khiển (dashboard)
- Trang chủ hiển thị bài viết mới nhất
- Hỗ trợ đa phương tiện (media)

## Cài đặt

### Yêu cầu

- Python 3.8 hoặc cao hơn
- Django 4.2.7
- MySQL 5.7 hoặc cao hơn
- Các gói phụ thuộc khác (xem requirements.txt)

### Bước cài đặt

1. Clone dự án về máy của bạn:
```
git clone https://github.com/hasmeddd/blog-new.git
cd blog-new
```

2. Cài đặt các gói phụ thuộc:
```
pip install -r requirements.txt
```

3. Cấu hình cơ sở dữ liệu MySQL:
   
   Dự án đã được cấu hình để kết nối với cơ sở dữ liệu MySQL `football-news`. Bạn có thể kiểm tra và chỉnh sửa cấu hình kết nối trong file `blog/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'football-news',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost'
       }
   }
   ```
   Hãy đảm bảo bạn đã tạo sẵn cơ sở dữ liệu có tên `football-news` trong MySQL.

4. Chạy migration để đồng bộ cấu trúc database:
```
python manage.py migrate
```

5. Tạo tài khoản admin:
```
python manage.py createsuperuser
```

6. Khởi chạy server:
```
python manage.py runserver
```

7. Truy cập ứng dụng tại địa chỉ: http://127.0.0.1:8000/

## Triển khai lên Hosting

### Chuẩn bị

1. Đảm bảo bạn đã có:
   - Tài khoản hosting hỗ trợ Python/Django
   - Cơ sở dữ liệu MySQL trên hosting

2. Cập nhật cấu hình database trong file `blog/settings.py` cho môi trường production:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'football-news',
           'USER': 'hosting_db_username',
           'PASSWORD': 'hosting_db_password',
           'HOST': 'hosting_db_host'
       }
   }
   ```

## Sử dụng

1. Đăng nhập vào hệ thống bằng tài khoản đã tạo
2. Sử dụng bảng điều khiển để quản lý bài viết
3. Tạo bài viết mới thông qua giao diện người dùng
4. Quản lý profile và cài đặt cá nhân

## Cấu trúc thư mục

- `blog/`: Cấu hình chính của Django project
- `HOME/`: Ứng dụng chính quản lý trang chủ và bài viết
- `dashboard/`: Ứng dụng quản lý bảng điều khiển người dùng
- `static/`: Chứa các file tĩnh (CSS, JavaScript, hình ảnh)
- `templates/`: Chứa các template HTML
- `media/`: Lưu trữ các file người dùng tải lên

