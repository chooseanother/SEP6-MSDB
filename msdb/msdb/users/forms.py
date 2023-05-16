from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import EmailField, CharField, TextInput, ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    name = CharField(
        max_length=255,
        label="Display name",
        widget=TextInput(
            attrs={
                "placeholder": _("Display name"),
                "autocomplete": "name",
                "autofocus": True,
            }
        ),
    )

    field_order = [
        "name",
        "email",
        "password1",
        "password2",
    ]
    
    def save(self, request):
        """
        Saves the user to the database.
        """
        user = super(UserSignupForm, self).save(request)
        user.name = self.cleaned_data.get("name")
        user.save()
        return user
    
    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if User.objects.filter(name=name).exists():
            raise ValidationError(_("This name has already been taken."))

        return name
    


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
