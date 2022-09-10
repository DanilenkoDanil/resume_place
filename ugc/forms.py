from django import forms

from .models import Profile, Service


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name'
        )
        widgets = {
            'name': forms.TextInput,
        }


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = (
            'platform',
            'type',
            'service',
            'product_id',
            'price',
            'min_count',
            'max_count',
            'link_form'

        )
        widgets = {
            'platform': forms.TextInput,
            'type': forms.TextInput,
            'service': forms.TextInput,
            'product_id': forms.TextInput
        }
