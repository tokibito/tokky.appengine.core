==========================
ユニットテストの作成と実行
==========================

ユニットテストの実行
====================

ユニットテストを実行するためには ``unittests.py`` スクリプトを実行します。

.. code-block:: bash

   $ python unittests.py
   test_ok (apps.warmup.tests.WarmupHandlerTest) ... ok
   
   ----------------------------------------------------------------------
   Ran 1 test in 0.610s
   
   OK

warmupアプリケーションには、 ``tests.py`` という名前のモジュールに ``unittests.HandlerTestCase`` クラスを継承したユニットテストが書かれています。HandlerTestCaseクラスは継承ツリーにunittestモジュールのTestCaseクラスを含んでいます。

``unittests.py`` はTestCaseクラスを継承したユニットテストを見つけて実行します。

また、引数にディレクトリパスを指定することで、任意のディレクトリ以下のテストのみを実行することができます。

.. code-block:: bash

   $ python unittests.py apps/warmup

.. note::

   tokky.appengine.core では、テスト対象のユニットテストを見つけるためにunittest2(Python2.7では標準モジュールのunittest)モジュールのdiscover関数を使用しています。

ユニットテストの作成
====================

GAEのDatastoreやMemcacheなどのサービスを使用するテストは、 ``unittests`` モジュールのクラスを継承して実装します。

TestbedTestCase
---------------

``unittest.TestCase`` クラスを継承しています。 ``setUp`` メソッド内でTestbed(``google.appengine.ext.testbed``)を有効にしています。

HandlerTestCase
---------------

``TestBedTestCase`` クラスを継承しています。
