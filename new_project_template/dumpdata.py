#!/usr/bin/env python
import os
import sys
import types


def is_str(value):
    return issubclass(type(value), types.UnicodeType) or \
        issubclass(type(value), types.StringType)


def is_int(value):
    return issubclass(type(value), types.IntType) or \
        issubclass(type(value), types.LongType)


def load_class(name):
    bits = name.split('.')
    module_name = '.'.join(bits[:-1])
    target_name = bits[-1]
    __import__(module_name, {}, {}, [])
    module = sys.modules[module_name]
    return getattr(module, target_name)


def to_yaml(data):
    import yaml
    result = yaml.safe_dump(data)
    return result


def object_to_dict(obj, fields):
    from google.appengine.ext import db
    result = {}
    result['__class__'] = '%s.%s' % (
        obj.__class__.__module__,
        obj.__class__.__name__)
    result['key_name'] = obj.key().name()
    for attr_name, property_obj in obj.properties().items():
        if fields:
            if attr_name not in fields:
                continue
        origin_value = getattr(obj, attr_name, None)
        if isinstance(property_obj, db.ReferenceProperty):
          if origin_value is None:
              value = None
          else:
              value = '<%s.%s:%s>' % (
                  origin_value.__class__.__module__,
                  origin_value.__class__.__name__,
                  origin_value.key().name())
        #elif is_str(origin_value):
        #    value = origin_value.encode('utf-8')
        #elif is_int(origin_value):
        #    value = int(origin_value)
        else:
            value = origin_value
        result[attr_name] = value
    return result


def dumpdata_from_model(model_class, fields):
    data = {
        'objects': []
    }
    objects = model_class.all().fetch(limit=1000)
    for obj in objects:
        data['objects'].append(object_to_dict(obj, fields))
    return to_yaml(data)


def search_sdk_path():
    raw_paths = os.environ['PATH']
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for path in raw_paths.split(sep):
        dev_script_path = os.path.join(path, 'dev_appserver.py')
        if os.path.exists(dev_script_path):
            return path
    raise Exception("SDK Path is not found.")


def get_appid():
    from google.appengine.api import apiproxy_stub_map
    have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))
    if have_appserver:
        appid = os.environ.get('APPLICATION_ID')
    else:
        try:
            from google.appengine.tools import dev_appserver
            appconfig, unused, unused = dev_appserver.LoadAppConfig(
                  os.path.dirname(os.path.abspath(__file__)), {})
            appid = appconfig.application
        except ImportError:
            appid = None
    return appid


def get_datastore_paths():
    """Returns a tuple with the path to the datastore and history file.
    """
    from google.appengine.tools import dev_appserver_main
    datastore_path = dev_appserver_main.DEFAULT_ARGS['datastore_path']
    history_path = dev_appserver_main.DEFAULT_ARGS['history_path']
    #datastore_path = datastore_path.replace("dev_appserver", "core_%s" %
    #                                        get_appid())
    #history_path = history_path.replace("dev_appserver", "core_%s" %
    #                                    get_appid())
    return datastore_path, history_path


def main():
    if len(sys.argv) < 2:
        sys.stdout.write('dumpdata.py model_name [fields]\n')
        sys.exit()

    sys.path.insert(0, search_sdk_path())
    import dev_appserver
    dev_appserver.fix_sys_path()
    from google.appengine.api import apiproxy_stub_map, datastore_file_stub
    from google.appengine.api.memcache import memcache_stub
    # from kay-fw
    appid = 'dev~%s' % get_appid()
    os.environ['APPLICATION_ID'] = appid
    os.environ['SERVER_SOFTWARE'] = 'Development/1.0'
    p = get_datastore_paths()
    datastore_path = p[0]
    history_path = p[1]
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub(appid, datastore_path,
                                                   history_path)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    apiproxy_stub_map.apiproxy.RegisterStub('memcache',
        memcache_stub.MemcacheServiceStub())

    fields = None
    if len(sys.argv) > 2:
        fields = [field_name for field_name in sys.argv[2].split(',')]

    model_class = load_class(sys.argv[1])
    result = dumpdata_from_model(model_class, fields)
    sys.stdout.write(result + '\n')


if __name__ == '__main__':
    main()
