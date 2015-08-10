from django import forms
from .models import URLExp

class SubmitForm(forms.ModelForm):
	class Meta:
		model = URLExp
		fields = ('shorturl',)
