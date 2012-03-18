#!/usr/bin/env python
import os
import sys
import types


def is_str(value):
    return issubclass(type(value), types.UnicodeType) or \
        issubclass(type(value), types.StringType)


def load_class(name):
    bits = name.split('.')
    module_name = '.'.join(bits[:-1])
    target_name = bits[-1]
    __import__(module_name, {}, {}, [])
    module = sys.modules[module_name]
    return getattr(module, target_name)


def get_reference_object(class_name_with_module, key_name):
    klass = load_class(class_name_with_module)
    return klass.get_by_key_name(key_name)


def create_object(class_name_with_module, data):
    from google.appengine.ext import db
    klass = load_class(class_name_with_module)
    for key in data:
        # reference
        # <klass:key_name>
        if is_str(data[key]) and data[key].startswith('<') and data[key].endswith('>'):
            ref_klass_name, ref_key_name = data[key][1:-1].split(':')
            ref_obj = get_reference_object(ref_klass_name, ref_key_name)
            data[key] = ref_obj
    obj = klass(**data)
    obj.put()


def loaddata_from_yaml(filename):
    import yaml
    f = open(filename)
    rawdata = f.read()
    f.close()
    yamldata = yaml.load(rawdata)
    # required data
    required = yamldata.get('required', [])
    if required:
        base_dir = os.path.dirname(os.path.abspath(filename))
        for required_record in required:
            required_filepath = os.path.join(base_dir, required_record['file'] + '.yaml')
            loaddata_from_yaml(required_filepath)
    # load objects
    objects = yamldata.get('objects', [])
    created_count = 0
    for record in objects:
        object_data = record.copy()
        klass = object_data.pop('__class__')
        create_object(klass, object_data)
        created_count += 1
    sys.stdout.write('%d objects loaded. [%s]\n' % (created_count, os.path.basename(filename)))


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
        sys.stdout.write('loaddata.py yamlfile\n')
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

    loaddata_from_yaml(sys.argv[1])


if __name__ == '__main__':
    main()
