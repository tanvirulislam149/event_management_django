from django.forms import ModelForm 
from events.models import Event, Participant, Category
from django.forms import widgets
from django import forms

class StyledFormMixin:

    default_styles = "border border-gray-400 w-full mb-3 mt-1 px-2 py-2 text-lg"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": f"{self.default_styles} resize-none",
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 4
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    "class": f"{self.default_styles} resize-none",
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 4
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    # "placeholder": f"Enter {field.label.lower()}"
                    "placeholder": "04:05 am"
                })

class EventModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "location", "category", "date", "time"]
        widgets = {
            "name": widgets.TextInput(),
            "description": widgets.Textarea(),
            "location": widgets.TextInput(),
            "category": widgets.Select(),
            "date": widgets.SelectDateWidget(),
            "time": widgets.TimeInput(attrs={'type': 'time'})
        }



class ParticipantsModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Participant
        # fields = ["name", "email"]
        fields = "__all__"
        widgets = {
            "name": widgets.TextInput(),
            "email": widgets.EmailInput(),
            "events": widgets.CheckboxSelectMultiple()
        }
        

class CategoryModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
