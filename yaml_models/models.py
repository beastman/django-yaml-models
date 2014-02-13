# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class YamlModel(models.Model):
    def __unicode__(self):
        fields = self._meta.get_all_field_names()
        #TODO: СДелать проход по списку полей с поиском названий, которые можно использовать для вывода,
        #вместо первого попавшегося (title, display_value, etc)
        return unicode(getattr(self, fields[0]))
    class Meta:
        abstract = True