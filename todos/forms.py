from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What needs to be done?',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add details (optional)',
                'rows': 3,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-input',
            }),
        }
