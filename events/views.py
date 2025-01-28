from django.shortcuts import render
from events.forms import EventModelForm, ParticipantsModelForm, CategoryModelForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def dashboard(request):
    return render(request, "dashboard.html")

def create_event(request, id):
    if(request.method == "POST"):
        if id == 1:
            event_form = EventModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event saved successfully.")
            
        elif id == 2:
            event_form = ParticipantsModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Participant created successfully.")

        elif id == 3:
            event_form = CategoryModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category created successfully.")

        return redirect("create_event", id)
        
    else :
        event_form = EventModelForm(request.GET)
        Participant_form = ParticipantsModelForm(request.GET)
        cat_form = CategoryModelForm(request.GET)
        context = {
            "form": event_form if id == 1 else Participant_form if id == 2 else cat_form,
            "id": id
        }
        return render(request, "create_event.html", context)
        
