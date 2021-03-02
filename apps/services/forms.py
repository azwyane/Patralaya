'''
PATRALAYA - A Web Application for research article publishing and article aggregation.
    Copyright (C) 2020 Shrawan Baral, Sandesh Sharma

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

   contact at: debianbyte@gmail.com, sandesh0806@gmail.com
   Patralaya Copyright (C) 2020 Shrawan Baral, Sandesh Sharma
'''

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