from flask import render_template_string
from .Widget import Widget
"""
Widgets for rendering generic form field types.
 - Text Box
 - Text Area
 - Radio Button
 - Checkbox 
"""


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


class Textbox(Widget):
    def __call__(self, field, **kwargs):
        html = """
        """
        return field(class="form-control", **kwargs)
