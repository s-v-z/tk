import logging
from itertools import groupby
from datetime import datetime
from functools import lru_cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from apps.tk_database.models import Hike, HikeReport, UserProfile, CalendarEvent
from apps.tk_database.forms import HikeForm, HikeReportForm, DeleteConfirmationForm


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


# @lru_cache(maxsize=2048) TODO: enable later
def hikes_list(request):
    # TODO: add pagination, add query filters
    hikes = Hike.objects.order_by('category','start_date').select_related('leader').all()

    context = {
        'grouped_hikes': ((key, list(group)) for key, group in groupby(hikes, lambda hike: hike.category))
    }
    return render(request, 'hikes/list.html', context)


def hike_show(request, hike_id):
    hike = Hike.objects.select_related("region", "type").get(pk=hike_id)
    report = HikeReport.objects.filter(hike_id=hike_id)
    leader = UserProfile.objects.select_related("user").get(user__id = hike.leader_id)

    log.debug('leader: %s', leader)
    context = {
        'hike': hike,
        'report': report,
        'leader': leader
    }
    return render(request, 'hikes/show.html', context)

# TODO: use Ninja REST
def hike_close(request, hike_id):
    hike = Hike.objects.select_related("region", "type").get(pk=hike_id)

    if hike.leader_id != request.user.id:
        raise PermissionDenied('Нельзя изменить чужой поход')

    hike.is_completed = True
    hike.save()
    return redirect(reverse('hike_show', kwargs={'hike_id' : hike_id}))


class CreateHikeView(CreateView):
    model = Hike
    form_class = HikeForm
    template_name='hikes/new.html'

    def form_valid(self, form):
        form.instance.leader = self.request.user
        return super(CreateHikeView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateHikeView, self).get_form_kwargs()
        kwargs['action'] = 'new'
        kwargs['leader'] = self.request.user
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
    reports = HikeReport.objects.order_by('actual_start_date').select_related('hike').all()

    context = {
        'reports': reports
    }
    return render(request, 'reports/list.html', context)


def report_show(request, hike_id):
    report = HikeReport.objects.filter(hike_id=hike_id).select_related("hike").first()
    hike = report.hike
    leader = UserProfile.objects.select_related("user").get(user__id = report.hike.leader_id)

    log.debug('leader: %s', leader)
    context = {
        'report': report,
        'hike': hike,
        'leader': leader
    }
    return render(request, 'reports/show.html', context)

def report_edit(request, hike_id):
    return render(request, 'reports/edit.html')

def report_delete(request, hike_id):
    return render(request, 'reports/delete.html')

class CreateReportView(CreateView):
    model = Hike
    form_class = HikeReportForm
    template_name='reports/new.html'

    def get_form_kwargs(self):
        kwargs = super(CreateReportView, self).get_form_kwargs()
        # kwargs['action'] = 'new'
        kwargs['submit_label'] = 'Добавить отчёт'
        return kwargs

    def get_success_url(self):
        return reverse('report_show', kwargs={'hike_id' : self.object.hike_id})


# --------- EVENTS -----------
def events_list(request):    
    return render(request, 'events/list.html')

# --------- HOME -----------

def tk_home(request):
    hikes_total_count = Hike.objects.count()
    hikes_open_count = Hike.objects.filter(is_completed=False).count()
    users_count = UserProfile.objects.count()


    context = {
        'stats' : {
            'hikes_total': hikes_total_count,
            'hikes_active': hikes_open_count,
            'users_count': users_count
        },
        'events': []
    }
    return render(request, 'home/index.html', context)


# --------- CALENDAR -----------

# TODO: replace with Ninja API
def events_json(request):
    start_str = request.GET.get('start','')
    end_str = request.GET.get('end','')

    start = datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S%z')
    end = datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S%z')

    events = CalendarEvent.objects.filter(start_dt__gte=start, start_dt__lte=end).all()

    response = []

    for event in events:
        evt = {}
        evt['id']= event.pk
        evt['title'] = event.title
        evt['description'] = event.description
        evt['start'] = event.start_dt
        evt['end'] = event.end_dt
        response.append(evt)

    return JsonResponse(response, safe=False)

def event_json(request, event_id):
    event = CalendarEvent.objects.get(pk=event_id)

    evt = {}
    evt['id']= event.pk
    evt['title'] = event.title
    evt['description'] = event.description
    evt['start'] = event.start_dt
    evt['end'] = event.end_dt    

    return JsonResponse(evt, safe=False)

# TODO: replace with Ninja API
def events_daily_json(request, day):
    evt_date = datetime.strptime(day, '%Y-%m-%d')
    
    events = CalendarEvent.objects.filter(start_dt__gte=evt_date, start_dt__lte=evt_date).all()

    response = []

    for event in events:
        evt = {}
        evt['id']= event.pk
        evt['title'] = event.title
        evt['description'] = event.description
        evt['start'] = event.start_dt
        evt['end'] = event.end_dt
        response.append(evt)

    return JsonResponse(response, safe=False)