from django.shortcuts import render, redirect
from .models import User


def login_view(request):
    if request.session.get('user_id'):
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        user = User.objects.filter(user=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session['username'] = user.user
            return redirect('home')

        error = 'نام کاربری یا رمز عبور اشتباه است.'

    return render(request, 'accounts/login.html', {'error': error})


def signup_view(request):
    if request.session.get('user_id'):
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        password_confirm = request.POST.get('password_confirm') or ''

        if not username or not password:
            error = 'نام کاربری و رمز عبور الزامی است.'
        elif password != password_confirm:
            error = 'رمز عبور و تکرار آن یکسان نیستند.'
        elif User.objects.filter(user=username).exists():
            error = 'این نام کاربری قبلاً گرفته شده است.'
        else:
            user = User.objects.create(user=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.user
            return redirect('home')

    return render(request, 'accounts/signup.html', {'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')