# -*- coding: utf-8 -*-
from models import Book, Branch

from django import forms
from django.forms import ModelForm, Textarea


class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ('creator', 'coverimg', 'title', 'genre', 'synopsis', )
        widgets = {
            'creator': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'placeholder': '제목'}),
            'synopsis': forms.Textarea(attrs={'placeholder': '줄거리'}),
        }

class BranchCreationForm(ModelForm):
    class Meta:
        model = Branch
        fields = ('book', 'title', 'author', 'contents', 'parent_branch',)
        widgets = {
            'book': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            'parent_branch': forms.HiddenInput(),
            
            'title': forms.TextInput(attrs={'placeholder': '제목'}),
            'contents': forms.Textarea(attrs={'placeholder': '내용'}),
        }        