from django.shortcuts import render, redirect
from django.urls import reverse
from apps.tk_database.models import Hike
from apps.tk_database.forms import HikeForm
from django.contrib.auth.models import User
from itertools import groupby
import logging

log = logging.getLogger(__name__)


def hike_index(request):
    # TODO: add pagination, add query filters
    hikes = Hike.objects.order_by('category','start_date').select_related('leader').all()

    context = {
        'grouped_hikes': ((key, list(group)) for key, group in groupby(hikes, lambda hike: hike.category))
    }
    return render(request, 'hikes_index.html', context)


def hike_detail(request, pk):
    hike = Hike.objects.select_related("region", "type").get(pk=pk)
    leader = User.objects.select_related("profile").get(pk=hike.leader_id)

    log.debug('leader: ' + str(leader))
    context = {
        'hike': hike,
        'leader': leader
    }
    return render(request, 'hike_detail.html', context)

def hike_edit(request, pk):
    hike = Hike.objects.select_related("region", "type").get(pk=pk)
    leader = User.objects.select_related("profile").get(pk=hike.leader_id)

    log.debug('leader: ' + str(leader))
    context = {
        'hike': hike,
        'leader': leader
    }
    return render(request, 'hike_edit.html', context)

def hike_new(request):
    if request.method == "GET":
        return render(
                request, "hike_new.html",
                {"form": HikeForm}
            )
    elif request.method == "POST":
        form = HikeForm(request.POST)
        if form.is_valid():
            hike = form.save()        
            return redirect(reverse("hike_detail", kwargs={'pk':hike.pk}))