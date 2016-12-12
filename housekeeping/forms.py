from django import forms

from core.models import PATHWAY_DATABASE, PATHWAY_ORGANISM


class UpdatePathwayForm(forms.Form):

    filename = forms.FileField(label='File')
    database = forms.ChoiceField(
        label='Database',
        choices=PATHWAY_DATABASE,
    )
    organism = forms.ChoiceField(
        label='Organism',
        choices=PATHWAY_ORGANISM,
    )

    def __init__(self, *args, **kwargs):
        super(UpdatePathwayForm, self).__init__(*args, **kwargs)

        attrs = {'class' : 'form-control'}
        self.fields['filename'].widget.attrs.update(attrs)
        self.fields['database'].widget.attrs.update(attrs)
        self.fields['organism'].widget.attrs.update(attrs)
