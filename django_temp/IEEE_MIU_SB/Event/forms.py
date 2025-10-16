from django import forms
from .models import Event
class EventForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'id': 'required', 'placeholder': 'Event Title'}),
    )
    location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'required', 'placeholder': 'Event Location'}),
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'required', 'placeholder': 'Event Summary max 200 characters','rows': 3, 'maxlength': 200}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Event
        exclude = ['slug']
