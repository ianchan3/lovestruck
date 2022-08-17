from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from .models import Location, Partner, Date
from .forms import DateForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request): 
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class LocationList(ListView):
    model = Location
    fields = ['name', 'category', 'city', 'state']

class LocationCreate(CreateView):
    model = Location
    fields = ['name', 'address', 'phone_num', 'city', 'state', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LocationDetail(DetailView):
    model = Location
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partner_list'] = Partner.objects.filter(user=self.request.user)
        context['date_form'] = DateForm()
        return context

class LocationUpdate(UpdateView):
    model = Location
    fields = ['name', 'address', 'phone_num', 'city', 'state', 'category']

class LocationDelete(DeleteView):
    model = Location
    success_url = '/locations/'

class PartnerList(ListView):
    model = Partner
    fields = ['name']

class PartnerCreate(CreateView):
    model = Partner
    fields = ['name', 'notes']
    success_url = '/partners/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PartnerDetail(DetailView):
    model = Partner
    fields = '__all__'

class PartnerUpdate(UpdateView):
    model = Partner
    fields = '__all__'

class PartnerDelete(DeleteView):
    model = Partner
    success_url = '/partners/'

class DateList(ListView):
    model = Date
    fields = ['location', 'partner']

class DateCreate(CreateView):
    model = Date
    form_class = DateForm

    def form_valid(self, form):
        form.instance.partner_id = self.request.POST.get('partner_id')
        form.instance.location_id = self.request.POST.get('location_id')
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/dates/'

class DateDetail(DetailView):
    model = Date
