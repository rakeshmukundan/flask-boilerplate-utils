from flask import render_template_string, Markup
from wtforms.widgets.core import html_params
import wtforms.widgets.core as wt_core


from .Widget import Widget
"""
Widgets for rendering generic form field types.
 - Text Box
 - Text Area
 - Radio Button
 - Checkbox 
"""

# TODO: RenderErrorsForOtherField validator.
# 

class BPWidgetMixin(object):
    pass

class SuffixedTextbox(Widget):
    """Render a textbox with a suffix part"""
    def __init__(self, suffix):
        self.suffix = suffix

    def __call__(self, field, suffix_override=None, **kwargs):
        pass


class PrefixedTextbox(Widget):
    """Render a textbox with a prefix part"""
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, field, prefix_override=None, **kwargs):
        pass


def render_field_errors(field):
    if field.errors:
        html = """<p class="help-block">{{errors}}</p>"""
        return Markup(render_template_string(
            html,
            errors='. '.join(field.errors)
        ))
    return ''

def render_field_description(field):
    if hasattr(field, 'description') and field.description != '':
        html = """<p class="help-block">{{ field.description }}</p>"""
        return Markup(render_template_string(
            html,
            field=field
        ))
    return ''

def render_field_label(field):
    html = """<label for="{{ field.id }}" class="control-label>{{ field.label }}</label>"""
    return Markup(render_template_string(html,
        field=field
    ))

from functools import wraps

def form_group_wrapped(f):
    """
    Wrap a field in a form-group classed group. Additionally, will
    activate bootstrap's has-error class.
    """
    @wraps(f)
    def wrapped_function(self, field, *args, **kwargs):
        html = """<div class="form-group{{ ' has-error' if field.errors }}">
            {{ rendered_field }}
           </div>
        """
        return Markup(render_template_string(
            html,
            field=field,
            rendered_field=f(self, field, *args, **kwargs)
        ))

    return wrapped_function

def add_meta(f):
    @wraps(f)
    def wrapped(self, field, *args, **kwargs):
        html = "{label}{original}{errors}{description}".format(
            label=render_field_label(field),
            original=f(self, field, *args, **kwargs),
            errors=render_field_errors(field),
            description=render_field_description(field)
        )
        return Markup(html)
    return wrapped


def input_widget_factory(wtforms_class):
    class Cls(wtforms_class, BPWidgetMixin):
        @form_group_wrapped
        @add_meta
        def __call__(self, field, **kwargs):
            kwargs.setdefault('class', 'form-control')
            return super(self.__class__, self).__call__(field, **kwargs)

    return Cls

TextInput = input_widget_factory(wt_core.TextInput)
PasswordInput = input_widget_factory(wt_core.PasswordInput)

class Select(wt_core.Select, BPWidgetMixin):
    @form_group_wrapped
    @add_meta
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class', 'form-control')
        return super(self.__class__, self).__call__(field, **kwargs)


class CheckboxInput(wt_core.CheckboxInput, BPWidgetMixin):
    @form_group_wrapped
    @add_meta
    def __call__(self, field, **kwargs):
        html = """
        <div class="checkbox">
            <label>{{ rendered_field }}{{ field.label }}</label>
        </div>
        """
        return Markup(render_template_string(
            html,
            field=field,
            rendered_field=super(self.__class__, self).__call__(field, **kwargs)
        ))

class MultipleCheckbox(BPWidgetMixin, object):
    @form_group_wrapped
    @add_meta
    def __call__(self, field, container_class='', **kwargs):
        kwargs.setdefault('type', 'checkbox')
        field_id = kwargs.pop('id', field.id)

        html = [u'<div {0}>'.format(html_params(id=field_id, class_=container_class))]
        for value, label, checked in field.iter_choices():
            choice_id = u'%s-%s' % (field_id, value)
            options = dict(kwargs, name=field.name, value=value, id=choice_id)
            if checked:
                options['checked'] = 'checked'
            html.append(u'<div class="checkbox"><label><input {input_params}'\
                        '/>{label}</label></div>'.format(
                input_params=html_params(**options),
                label=label
            ))

        html.append(u'</div>')
        return u''.join(html)



default_widgets = {
    # Multi Types
    'SelectMultipleField': Select(multiple=True),
    'SelectField': Select(),
    'QuerySelectMultipleField': Select(multiple=True),
    'QuerySelectField': Select(),

    # Input Types
    # 'DateField': None,
    'TextField': TextInput(),
    'StringField': TextInput(),
    'PasswordField': PasswordInput(),

    # Boolean Types
    'BooleanField': CheckboxInput(),
    # 'FileField': None,
    # 'SubmitField': None,
}



