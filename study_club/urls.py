"""
URL configuration for study_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from members import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup' ),
    path('welcome1/', views.welcome1, name='welcome1'),
    path('terminar_sesion', views.terminar_sesion, name='terminar_sesion'),
    path('signin/', views.signin, name='signin'),
    path('main_dashboard/', views.main_dashboard, name='main_dashboard'),
    path('task/<int:task_id>', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'), 
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/completed', views.tasks_completed, name='tasks_completed')
    ]
