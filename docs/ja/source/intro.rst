========
はじめに
========

これは何？
==========

tokky.appengine.core は `GoogleAppEngine`_ (以降AppEngine)用のアプリケーションフレームワークです。

AppEngine の Python 版のSDKに含まれている `webapp フレームワーク`_ をベースとして、少しだけ便利にする機能を提供します。
大きめのアプリケーションを作る場合などに楽かもしれません。

次に示す機能を提供します:

* 機能単位のURLルーティング
* 設定によるアプリケーションの自動ロード
* unittestの実行
* doctestの実行

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

ソースコード
============

オリジナルのソースコードは bitbucket.org 上のリポジトリで管理されています。

https://bitbucket.org/tokibito/tokky.appengine.core/

ライセンス
==========

tokky.appengine.core のソースコードのライセンスは、 New BSD License とします。
