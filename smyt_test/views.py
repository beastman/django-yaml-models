from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.importlib import import_module
from django.http import Http404, HttpResponse
from django.db import models
import json
from collections import OrderedDict
from django.middleware.csrf import get_token
from django.forms.models import modelform_factory
from django.utils.html import escape


def home(request):
    context = RequestContext(request)
    registered_models = models.get_models(app_mod=import_module('smyt_test.models'))
    models_list = []
    for model in registered_models:
        models_list.append({
            'verbose_name': model._meta.verbose_name_plural,
            'class_name': model.__name__
        })
    context['models_list'] = models_list
    return render_to_response('home.html', context)


def load_model_data(request):
    from smyt_test import models as main_app_models
    model_class_name = request.GET.get('model_class')
    if not model_class_name or not hasattr(main_app_models, model_class_name):
        raise Http404
    response = {}
    model_class = getattr(main_app_models, model_class_name)
    response['title'] = model_class._meta.verbose_name
    columns = OrderedDict()
    model_fields = model_class._meta._fields()
    for field in model_fields:
        columns[field.name] = {}
        if field.name == model_class._meta.pk.name:
            columns[field.name]['type'] = 'pk'
        elif type(field) is models.CharField:
            columns[field.name]['type'] = 'str'
        elif type(field) is models.IntegerField:
            columns[field.name]['type'] = 'int'
        elif type(field) is models.DateField:
            columns[field.name]['type'] = 'date'
        columns[field.name]['title'] = field.verbose_name
    response['columns'] = columns
    rows = []
    for row in model_class.objects.all():
        r = {}
        for field_name in columns.keys():
            r[field_name] = escape(unicode(getattr(row, field_name)))
        rows.append(r)
    response['rows'] = rows
    response['csrf_token'] = get_token(request)
    response['model_class'] = model_class_name
    response['success'] = True
    return HttpResponse(json.dumps(response))


def add_record(request):
    from smyt_test import models as main_app_models
    model_class_name = request.POST.get('model')
    if not model_class_name or not hasattr(main_app_models, model_class_name):
        raise Http404
    model_class = getattr(main_app_models, model_class_name)
    model_form = modelform_factory(model_class)
    form = model_form(request.POST)
    response = {}
    if form.is_valid():
        form.instance.save()
        response['success'] = True
    else:
        response['success'] = False
        response['errors'] = []
        for field in form:
            for error in field.errors:
                response['errors'].append(u'{0} - {1}'.format(field.label, error))
    return HttpResponse(json.dumps(response))