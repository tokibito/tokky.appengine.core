#!/usr/bin/env python
import os
import sys


def ipython():
    """django.core.management.commands.shell
    """
    try:
        from IPython.frontend.terminal.embed import TerminalInteractiveShell
        shell = TerminalInteractiveShell()
        shell.mainloop()
    except ImportError:
        try:
            from IPython.Shell import IPShell
            shell = IPShell(argv=[])
            shell.mainloop()
        except ImportError:
            raise


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
            appconfig, unused = dev_appserver.LoadAppConfig(
                  os.path.dirname(os.path.abspath(__file__)), {})
            appid = appconfig.application
        except ImportError:
            appid = None
    return appid


def get_datastore_paths():
    """Returns a tuple with the path to the datastore and history file.

    The datastore is stored in the same location as dev_appserver uses by
    default, but the name is altered to be unique to this project so multiple
    Django projects can be developed on the same machine in parallel.

    Returns:
      (datastore_path, history_path)
    """
    from google.appengine.tools import dev_appserver_main
    datastore_path = dev_appserver_main.DEFAULT_ARGS['datastore_path']
    history_path = dev_appserver_main.DEFAULT_ARGS['history_path']
    datastore_path = datastore_path.replace("dev_appserver", "core_%s" %
                                            get_appid())
    history_path = history_path.replace("dev_appserver", "core_%s" %
                                        get_appid())
    return datastore_path, history_path


def main():
    sys.path.insert(0, search_sdk_path())
    import dev_appserver
    dev_appserver.fix_sys_path()

    from google.appengine.api import apiproxy_stub_map, datastore_file_stub
    # from kay-fw
    appid = get_appid()
    os.environ['APPLICATION_ID'] = appid
    p = get_datastore_paths()
    datastore_path = p[0]
    history_path = p[1]
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub(appid, datastore_path,
                                                   history_path)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    try:
        ipython()
    except ImportError:
        import code
        imported_objects = {}
        try:
            import readline
        except ImportError:
            pass
        else:
            import rlcompleter
            readline.set_completer(
                rlcompleter.Completer(imported_objects).complete)
            readline.parse_and_bind("tab:complete")

            pythonrc = os.environ.get("PYTHONSTARTUP")
            if pythonrc and os.path.isfile(pythonrc):
                try:
                    execfile(pythonrc)
                except NameError:
                    pass
            import user
        code.interact(local=imported_objects)


if __name__ == '__main__':
    main()