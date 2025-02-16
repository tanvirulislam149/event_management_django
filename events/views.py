from django.shortcuts import render
from events.forms import EventModelForm, CategoryModelForm
from django.shortcuts import redirect
from django.contrib import messages
from events.models import Event, Category
from django.db.models import Count
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


# Create your views here.


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer_or_admin(user):
    return user.groups.filter(name="Organizer").exists() or user.groups.filter(name="Admin").exists()

def is_user(user):
    return user.groups.filter(name="User").exists()


@login_required
# @user_passes_test(is_organizer_or_admin)
def dashboard(request):
    if is_user(request.user):
        users = User.objects.prefetch_related("confirmed_events").get(id = request.user.id)
        context = {
            "is_user": True,
            "users": users
        }
        return render(request, "user_dashboard.html", context)

    base_query = Event.objects.select_related("category").annotate(confirmed_participants_count=Count("confirm_participants"))
    events = base_query.all()

    event_count = Event.objects.aggregate(
        events=Count("id"),
        upcoming = Count("id", filter=Q(date__gt = datetime.now().date())),
        past = Count("id", filter=Q(date__lt = datetime.now().date())),
        todays_count = Count("id", filter=Q(date = datetime.now().date()))
    )
    participant_count = User.objects.all().count()
    # category_count = Category.objects.all().count()
    todays_events = Event.objects.filter(date= datetime.now().date())
    
    upcoming = request.GET.get("upcoming")
    past = request.GET.get("past")
    if upcoming:
        events = base_query.filter(date__gt = datetime.now().date())
        print(events)
    elif past:
        events = base_query.filter(date__lt = datetime.now().date())
    else:
        events = base_query.all()
    
    context = {
        "events": events,
        "event_count": event_count,
        "participant_count": participant_count,
        # "category_count": category_count,
        "todays_events": todays_events,
        "is_admin": is_admin(request.user),
        "is_organizer": is_organizer_or_admin(request.user),
    }
    return render(request, "event_table.html", context)


show_participant_decorator = [login_required, user_passes_test(is_admin, "no_permission")]
@method_decorator(show_participant_decorator, name="dispatch")
class Show_participants(TemplateView):
    template_name = "participants.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participants = User.objects.all()
        context["participants"] = participants
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(context)
        return render(request, self.template_name, context)

show_category_decorator = [login_required, user_passes_test(is_organizer_or_admin, "no_permission")]
@method_decorator(show_category_decorator, name="dispatch")
class Show_category(ListView):
    model = Category
    template_name = "category.html"
    queryset = Category.objects.all()
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context


def details(request, id):
    event = Event.objects.select_related("category").prefetch_related("participants").get(id = id)
    context = {
        "event": event
    }
    return render(request, "details.html", context)

create_event_decorator = [login_required, user_passes_test(is_organizer_or_admin, "no_permission")]
@method_decorator(create_event_decorator, name="dispatch")
class Create_event(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = "create_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "create"
        context["pageId"] = self.kwargs.get("pageId")
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event saved successfully.")
        return redirect("create_event", self.kwargs.get("pageId"))
        

create_category_decorator = [login_required, user_passes_test(is_organizer_or_admin, "no_permission")]
@method_decorator(create_category_decorator, name="dispatch")
class Create_category(CreateView):
    model = Category 
    form_class = CategoryModelForm 
    template_name = "create_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "create"
        context["pageId"] = self.kwargs.get("pageId")
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        cat_form = CategoryModelForm(request.POST, request.FILES)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, "Category saved successfully.")
        return redirect("create_category", self.kwargs.get("pageId"))

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def update_event(request, pageId, eventId):
    event = None
    if(request.method == "POST"):
        if pageId == 1:  # 
            event = Event.objects.get(id = eventId)
            event_form = EventModelForm(request.POST, request.FILES, instance = event)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event saved successfully.")

        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            event_form = CategoryModelForm(request.POST, instance = event)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category updated successfully.")

        return redirect("update_event", pageId = pageId, eventId = eventId)
        
    else :
        if pageId == 1:  # 
            event = Event.objects.get(id = eventId)
            
        elif pageId == 2:
            event = User.objects.get(id = eventId)
            
        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            
        
        event_form = EventModelForm(instance = event)
        cat_form = CategoryModelForm(instance = event)
        context = {
            "type": "update",
            "form": event_form if pageId == 1 else cat_form,
            "pageId": pageId,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "create_event.html", context)
        

delete_event_decorator = [login_required, user_passes_test(is_organizer_or_admin, "no_permission")]
@method_decorator(delete_event_decorator, name="dispatch")
class Delete_event(DeleteView):
    model = Event
    pk_url_kwarg = 'id' 
    success_url = reverse_lazy("dashboard")

@login_required
@user_passes_test(is_admin, "no_permission")
def delete_participants(request, id):
    if request.method == "POST":
        event = User.objects.get(id = id)
        event.delete()
        messages.success(request, "Participant deleted")
        return redirect('show_participants')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_participants')

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def delete_category(request, id):
    if request.method == "POST":
        event = Category.objects.get(id = id)
        event.delete()
        messages.success(request, "Category deleted")
        return redirect('show_category')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_category')
    

@login_required
def accept_invitation(request, event_id):
    event = Event.objects.get(id = event_id)
    if event.confirm_participants.filter(id = request.user.id).exists():
        return redirect("no_permission")
    else:
        event.confirm_participants.add(request.user)
        return redirect("dashboard")