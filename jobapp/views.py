# jobapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Job, Application, UserProfile
from .forms import JobForm, ApplicationForm, SignUpForm
from .decorators import employer_required, jobseeker_required
# -----------------------------
# Authentication Views
# -----------------------------

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'jobapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ✅ Redirect superuser to Django admin
            if user.is_superuser:
                return redirect('/admin/')

            # ✅ Redirect based on custom user role
            profile = get_object_or_404(UserProfile, user=user)

            if profile.role == "Employer":
                return redirect('employer_dashboard')
            elif profile.role == "Job Seeker":
                return redirect('home')  # or 'jobseeker_dashboard' if you have one

        else:
            return render(request, 'jobapp/login.html', {'error': 'Invalid credentials'})

    return render(request, 'jobapp/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')

# -----------------------------
# Home and Job Listings
# -----------------------------

@login_required
def home_view(request):
    # Only Job Seekers can access the home page
    if request.user.userprofile.role != "Job Seeker":
        return redirect('employer_dashboard')

    # Normal job listings logic
    search = request.GET.get('search')
    location = request.GET.get('location')
    jobs = Job.objects.all()

    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(company__icontains=search)
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'jobapp/home.html', {'jobs': jobs})


# -----------------------------
# Job Posting (Employers Only)
# -----------------------------
@login_required
@employer_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('home')  # Redirect after successful submission
    else:
        form = JobForm()
    return render(request, 'jobapp/post_job.html', {'form': form})


@login_required
@jobseeker_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            return redirect('home')  # Or redirect to a "my_applications" page
    else:
        form = ApplicationForm()

    return render(request, 'jobapp/apply_job.html', {'form': form, 'job': job})
# -----------------------------
# Custom Signup with Role Selection
# -----------------------------

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = request.POST.get('role')
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'jobapp/signup.html', {'form': form})

@login_required
def employer_dashboard(request):
    if request.user.userprofile.role != "Employer":
        return HttpResponseForbidden("You are not authorized to view this page.")

    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobapp/employer_dashboard.html', {'jobs': jobs})

@login_required
def jobseeker_dashboard(request):
    if request.user.userprofile.role != 'Job Seeker':
        return redirect('home')  # Optional: Prevent access if not job seeker

    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobapp/jobseeker_dashboard.html', {'applications': applications})

@login_required
def my_applications(request):
    # Replace Application with your actual model name if different
    applications = Application.objects.filter(applicant=request.user)

    return render(request, 'jobapp/my_applications.html', {'applications': applications})

@login_required
def my_jobs(request):
    if request.user.userprofile.role != "Employer":
        return redirect('home')  # or show a 403 page

    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobapp/my_jobs.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    # Apply logic only for Job Seekers
    if request.user.userprofile.role == "Job Seeker":
        if request.method == "POST":
            # Prevent duplicate applications
            existing = Application.objects.filter(job=job, applicant=request.user).first()
            if not existing:
                Application.objects.create(job=job, applicant=request.user)
            return redirect('my_applications')

    return render(request, 'jobapp/job_detail.html', {'job': job})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('my_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobapp/edit_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('my_jobs')
    return render(request, 'jobapp/delete_job.html', {'job': job})

def is_employer(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'employer'

