from django import forms


class UpdatePathwayForm(forms.Form):

    pathway = forms.CharField(label='Pathway', max_length=255)
