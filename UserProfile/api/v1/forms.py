from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=32
    )
