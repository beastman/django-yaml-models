# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
import yaml
from yaml_models.models import YamlModel
from django.db import models
from django.contrib import admin as django_admin

FIELD_TYPE_MAPPING = {
    'char': {'class': models.CharField, 'initial_kwargs': {'max_length':255}},
    'int': {'class': models.IntegerField, 'initial_kwargs': {}},
    'date': {'class': models.DateField, 'initial_kwargs': {}},
}

def dict_to_model_class(app_name, class_name, model_dict):
    """Преобразует словарь полученный из YAML файла в класс модели"""
    class Meta:
        pass
    Meta.verbose_name = model_dict['title']
    Meta.verbose_name_plural = model_dict['title']
    Meta.app_label = app_name
    fields = {}
    fields['__module__'] = app_name
    fields['Meta'] = Meta
    for row in model_dict['fields']:
        field_info = FIELD_TYPE_MAPPING[row['type']]
        kwargs = field_info['initial_kwargs']
        kwargs['verbose_name'] = row['title']
        fields[row['id']] = field_info['class'](**kwargs)
    result = type(class_name, (YamlModel,), fields)
    return result



def models_from_yaml(yaml_path, app_name, models_module, admin_register=True):
    models_module = import_module(models_module)
    models_data = yaml.load(open(yaml_path))
    result = []
    for key in models_data.keys():
        class_name = key.lower().capitalize()
        model_class = dict_to_model_class(app_name, class_name, models_data[key])
        setattr(models_module, class_name, model_class)
        if admin_register:
            django_admin.site.register(getattr(models_module, class_name))