from django import forms
from django.contrib.auth.models import User
from .models import Link, Vote, UserProfile, Comment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude =("user",)

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ("submitter", "rank_score")

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)