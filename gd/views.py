#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import MV, Mv_records
from django.db.models import Count
from django.core.serializers import serialize


def home(request):
    """
    home view
    """
    partypercent = MV.objects.values('party').annotate(dcount=Count('party'))
    return render_to_response('index.html', {'partypercent': partypercent}, context_instance=RequestContext(request))


def home_maintenance(request):
    """
    view for maintenance mode
    """
    mNote = 'Şu anda ek geliştirmeler yapılmaktadır.'
    return render_to_response('index.html', {'mnote': mNote}, context_instance=RequestContext(request))


def detail(request):
    mvdata = MV.objects.all()
    return render_to_response('detail.html', {'mvdata': mvdata}, context_instance=RequestContext(request))


def getmvdata(request, mvnum):
    """
    :param request:
    :param mvnum: mv_id
    :return: json data
    """
    numbersof = Mv_records.objects.filter(mv=mvnum).order_by('-date')
    mvx = serialize('json', numbersof)
    return HttpResponse(mvx, mimetype='application/json')


def mvnames(request):
    allnames = MV.objects.defer('mv_id', 'name')
    all_names = serialize('json', allnames, fields=('mv_id', 'name'))
    return HttpResponse(all_names, mimetype='application/json')