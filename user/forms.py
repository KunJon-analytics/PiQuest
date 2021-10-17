import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .models import Profile
from .utils import ActivationMailFormMixin

import pywaves as pw


logger = logging.getLogger(__name__)


class ResendActivationEmailForm(ActivationMailFormMixin, forms.Form):

    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except:
            logger.warning(
                'Resend Activation: No user with '
                'email: {} .'.format(
                    self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user


class UserCreationForm(ActivationMailFormMixin, BaseUserCreationForm):

    name = forms.CharField(max_length=255, help_text=(
        "The name displayed on your "
        "public profile."))

    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)')

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('name', 'email')

    def clean_name(self):
        name = self.cleaned_data['name']
        disallowed = ('activate', 'create', 'disable', 'login',
                      'logout', 'password', 'profile',)
        if name in disallowed:
            raise ValidationError(
                "A user with that name"
                " already exists.")
        return name

    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        Profile.objects.update_or_create(user=user, defaults={
            'name': self.cleaned_data['name'],
            'slug': slugify(self.cleaned_data['name']), })
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('name', 'wallet_address', 'telegram_id', 'about', 'image')

    def clean_name(self):
        name = self.cleaned_data['name']
        disallowed = ('activate', 'create', 'disable', 'login',
                      'logout', 'password', 'profile',)
        if name in disallowed:
            raise ValidationError(
                "A user with that name"
                " already exists.")
        return name

    def clean_wallet_address(self):
        wallet_address = self.cleaned_data['wallet_address']
        if pw.validateAddress(wallet_address) != True:
            raise ValidationError(
                _('%(wallet_address)s is not a valid Waves address'),
                params={'wallet_address': wallet_address},
            )
        return wallet_address


class CampusAmbassadorForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), max_length=100)
    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)