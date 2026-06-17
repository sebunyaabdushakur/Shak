from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo
from .forms import TodoForm


def todo_list(request):
    filter_status = request.GET.get('filter', 'all')
    priority = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')

    todos = Todo.objects.all()

    if search_query:
        todos = todos.filter(title__icontains=search_query)

    if filter_status == 'active':
        todos = todos.filter(completed=False)
    elif filter_status == 'completed':
        todos = todos.filter(completed=True)

    if priority:
        todos = todos.filter(priority=priority)

    total = Todo.objects.count()
    active = Todo.objects.filter(completed=False).count()
    completed = Todo.objects.filter(completed=True).count()

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


def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added!')
        else:
            messages.error(request, 'Please enter a task title.')
    return redirect('todo_list')


def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect(request.META.get('HTTP_REFERER', 'todo_list'))


def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/edit.html', {'form': form, 'todo': todo})


def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted.')
    return redirect('todo_list')


def clear_completed(request):
    if request.method == 'POST':
        Todo.objects.filter(completed=True).delete()
        messages.success(request, 'Cleared completed tasks.')
    return redirect('todo_list')
