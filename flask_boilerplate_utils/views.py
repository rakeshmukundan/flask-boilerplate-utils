from flask.ext.classy import FlaskView
from flask import g, url_for, request, current_app
from functools import wraps
import inspect


class MenuManager(object):
    """
    A Menu manager which can have multiple menus registered.
    """
    def __init__(self):
        self._menus = {}

    def register_menu(self, menu_id):
        self._menus[menu_id] = Menu(identifier=menu_id)

    def get_menu(self, menu_id):
        return self._menus[menu_id]

    @property
    def menus(self):
        return self._menus


class Menu(object):
    """
    A menu which can be registered with boilerplate's menu manager.

    :param identifier: A name for the menu. When using with_menu_manager, the 
                       menu can be accessed via jinja global 'menu.{identifier}'
    """
    def __init__(self, identifier):
        self.identifier = identifier
        self.items = []

    def register_item(self, item):
        """
        Add a menu item to the root of this menu. 
        :param item: A MenuItem object to add to the menu.
        """
        if type(item) != MenuItem:
            raise Exception("Expected item to be of type 'MenuItem'. Got"\
                " '{}'.".format(type(item)))

        self.items.append(item)
        self.items.sort(key=lambda x: x.position)

    def __iter__(self):
        """
        Iterate over the menu's items.
        """
        return self.items.__iter__()

class MenuItem(object):
    def __init__(self, title=None, identifier=None, position=0, href=None,
     menu_id=None, _root_item=False, always_expanded=False, hidden=False,
     parent=None, activates_parent=False, accepted_args=[], default_args={}):
        self.title = title
        self.identifier = identifier
        self.position = position
        self.href = href
        self.menu_id = menu_id
        self._children = []
        self._root_item = _root_item
        self.always_expanded = always_expanded
        self.hidden = hidden
        self.parent = parent
        self.activates_parent = activates_parent
        self._accepted_args = accepted_args
        self.default_args = default_args


    def is_active(self):
        """
        Helper method for determining whether or not a menu tem is 
        currently active. 
        """
        return self.url() == request.path or any(
            [child.is_active() for child in \
            self._children if child.activates_parent])

    def child_is_active(self):
        """
        Returns true if any child is active (Includes hidden children)
        """
        return any([x.is_active() for x in self._children]) 

    def should_show_children(self):
        """
        Returns true if any child is active, this item is active, or the item
        is set it always be expanded.
        """
        return self.always_expanded or \
        self.child_is_active() or self.is_active()

    def url(self, **kwargs):
        """
        Get a flask constructed URL for this menu item.
        """
        kw = {}
        if hasattr(g, '_menu_kwargs'):
            kw = g._menu_kwargs

        # Filter out kwargs which the function does not take
        kw = {key:kw[key] for key in kw if key in self._accepted_args}
        kw.update(self.default_args)
        try:
            return url_for(self.href, **kw)
        except Exception:
            return None
        
    def register_child(self, item):
        """
        Add a child menu item to this menu item.
        """
        if type(item) != MenuItem:
            raise Exception("Expected item to be of type 'MenuItem'. "\
                "Got '{}'.".format(type(item)))

        self._children.append(item)
        self._children.sort(key=lambda x: x.position)

    def has_children(self):
        """
        Return true if this item has any children (includes hidden children)
        """
        return bool(len(self._children))

    @property
    def children(self):
        return [item for item in self._children if not item.hidden]

class MenuFlaskView(FlaskView):
    """
    A subclass of FlaskView, adding capabilities for menu items
    """

    @classmethod
    def register(cls, app):
        """
        Run the FlaskView register super method and process menu items for this
        view.
        """

        super(__class__, cls).register(app)

        cls._menu_items = []
        has_root = False
        found_root_view = False

        if hasattr(cls, '_menu_item'):
            has_root = True
            if hasattr(app, 'menu_manager'):
                menu = app.menu_manager.get_menu(cls._menu_item.menu_id)
                menu.register_item(cls._menu_item)

        for meth_str in dir(cls):
            meth = getattr(cls, meth_str)
            if hasattr(meth, '_menu_item'):
                menu_item = meth._menu_item
                menu_item.href = '{}:{}'.format(cls.__name__, meth.__name__)

                if has_root and menu_item._root_item:
                    found_root_view = True
                    cls._menu_item.href = menu_item.href
                    cls._menu_item.title = menu_item.title
                    cls._menu_item.identifier = menu_item.identifier

                else:
                    if not menu_item.parent:
                        cls._menu_items.append(menu_item)
                        if has_root:
                            cls._menu_item.register_child(menu_item)
                        elif menu_item.menu_id:
                            menu = app.menu_manager.get_menu(menu_item.menu_id)
                            menu.register_item(menu_item)

        cls._menu_items.sort(key=lambda x: x.position)
        

    def before_request(self, name, **kwargs):
        """
        Makes the menu items accessible to the template renderer.

        If not using use_menu_manager = True, access the current view's menus
        via jinja global 'menu_items'

        If you are using menu manager, you can use the above, but also use 
        section_menu_items for scoping. 
        """
        g._menu_kwargs = kwargs
        current_app.jinja_env.globals['menu_items'] = self._menu_items
        if hasattr(self, '_root_item'):
            current_app.jinja_env.globals['section_menu_items'] = \
            self._root_item.children

def menu_item(title='', identifier=None, position=10, menu_id=None, 
    root_item=False, always_expanded=False, hidden=False, 
    parent=None, activates_parent=False, default_args={},
    accepted_args=None):
    
    """
    Decorator for defining a menu item.

    @menu_item('My Menu Item', default_args={'some_id':22})
    @menu_item('Hello World', order=0)


    :param title: Title of the menu item
    :param identifier: Identifier of the menu item, automatically generated by
                       class name and method name if not provided.
    :param position: Position for the menu item. 0 = top of list.
    :param menu_id: Add this item to a registered menu if using 
                    with_menu_manager=True in your boilerplate config.
    :param root_item: Declare this as a root item if the class containing
                      this method if a menu item. (When using menu_manager)
    :param always_expanded: Always show the children of this menu item
    :param hidden: Hide this menu item from showing in any children iterators.
                   Hides the item from menus. Useful if you wish to 
                   activate/expand a parent without showing the child.
    :param activates_parent: Makes the parent item active. Useful when hidden.
    :param default_args: When generating a url for this item, give it the default
                         url_for kwargs, otherwise the active view's kwargs are 
                         used
    :param accepted_args: Define what arguments are accepted by the url_for
                          generator. This allows kwargs to be filtered out if 
                          the user is in a view which also takes kw as input.
                          If not defined, the names of kwargs for the method 
                          are used.

    
    """
    def decorator(f):
        _accepted_args = accepted_args
        if not accepted_args:
            _accepted_args = inspect.getargspec(f)[0]
        
        _parent = None
        if parent:
            _parent = parent._menu_item

        item = MenuItem(
            title=title,
            identifier=identifier,
            position=position,
            menu_id=menu_id,
            _root_item=root_item,
            always_expanded=always_expanded,
            parent=_parent,
            hidden=hidden,
            activates_parent=activates_parent,
            accepted_args=_accepted_args,
            default_args=default_args
        )
        if _parent:
            _parent.register_child(item)

        f._menu_item = item

        return f
    return decorator

def activates(func, default_args={}):
    """
    Decorator for defining a child menu item and automatically activating
    it's parent and setting it hidden. 

    Simply a convenience decorator for @menu_item.
    """


    def decorator(f):
        accepted_args = inspect.getargspec(f)[0]
        
        @menu_item(hidden=True, parent=func, activates_parent=True, 
            accepted_args=accepted_args, default_args=default_args)
        @wraps(f)
        def fc(*args, **kwargs):
            return f(*args, **kwargs)
        return fc
    return decorator  
