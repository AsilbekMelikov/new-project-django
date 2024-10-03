from django import forms
from .models import Contact, Comment


class ContactForms(forms.ModelForm):

    class Meta:
        model = Contact
        fields = "__all__"


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

        labels = {
            "body": ""
        }

        widgets = {
            "body": forms.Textarea(attrs={
                "placeholder": "Add a comment...",
                "rows": 5,
                "cols": 50,
                'style': 'border: 2px solid #ccc; border-radius:8px; padding: 10px;',
            })
        }