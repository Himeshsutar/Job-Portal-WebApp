from django.urls import path
from jobapp import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
]
