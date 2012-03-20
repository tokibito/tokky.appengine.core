======================
開発用対話シェルの実行
======================

ローカル環境で対話シェルを使用するためには、 ``shell.py`` スクリプトを実行します。IPythonにも対応しています。

.. code-block:: bash

   $ python shell.py

.. note::

   shell.pyスクリプトは、dev_appserverと同じデータベースファイルを使用するため、dev_appserverを起動した状態では対話シェル上でのデータの変更はdev_appserver側に反映されません。
