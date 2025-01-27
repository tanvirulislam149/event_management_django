from django.shortcuts import render
from events.forms import EventModelForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def dashboard(request):
    return render(request, "dashboard.html")

def create_event(request):
    if(request.method == "POST"):
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()

        messages.success(request, "Event saved successfully.")
        return redirect("create_event")
    else :
        event_form = EventModelForm(request.GET)
        context = {
            "form": event_form
        }
        return render(request, "create_event.html", context)
        
