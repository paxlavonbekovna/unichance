from urllib.parse import unquote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
import json
from .models import UserProfile, University, ApplicationDocument

def register_view(request):
    if request.user.is_authenticated:
        return redirect('unichance_dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, sat_score=0, ielts_score=0.0, budget=0)
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('unichance_dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'unichance/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('unichance_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('unichance_dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'unichance/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import University, UserProfile

@login_required
def dashboard_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    all_universities = University.objects.all()

    context = {
        'user_profile': user_profile,
        'universities': all_universities, 
    }
    return render(request, 'unichance/index.html', context)


@login_required
def universities_directory_view(request):
    """
    Fetches all institutions stored in the SQL database core and passes them 
    forward to populate the search directory grid page.
    """
    all_unis = University.objects.all()
    
    context = {
        'universities': all_unis,
        'universities_list': all_unis,
    }
    return render(request, 'unichance/universities.html', context)

@login_required(login_url='login')
def profile_settings_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        sat = request.POST.get('sat_score')
        ielts = request.POST.get('ielts_score')
        budget = request.POST.get('budget')
        
        profile.sat_score = int(sat) if sat else 0
        profile.ielts_score = float(ielts) if ielts else 0.0
        profile.budget = int(budget) if budget else 0
        profile.save()
        
        messages.success(request, "Academic data saved successfully!")
        return redirect('unichance_dashboard')
        
    return render(request, 'unichance/profile.html', {'profile': profile})

def university_search_api(request):
    query = request.GET.get('q', '')
    unis = University.objects.filter(name__icontains=query)
    results = []
    for u in unis:
        results.append({
            'name': u.name,
            'country': u.country,
            'cost_per_year': u.cost_per_year,
            'match_status': u.match_status,
            'match_status_display': u.match_status.upper()
        })
    return JsonResponse({'universities': results})


def all_universities_api(request):
    unis = University.objects.all()
    results = [{'name': u.name, 'country': u.country, 'cost_per_year': u.cost_per_year, 'match_status': u.match_status} for u in unis]
    return JsonResponse({'universities': results})

def toggle_document_status_api(request, doc_id):
    try:
        doc = ApplicationDocument.objects.get(id=doc_id)
        doc.is_completed = not doc.is_completed
        doc.save()
        return JsonResponse({
            'success': True,
            'is_completed': doc.is_completed,
            'display_text': 'Ready' if doc.is_completed else 'Pending'
        })
    except ApplicationDocument.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Document not found'})

@login_required
def university_profile_view(request, university_name):
    decoded_name = unquote(university_name)
    university_obj = get_object_or_404(University, name__iexact=decoded_name)
    
    context = {
        'university': university_obj,
        'uni': university_obj,
    }
    return render(request, 'unichance/university_profile.html', context)


@login_required
def document_examples_view(request):
    """
    Renders the document benchmarks, statement of purpose guides, 
    and blueprint example catalog files.
    """
    return render(request, 'unichance/document_examples.html')