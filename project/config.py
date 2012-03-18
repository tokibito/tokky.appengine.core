# coding: utf-8
# webapp debug flag
DEBUG = True

# appstats
ENABLE_APPSTATS = False

# installed apps
APPS = [
    (r'^/_ah/warmup$', 'apps.warmup.handlers.application'),  # ウォームアップ用アプリケーション
]

# global middleware
MIDDLEWARE = [
    'core.middleware.not_found_middleware',
    #'basic_auth.apply_middleware',  # サイトにベーシック認証をかけるミドルウェア
]

# not found app
NOT_FOUND_APP = 'core.defaultapps.not_found'

MEDIA_URL = '/'

##############################
# basic_authモジュールの設定
##############################
BASIC_AUTH_REALM = 'project'
BASIC_AUTH_USERNAME = 'username'
BASIC_AUTH_PASSWORD = 'password'
# ベーシック認証の対象とするページのURLを正規表現で指定
BASIC_AUTH_PATHS = [
    '^/$',
]


##########################################
# 本番環境設定(config_production.py)読み込み
# configの内容はここより前に書いてください
##########################################
PRODUCTION_APP_ID = 'production_appid'  # 本番環境と判定するAPP_ID
def is_production():
    import os
    raw_app_id = os.environ.get('APPLICATION_ID')
    if not raw_app_id:
        return False
    # s~という文字列が先頭に付与されているので削除して判定
    return raw_app_id.replace('s~', '') == PRODUCTION_APP_ID
if is_production():
    import logging
    try:
        logging.info('loading config_production...')
        from config_production import *
    except ImportError:
        logging.error('---- config_production is not exist. using default config.  ----')
##########################################
# ローカル設定(config_local.py)読み込み
##########################################
# 開発サーバ判定
def is_development():
    import os
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
# ローカル設定読み込み
if is_development():
    import logging
    logging.info('---- development ----')
    try:
        from config_local import *
    except ImportError:
        logging.warn('---- config_local is not exist. using default config.  ----')
