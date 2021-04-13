from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers


class ContactForm(forms.Form):
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    REASON_CHOICES = (
        (FEEDBACK, 'Feedback'),
        (CORRECTION, 'Correction'),
        (SUPPORT, 'Support'),
    )
    reason = forms.ChoiceField(choices=REASON_CHOICES, initial=FEEDBACK)
    email = forms.EmailField(initial='youremail@domain.com')
    your_message = forms.CharField(widget=forms.Textarea)

    def send_mail(self):
        reason = self.cleaned_data.get('reason')
        reason_dict = dict(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data.get('email')
        your_message = self.cleaned_data.get('your_message')
        body = 'Message From: {}\n\n{}\n'.format(email, your_message)
        try:
            # shortcut for send_mail
            mail_managers(full_reason, body)
        except BadHeaderError:
            self.add_error(None,
                ValidationError(
                    'Could Not Send Email.\n'
                    'Extra Headers not allowed '
                    'in email body.',
                    code='badheader'))
            return False
        else:
            return True