========
はじめに
========

これは何？
==========

tokky.appengine.core は `GoogleAppEngine`_ (以降AppEngine)用のアプリケーションフレームワークです。

AppEngine の Python 版のSDKに含まれている `webapp フレームワーク`_ をベースとして、少しだけ便利にする機能を提供します。
大きめのアプリケーションを作る場合などに楽かもしれません。

機能単位のURLルーティングと、設定による自動ロードを提供します。

.. _`GoogleAppEngine`: http://code.google.com/appengine/
.. _`webapp フレームワーク`: http://code.google.com/appengine/docs/python/tools/webapp/

インストール
============

tokky.appengine.core をインストールする前に、 `Google App Engine SDK for Python`_ をインストールしてください。

.. _`Google App Engine SDK for Python`: http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python

scaffoldコマンドによるインストール
----------------------------------

tokky.appengine.core は `aodag.scaffold`_ のコマンドから使用します。

``scaffold`` コマンドからzipファイルをインストールします。

::

   $ scaffold install https://bitbucket.org/tokibito/tokky.appengine.core/downloads/tokky.appengine.core.zip tokky.appengine.core

これでインストールは完了です。

.. _`aodag.scaffold`: http://pypi.python.org/pypi/aodag.scaffold/
