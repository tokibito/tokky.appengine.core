import sys

# application cache variable
_app_cache = {}

def get_application(name):
    global _app_cache
    if name in _app_cache:
        app = _app_cache[name]
    else:
        app = load_module(name)
        _app_cache[name] = app
    return app

def load_module(name):
    bits = name.split('.')
    module_name = '.'.join(bits[:-1])
    app_name = bits[-1]
    __import__(module_name, {}, {}, [])
    module = sys.modules[module_name]
    return getattr(module, app_name)
