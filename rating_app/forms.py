from django import forms

from rating_app.models import Movie


class CreationForm(forms.ModelForm):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': "form-field",
                                                                                    'placeholder': "Title"}))

    rating = forms.IntegerField(label='', widget=forms.TextInput(attrs={'class': "rating-field",
                                                                        'type': 'range',
                                                                        'min': '0',
                                                                        'max': '10',
                                                                        'step': '0.5',
                                                                        'value': '0'}))

    class Meta:
        model = Movie
        fields = ['title', 'rating']
