# finalregapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import SignUpForm
from .models import PDF

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def home(request):
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES['pdf_file']
        pdf = PDF(title=title, file=file)
        pdf.save()
        return redirect('home')  # Redirect to home page after successful PDF upload
    
    pdfs = PDF.objects.all()
    return render(request, 'home.html', {'pdfs': pdfs})

@login_required
def download_pdf(request, pdf_id):
    pdf = PDF.objects.get(id=pdf_id)
    response = FileResponse(pdf.file.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.file.name}"'
    return response

def logout_page(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
