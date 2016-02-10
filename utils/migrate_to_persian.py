from django.db import models
from django.db.transaction import atomic
from django.apps import apps

from utils.persian import arToPersianChar

__author__ = 'M.Y'


@atomic
def migrate():
    migrate_models = apps.get_models()

    for model in migrate_models:

        if model.__name__ in ['Related', 'TestFieldsModel', 'EmptyModel']:
            continue

        char_fields = []

        for field in model._meta.get_all_field_names():
            model_field = model._meta.get_field(field)
            if isinstance(model_field, (models.CharField, models.TextField)) and \
                    not isinstance(model_field, models.URLField) and field != 'password':
                char_fields.append(field)

        print(model)
        print(char_fields)

        for obj in model.objects.all():
            for field in char_fields:
                old_val = getattr(obj, field)
                if old_val:
                    setattr(obj, field, arToPersianChar(old_val))
            obj.save()
