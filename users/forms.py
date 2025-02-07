from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from events.forms import StyledFormMixin 
from django.core.exceptions import ValidationError

class CustomRegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User 
        fields = ["username", 'first_name', 'last_name', "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', "password2"]:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")
        return email