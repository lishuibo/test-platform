from wtforms import Form

__author__ = 'litl'


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message