
from django.shortcuts import render, redirect
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import User, UserImage
import face_recognition # type: ignore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User as DjangoUser
from .models import Document
from .forms import DocumentForm
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404, redirect



def home(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')
        face_image_data = face_image_data.split(',')[1]
        face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}_.jpg')
        
        try:
            user = User.objects.create(username=username)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists!'
            })
       
        UserImage.objects.create(user=user, face_image=face_image)
        return JsonResponse({
            'status': 'success',
            'message': 'User registered successfully!'
        })
        
    return render(request, 'register.html')



@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User does not exist!'
            })

        user_image = UserImage.objects.filter(user=user).last()
        if not user_image or not user_image.face_image:
            return JsonResponse({
                'status': 'error',
                'message': 'Face image not found for this user. Please register again.'
            })

        face_image_data = face_image_data.split(',')[1]
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}_.jpg')

        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)

        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
            stored_face_encoding = face_recognition.face_encodings(stored_face_image)[0]

            match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)

            if match[0]:
                django_user, created = DjangoUser.objects.get_or_create(username=username)
                auth_login(request, django_user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful!',
                    'redirect_url': '/dashboard/'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Face did not match.'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Face encoding failed. Try again.'
            })

    return render(request, 'login.html')


@login_required(login_url='/login/')


def dashboard(request):
    return render(request, 'dashboard.html')


def logout_user(request):
    logout(request)
    return redirect('home')  

@login_required(login_url='/login/')
def dashboard(request):
    # Fetch only this user's documents
    documents = Document.objects.filter(user=request.user)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user  # attach current user
            doc.save()
            return redirect('dashboard')  # refresh the page
    else:
        form = DocumentForm()

    return render(request, 'dashboard.html', {
        'form': form,
        'documents': documents
    })

@login_required
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, user=request.user)
    if request.method == "POST":
        doc.file.delete()  # Delete the actual file
        doc.delete()       # Delete the database record
    return redirect('dashboard') 


def some_view(request):
    user_image = UserImage.objects.filter(user=request.user).first()
    return render(request, 'dashboard.html', {'user_image': user_image})