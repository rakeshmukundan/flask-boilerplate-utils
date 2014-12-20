import os, sys, inspect

def choose_config(config_module,**kwargs):
    if '-c' in sys.argv:
        class_name = sys.argv[sys.argv.index('-c') + 1]
    elif '--config' in sys.argv:
        class_name = sys.argv[sys.argv.index('--config') + 1]
    elif os.environ.get('FLASK_CONFIG'):
        class_name = os.environ.get('FLASK_CONFIG')
    else:
        class_name = 'Development'

    clsmembers = inspect.getmembers(config_module, inspect.isclass)
    clsmembers = dict(clsmembers)
    if class_name in clsmembers:
        sys.stderr.write(" * Using configuration class '%s'\n" % class_name)
        return clsmembers[class_name]

    raise Exception("Configuration class '%s' could not be found." % (class_name))

