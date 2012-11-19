# -*- coding: utf-8 -*-
from models import UserComment, UserProfile

from django import forms
from django.forms import ModelForm, Textarea

class UserCommentForm(ModelForm):
    class Meta:
        model = UserComment
        fields = ('user', 'writer', 'text',)
        widgets = {
            'user': forms.HiddenInput(),
            'writer': forms.HiddenInput(),

            'text' : forms.Textarea(attrs={'placeholder': '댓글을 입력하세요.'})
        }

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('user', 'message', 'profileimg')
		widgets = {
			'user': forms.HiddenInput(),

			'message': forms.Textarea(attrs={ 'placeholder': "메시지를 입력하세요 (140자 제한)", 'rows':2, 'wrap': "hard" }),
		}