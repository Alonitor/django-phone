from django.views import generic
from .models import Contact
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/admin'
    redirect_field_name = 'redirect_to'
    template_name = 'contacts/index.html'
    context_object_name = 'contact_list'

    def get_queryset(self):
        return Contact.objects.order_by('-sync')[:100]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Contact
    template_name = 'contacts/detail.html'
