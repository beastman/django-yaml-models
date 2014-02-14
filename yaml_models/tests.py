# -*- coding: utf-8 -*-
from django.test import TestCase
from yaml_models import models_from_yaml
import os
from django.db import models
from django.utils.importlib import import_module

TEST_YAML_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.yaml')

class YamlModelsTest(TestCase):
    def setUp(self):
        models_from_yaml(TEST_YAML_PATH, 'yaml_models', 'yaml_models.models')
    def test_yaml_models(self):
        models_list = models.get_models(app_mod=import_module('smyt_test.models'))
        self.assertEqual(models_list[0].__name__,'Users')
        self.assertEquals(models_list[0]._meta.verbose_name, u'Пользователи')
        self.assertIsInstance(models_list[0]._meta._fields()[1], models.CharField)
        self.assertEqual(models_list[1].__name__,'Rooms')
        self.assertEquals(models_list[1]._meta.verbose_name, u'Комнаты')
        self.assertIsInstance(models_list[1]._meta._fields()[1], models.CharField)
