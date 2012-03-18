# coding: utf-8
import os
import logging

import config

from core import directory


def readfile(filepath):
    """ファイルを読み込んでデータを返す関数
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    return data


def get_404_page():
    """404ページのデータを返す関数
    """
    filepath = os.path.join(
        directory.get_base_dir(),
        getattr(config, '404_FILE_PATH', 'static/404.html'))
    return readfile(filepath)


def not_found(environ, start_response):
    """404ページのWSGIアプリケーション
    """
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return get_404_page()


def webapp2_not_found_handler(request, response, e):
    """webapp2.WSGIApplication用の404ページのハンドラ
    """
    logging.info(e)
    data = get_404_page()
    response.out.write(data)
    response.status_int = 404
    return response
