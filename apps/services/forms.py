from django import forms
from services.models import ReadingList
from events.models import Bundle

class ShareForm(forms.Form):
    sender = forms.EmailField()
    receiver = forms.EmailField()
    description = forms.CharField(
        required=False,
        widget=forms.Textarea
        )

class ReadingsListForm(forms.ModelForm):
    bundles = forms.ModelMultipleChoiceField(
        queryset = Bundle.published.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )
    class Meta:
        model = ReadingList
        fields = ["title","tags","bundles"]