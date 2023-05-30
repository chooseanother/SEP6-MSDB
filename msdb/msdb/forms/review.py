from django import forms

from msdb.models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False
        # change rating to radio widget
        self.fields["rating"].widget = forms.RadioSelect(choices=Review.RATING_CHOICES)
        # add placeholder text "optional" to text field
        self.fields["text"].widget.attrs["placeholder"] = "Optional"

    class Meta:
        model = Review
        fields = ["rating", "text"]
