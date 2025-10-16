from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .constants import DESIGNATION_CHOICES, gender_choices
from .models import Session, UserProfile
from PIL import Image
import io
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={"placeholder": "Enter Captcha", "class": "form-control"}
        )
    )


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"id": "required"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"id": "required"}))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"id": "required", "placeholder": "example@gmail.com"}
        )
    )
    # username = forms.CharField(widget=forms.TextInput(attrs={"id": "required"}))
    gender = forms.ChoiceField(
        choices=[("", "Select Gender")] + gender_choices,
        label="Gender",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    designation = forms.ChoiceField(
        choices=[("", "Select Designation")] + DESIGNATION_CHOICES,
        label="Designation",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    session = forms.ModelChoiceField(
        widget=forms.Select(attrs={"id": "required"}),
        queryset=Session.objects.all(),
        empty_label="Select Session",
    )
    facebook_profile = forms.URLField(
        widget=forms.URLInput(
            attrs={"placeholder": "https://facebook.com/yourprofile"}
        ),
        required=False,
        label="Facebook Profile",
    )
    linkedin_profile = forms.URLField(
        widget=forms.URLInput(
            attrs={"placeholder": "https://linkedin.com/in/yourprofile"}
        ),
        required=False,
        label="LinkedIn Profile",
    )
    profile_picture = forms.ImageField(required=False)
    captcha = CaptchaField(
        widget=CaptchaTextInput(
            attrs={
                "placeholder": "Enter Captcha",
                "id": "required",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "gender",
            "designation",
            "session",
            "facebook_profile",
            "linkedin_profile",
            "profile_picture",
            "password1",
            "password2",
            "captcha",
        ]

    def clean_profile_picture(self):
        pic = self.cleaned_data.get("profile_picture")

        if pic:
            if pic.size > 200 * 1024:
                raise forms.ValidationError("Profile picture must be less than 200KB.")
            img = Image.open(pic)
            width, height = img.size
            if width != height:
                raise forms.ValidationError(
                    "Profile picture must be square (1:1 ratio)."
                )
            # except Exception:
            #     raise forms.ValidationError("Invalid image file.")

        return pic

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
            gender = self.cleaned_data.get("gender")
            designation = self.cleaned_data.get("designation")
            session = self.cleaned_data.get("session")
            facebook_profile = self.cleaned_data.get("facebook_profile")
            linkedin_profile = self.cleaned_data.get("linkedin_profile")
            profile_picture = self.cleaned_data.get("profile_picture")

            UserProfile.objects.create(
                user=user,
                gender=gender,
                designation=designation,
                session=session,
                facebook_profile=facebook_profile,
                linkedin_profile=linkedin_profile,
                profile_picture=profile_picture,
            )
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "id": "required"}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "id": "required"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "id": "required"})
    )
    facebook_profile = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://facebook.com/yourname"}),
    )
    linkedin_profile = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={"placeholder": "https://linkedin.com/in/yourname"}
        ),
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                user_profile = self.instance.profile  # Better than .profile
            except UserProfile.DoesNotExist:
                user_profile = None

            if user_profile:
                self.fields["facebook_profile"].initial = user_profile.facebook_profile
                self.fields["linkedin_profile"].initial = user_profile.linkedin_profile
                self.fields["profile_picture"].initial = user_profile.profile_picture

    def clean_profile_picture(self):
        pic = self.cleaned_data.get("profile_picture")

        if pic:
            if pic.size > 200 * 1024:
                raise forms.ValidationError("Profile picture must be less than 200KB.")

            try:
                img = Image.open(pic)
                width, height = img.size
                if width != height:
                    raise forms.ValidationError(
                        "Profile picture must be square (1:1 ratio)."
                    )
            except Exception:
                raise forms.ValidationError("Invalid image file.")

        return pic

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.facebook_profile = self.cleaned_data.get("facebook_profile")
        user_profile.linkedin_profile = self.cleaned_data.get("linkedin_profile")

        pic = self.cleaned_data.get("profile_picture")
        if pic:
            user_profile.profile_picture = pic

        if commit:
            user_profile.save()

        return user


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["year"]
