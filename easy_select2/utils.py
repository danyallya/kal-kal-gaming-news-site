# coding: utf-8

from django.db.models import ForeignKey
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from multiselectfield.db.fields import MultiSelectField

from easy_select2.widgets import Select2Mixin, Select2, Select2Multiple
from easy_select2 import forms as es2_forms


# TODO: merge meta_fields and kwargs, which is the same.
def select2_modelform_meta(model,
                           meta_fields=None,
                           widgets=None,
                           attrs=None,
                           **kwargs):
    """
    Return `Meta` class with Select2-enabled widgets for fields
    with choices (e.g.  ForeignKey, CharField, etc) for use with
    ModelForm.

    Arguments:
        model - a model class to create `Meta` class for.
        meta_fields - dictionary with `Meta` class fields, for
            example, {'fields': ['id', 'name']}
        attrs - select2 widget attributes (width, for example),
            must be of type `dict`.
        **kwargs - will be merged with meta_fields.
    """
    widgets = widgets or {}
    meta_fields = meta_fields or {}

    # TODO: assert attrs is of type `dict`

    for field in model._meta.fields:
        if (isinstance(field, ForeignKey) or field.choices) and not isinstance(field, MultiSelectField):
            widgets.update({field.name: Select2(select2attrs=attrs)})
        elif isinstance(field, MultiSelectField):
            widgets.update({field.name: Select2Multiple(select2attrs=attrs)})

    for field in model._meta.many_to_many:
        widgets.update({field.name: Select2Multiple(select2attrs=attrs)})
        # TODO: move this hackish bugfix to another mixin
        msg = _('Hold down "Control", or "Command" on a Mac, '
                'to select more than one.')
        field.help_text = field.help_text.replace(force_text(msg), '')

    meta_fields.update({
        'model': model,
        'widgets': widgets,
    })
    if 'exclude' not in kwargs and 'fields' not in kwargs:
        meta_fields.update({'exclude': []})
    meta_fields.update(**kwargs)
    meta = type('Meta', (object,), meta_fields)

    return meta

# select2_meta_factory is deprecated name
select2_meta_factory = select2_modelform_meta


# TODO: make FixedModelForm default form_class
def select2_modelform(model, attrs=None,
                      form_class=es2_forms.FixedModelForm):
    """
    Return ModelForm class for model with select2 widgets.

    Arguments:
        attrs: select2 widget attributes (width, for example) of type `dict`.
        form_class: modelform base class, `forms.ModelForm` by default.

    ::

        SomeModelForm = select2_modelform(models.SomeModelBanner)

    is the same like::

        class SomeModelForm(forms.ModelForm):
            Meta = select2_modelform_meta(models.SomeModelForm)
    """
    classname = '%sForm' % model._meta.object_name
    meta = select2_modelform_meta(model, attrs=attrs)
    return type(classname, (form_class,), {'Meta': meta})


def apply_select2(widget_cls):
    """
    Dynamically create new widget class mixed with Select2Mixin.

    Args:
        widget_cls: class of source widget.

    Usage, for example::

        class SomeModelForm(admin.ModelForm):
            class Meta:
                widgets = {
                    'field': apply_select2(forms.Select),
                }

    So, `apply_select2(forms.Select)` will return new class,
    named Select2Select.
    """
    cname = 'Select2%s' % widget_cls.__name__
    return type(cname, (Select2Mixin, widget_cls), {})
