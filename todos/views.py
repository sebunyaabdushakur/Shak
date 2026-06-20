from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm


@login_required
def todo_list(request):
    filter_status = request.GET.get('filter', 'all')
    priority = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')

    todos = Todo.objects.filter(user=request.user)

    if search_query:
        todos = todos.filter(title__icontains=search_query)

    if filter_status == 'active':
        todos = todos.filter(completed=False)
    elif filter_status == 'completed':
        todos = todos.filter(completed=True)

    if priority:
        todos = todos.filter(priority=priority)

    total = Todo.objects.filter(user=request.user).count()
    active = Todo.objects.filter(user=request.user, completed=False).count()
    completed = Todo.objects.filter(user=request.user, completed=True).count()

    form = TodoForm()

    context = {
        'todos': todos,
        'form': form,
        'filter_status': filter_status,
        'priority_filter': priority,
        'search_query': search_query,
        'total': total,
        'active': active,
        'completed': completed,
    }
    return render(request, 'todos/index.html', context)


@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task added!')
        else:
            messages.error(request, 'Please enter a task title.')
    return redirect('todo_list')


@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect(request.META.get('HTTP_REFERER', 'todo_list'))


@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/edit.html', {'form': form, 'todo': todo})


@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted.')
    return redirect('todo_list')


@login_required
def clear_completed(request):
    if request.method == 'POST':
        Todo.objects.filter(user=request.user, completed=True).delete()
        messages.success(request, 'Cleared completed tasks.')
    return redirect('todo_list')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Shak, {user.username}!')
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('todo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')