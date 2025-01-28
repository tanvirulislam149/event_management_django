from django.forms import ModelForm 
from events.models import Event, Participant, Category
from django.forms import widgets
from django import forms

class StyledFormMixin:

    default_styles = "border border-gray-400 w-full mb-2 px-2 py-1 text-lg rounded-md"
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
                    "row": 3
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.default_styles, 
                    "placeholder": f"Enter {field.label.lower()}"
                })
            # elif isinstance(field.widget, forms.CheckboxSelectMultiple):
            #     field.widget.attrs.update({
            #         "class": self.default_styles, 
            #         "placeholder": f"Enter {field.label.lower()}"
            #     })

class EventModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "location"]
        widgets = {
            "name": widgets.TextInput(),
            "description": widgets.Textarea(),
            "location": widgets.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CategoryModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()