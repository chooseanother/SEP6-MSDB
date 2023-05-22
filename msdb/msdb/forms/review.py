from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ReviewForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form action to current page
        # self.helper.form_action = reverse_lazy("movie", kwargs=dict(movie_id=self.movie_id))

        # add submit button
        self.helper.add_input(Submit("submit", "Submit"))

    rating = forms.IntegerField(min_value=1, max_value=5)
    text = forms.CharField(widget=forms.Textarea, required=False)