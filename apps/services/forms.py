from django import forms

class ShareForm(forms.Form):
    sender = forms.EmailField()
    receiver = forms.EmailField()
    description = forms.CharField(
        required=False,
        widget=forms.Textarea
        )