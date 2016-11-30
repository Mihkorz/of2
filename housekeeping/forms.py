from django import forms


class UpdatePathwayForm(forms.Form):

    filename = forms.CharField(label='File', max_length=255)
    database = forms.CharField(label='Database', max_length=255)
    organism = forms.CharField(label='Organism', max_length=255)
