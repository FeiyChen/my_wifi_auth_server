from django import forms

class PwdForm(forms.Form):
	passwd = forms.FloatField()
	image = forms.FileField()