# -*- coding: utf-8 -*-
from yaml_models import models_from_yaml
from smyt_test.settings import rel

models_from_yaml(rel('./models.yaml'), 'smyt_test', 'smyt_test.models')