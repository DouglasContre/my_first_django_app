from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#las vistas van aca
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        print('envianado formulario al cliente')
        return render(request, 'signup.html', {
            'form' : UserCreationForm 
            })
    elif request.method == 'POST':
        
        if request.POST['password1'] == request.POST['password2']:
            print('Enviando datos')
            #register user
            try:
                user = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                username = user.username
                return render(request, 'welcome1.html', {'username': username})
            
            except IntegrityError:
                print('An exception occurred')
                return render(request, 'signup.html', {
                    'form' : UserCreationForm , 'error' : 'User already exists. Please try another username'
                    })
        elif request.POST['password1'] != request.POST['password2']:
            return render(request, 'signup.html', {
                'form' : UserCreationForm , 'error': 'Password is not same. Make sure to type confirmation password correctly'
                 })
        else:
        
            return render(request, 'signup.html', {
            'form' : UserCreationForm, 'error': 'an error occurred'
            })



def welcome1(request):
    return render(request, 'welcome1.html')


def terminar_sesion(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm, 'error': 'An error has accorred. User or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('main_dashboard') 
 
@login_required        
def main_dashboard(request):
    tasks = Task.objects.filter(user = request.user)
    if request.method == 'GET':
        return render(request ,'dashboard.html', {'tasks' : tasks, 'form': TaskForm})
    elif request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return render(request, 'dashboard.html', {'tasks': tasks, 'form': TaskForm})
        except ValueError:
            return render(request, 'dashboard.html',{'tasks': tasks, 'form': TaskForm, 'error': 'Please provide valid data'})


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    
    elif request.method == 'POST':
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance = task)
            form.save()
            return redirect('main_dashboard')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error':'An error occured and data may no have been saved'})
            
 
@login_required       
def complete_task(request, task_id):
     task = get_object_or_404(Task, pk = task_id, user=request.user)
     if request.method == 'POST':    
         task.datecompleted = timezone.now()  
         task.save() 
         return redirect('main_dashboard')

@login_required
def delete_task(request, task_id):
     task = get_object_or_404(Task, pk = task_id, user=request.user)
     if request.method == 'POST':    
         task.delete() 
         return redirect('main_dashboard')

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})