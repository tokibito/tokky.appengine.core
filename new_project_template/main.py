# coding: utf-8
import sys


def get_traceback(exc_info):
    import traceback
    ret = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
    try:
        return ret.decode('utf-8')
    except UnicodeDecodeError:
        return ret


def application(environ, start_response):
    # logging exception
    try:
        from core.entrypoint import get_root_application
        root_application = get_root_application()
        return root_application(environ, start_response)
    except Exception, e:
        import logging
        logging.error(get_traceback(sys.exc_info()))
        raise


def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
