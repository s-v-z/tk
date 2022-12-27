import logging
from itertools import groupby
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from apps.tk_database.models import Hike, UserProfile
from apps.tk_database.forms import HikeForm, DeleteConfirmationForm


log = logging.getLogger(__name__)

# TODO: improve view
def user_hikes(request, user_id):
    hikes = Hike.objects.order_by('category','start_date').select_related('leader').filter(Q(leader_id=user_id)) # TODO: filter by hike member

    context = {
        'grouped_hikes': ((key, list(group)) for key, group in groupby(hikes, lambda hike: hike.category))
    }
    return render(request, 'hikes/list.html', context)

# TODO: improve view
def user_announcements(request, user_id):
    hikes = Hike.objects.order_by('category','start_date').select_related('leader').filter(leader_id=user_id)

    context = {
        'grouped_hikes': ((key, list(group)) for key, group in groupby(hikes, lambda hike: hike.category))
    }
    return render(request, 'hikes/list.html', context)


def hikes_list(request):
    # TODO: add pagination, add query filters
    hikes = Hike.objects.order_by('category','start_date').select_related('leader').all()

    context = {
        'grouped_hikes': ((key, list(group)) for key, group in groupby(hikes, lambda hike: hike.category))
    }
    return render(request, 'hikes/list.html', context)


def hike_show(request, hike_id):
    hike = Hike.objects.select_related("region", "type").get(pk=hike_id)
    leader = UserProfile.objects.select_related("user").get(user__id = hike.leader_id)

    log.debug('leader: %s', leader)
    context = {
        'hike': hike,
        'leader': leader
    }
    return render(request, 'hikes/show.html', context)


class CreateHikeView(CreateView):
    model = Hike
    form_class = HikeForm
    template_name='hikes/new.html'

    def get_form_kwargs(self):
        kwargs = super(CreateHikeView, self).get_form_kwargs()
        kwargs['action'] = 'new'
        kwargs['submit_label'] = 'Создать поход'
        return kwargs

    def get_success_url(self):
        return reverse('hike_show', kwargs={'hike_id' : self.object.pk})

class UpdateHikeView(UpdateView):
    model = Hike
    form_class = HikeForm
    template_name='hikes/edit.html'
    pk_url_kwarg = 'hike_id'

    def get_form_kwargs(self):
        kwargs = super(UpdateHikeView, self).get_form_kwargs()
        kwargs['action'] = 'edit'
        kwargs['submit_label'] = 'Сохранить изменения'
        return kwargs

    def get_success_url(self):
        return reverse('hike_show', kwargs={'hike_id' : self.object.pk})

class DeleteHikeView(DeleteView):
    model = Hike
    form_class = DeleteConfirmationForm
    pk_url_kwarg = 'hike_id'
    template_name='hikes/delete.html'

    def form_valid(self, form):
        if self.request.user.id != self.object.leader.id:
            raise PermissionDenied("Вы не можете удалить чужой поход")

        success_url = reverse('hikes_list')
        self.object.is_deleted = True
        self.object.members_set = []
        self.object.save()
        return HttpResponseRedirect(success_url)

# --------- USERS -----------

def users_list(request):
    # TODO: add pagination, add query filters
    profiles = UserProfile.objects.order_by('user__last_name').select_related("user").all

    context = {
        'profiles': profiles
    }
    return render(request, 'users/list.html', context)

def user_show(request, user_id):
    profile = UserProfile.objects.select_related("user").get(user__id = user_id)
    context = {
        'profile': profile
    }
    return render(request, 'users/show.html', context)


# --------- REPORTS -----------

def reports_list(request):
    # TODO: add pagination, add query filters
    profiles = UserProfile.objects.order_by('user__last_name').select_related("user").all
    context = {
        'profiles': profiles
    }
    return render(request, 'reports/list.html', context)

# --------- HOME -----------

def tk_home(request):
    context = {
        'events': []
    }
    return render(request, 'home/index.html', context)
