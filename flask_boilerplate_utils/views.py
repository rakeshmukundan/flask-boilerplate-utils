from flask.ext.classy import FlaskView
from flask import g

class MenuFlaskView(FlaskView):
    @classmethod
    def register(cls, app):
        """
        Take the cached attributes from the methods that were
        created using the menu_item decorator. 

        Turn them into a list and sort it.
        """

        super(__class__, cls).register(app)
        cls._menu_items = []
        for meth_str in dir(cls):
            meth = getattr(cls, meth_str)
            if hasattr(meth, '_menu_items'):
                href = '{}:{}'.format(cls.__name__, meth.__name__)
                for menu_item in meth._menu_items:
                    menu_item = menu_item + (href,)
                    cls._menu_items.append(menu_item)
        cls._menu_items.sort(key=lambda x: x[2])

    def before_request(self, name):
        """
        Make the menu items accessible to the template renderer.
        Currently there is no context_preprocessor available for 
        FlaskView's, so this is as good as it gets.
        """
        g.menu_items = self._menu_items

def menu_item(title, identifier=None, position=0):
    def decorator(f):
        item = (title, identifier or f.__name__, position)
        if not hasattr(f, '_menu_items') or f._menu_items is None:
            f._menu_items = [item]
        else:
            f._menu_items.append(item)
        return f
    return decorator