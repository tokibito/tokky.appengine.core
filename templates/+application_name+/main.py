import sys

from google.appengine.ext.webapp import util

def get_traceback(exc_info):
    import traceback
    ret = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
    try:
        return ret.decode('utf-8')
    except UnicodeDecodeError:
        return ret

def main():
    # logging exception
    try:
        from core.entrypoint import get_root_application
        root_application = get_root_application()
        util.run_wsgi_app(root_application)
    except Exception, e:
        import logging
        logging.error(get_traceback(sys.exc_info()))
        raise

if __name__ == '__main__':
    main()