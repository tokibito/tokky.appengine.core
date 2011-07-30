==========================
アプリケーションを作成する
==========================

AppEngine用の新規プロジェクトを作成します。

``scaffold`` コマンドを実行します。このドキュメントでは `engineapp` という名前のアプリケーションを作成します。

::

   $ scaffold create tokky.appengine.core
   application_name: engineapp

これで雛型からアプリケーションディレクトリが作成されました。

AppEngineの開発サーバを起動して、確認してみます。

::

   $ cd engineapp
   $ dev_appserver.py .

起動したアドレスをブラウザで開いてみてください。

何も設定していない状態では `404 not Found.` と表示されるはずです。

トップページを有効にしてみましょう。

engineappディレクトリ内の ``config.py`` というファイルをエディタで開き、 ``APPS`` の次の行のコメント文字を消してください。

.. code-block:: python

   # installed apps
   APPS = [
       (r'^/$', 'apps.toppage.application'),
   ]

これでトップページが有効になりました。

ブラウザでもう一度開いてみると、 `hello world!` と表示されます。
