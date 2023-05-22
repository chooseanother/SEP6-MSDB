from django import forms
from msdb.models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, ButtonHolder, HTML, Div, Button
from crispy_forms.bootstrap import InlineField, FormActions, InlineRadios

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False
        # change rating to radio widget
        self.fields["rating"].widget = forms.RadioSelect(choices=Review.RATING_CHOICES)
        # add placeholder text "optional" to text field
        self.fields["text"].widget.attrs["placeholder"] = "Optional"
        # set the self.helper property:
        self.helper = FormHelper()

        # self.helper.layout = Layout(
        #     Field('rating', css_class="form-check form-check-inline"),
        #     Field("text"),
        # )

    class Meta:
        model = Review
        fields = ["rating", "text"]