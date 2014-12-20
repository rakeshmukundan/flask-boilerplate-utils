from wtforms.validators import Optional, ValidationError
import os

class ValidFileFormat(Optional):
    def __init__(self, fileupload, *args, **kwargs):
        self.fileupload = fileupload
        self.message = 'The selected file cannot be uploaded. Only %s are allowed.' % (
                ', '.join([t.lower() for t in fileupload._config.allow])
            )
        if 'message' in kwargs:
            self.message = kwargs['message']

    def __call__(self, form, field):
        filename, extension = os.path.splitext(field.data.filename)
        if not self.fileupload.extension_allowed(extension[1:].lower()):
            raise ValidationError(self.message)


class Unique(object):
    """
    Database Unique Validator for WTForms / SQLAlchemy.
    Throws ValidationError if the data alread exists in
    the database for the specified field.

    @param string timestamp     formatted date to display
    @param string priority      priority number
    @param string priority_name priority name
    @param string message       message to display

    @return string formatted string
    """
    def __init__(self, model, field, *args, **kwargs):
        self.model = model
        self.field = field
        self.message = 'A record with this information already exists.'
        if 'message' in kwargs:
            self.message = kwargs['message']

    def __call__(self, form, field):
        if self.model.query.filter(self.field == field.data).count() > 0:
            raise ValidationError(self.message)
