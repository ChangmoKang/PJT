from django import forms
from .models import Score

class ScoreModelForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['comment', 'score']