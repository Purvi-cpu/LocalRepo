from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from googletrans import Translator
from .utils import image_to_text, text_to_speech
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def upload_image(request):
    if request.method == "POST" and request.FILES['image']:
        # Save uploaded image
        ocr_lang = request.POST.get('ocr_lang','eng')
        target_lang = request.POST.get('target_lang','en')
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        image_full_path = fs.path(image_path)
        
        # Extract text from the image
        extracted_text = image_to_text(image_full_path,lang=ocr_lang)

        #Translate exctracted text to target language
        translator = Translator()
        translation = translator.translate(extracted_text, dest=target_lang)
        translated_text = translation.text
        
        # Convert text to speech
        audio_path = text_to_speech(translated_text,language=target_lang)
        audio_url =fs.url(audio_path)
        
        # Serve the result in the template
        return render(request, 'result.html', {
            'text':  translated_text,
            'audio_path': audio_url
        })
    
    return render(request, 'upload.html')

# Registration View
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Registration successful")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    
    return render(request, 'register.html')

# Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_image')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

# Logout View
def logout_user(request):
    logout(request)
    return redirect('login')

#login required
def some_protected_view(request):
    #only logged-in users can access this view
    return render(request,'upload.html','result.html')
