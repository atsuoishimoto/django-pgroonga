
django-pgroonga - PGroonga utility for Django
==============================================

django-pgroonga は Django で PGroonga を利用するためのユーティリティです


PGroonga のセットアップ
------------------------

PGroonga で全文検索を行うために、以下の設定を行います。

1. PGroonga の Extension 登録

2. 検索用インデックスの作成

Extensionの登録はデータベース作成後に一回だけ行います。検索用インデックスは、検索対象となるカラムごとにそれぞれ作成します。


この設定は、手動でSQLを実行しても構いませんが、以下のようにDjangoのマイグレーションとして登録・実行できます。


空のマイグレーションを作成する
*********************************

.. code-block:: sh

   $ python3 manage.py makemigration testapp --empty
   Migrations for 'testapp':
     testapp/migrations/0002_auto_20161210_1544.py:


マイグレーションを編集する
*********************************

作成されたマイグレーション(上の例では testapp/migrations/0002_auto_20161210_1544.py ) を、以下のように編集します。この例では、全文検索用のインデックスを、``testapp_testmodel`` テーブルの ``text1`` カラムに作成しています。

.. code-block:: python

   from __future__ import unicode_literals
   from django.db import migrations

   class Migration(migrations.Migration):
   
       dependencies = [
           ('testapp', '0001_initial'),
       ]
   
       operations = [
           # pgroonga を登録する(一回のみ)
           migrations.RunSQL(
               'CREATE EXTENSION pgroonga',
               'DROP EXTENSION pgroonga',
           ),

           # 全文検索用インデックスを作成する(検索対象のカラムごとに作成)
           migrations.RunSQL(
               'CREATE INDEX idx1 ON testapp_testmodel USING pgroonga (id, text1)',
               'DROP INDEX idx1',
           )
       ]


検索する
------------------------

PGroonga用のインデックスを作成したカラムは、Djangoの ``contains`` を使った検索で全文検索を行えます。

.. code-block:: python

   TestModel(text1='あいうえお').save()  # 日本語のテキストを登録
   TestModel.objects.filter(text1__contains='あいうえお')

この検索は ``like`` 演算子を利用した、指定した単語を検索するSQLとして実行されます。

``@@`` 演算子を使用し、Groongaのクエリ構文で検索する場合は、ルックアップとして ``groonga`` を指定します。


.. code-block:: python

   TestModel.objects.filter(text1__groonga='あいうえお OR かきくけこ')


検索スコア
------------------------

検索のマッチ度合いは、``django_pgroonga.Score()`` 関数を使って取得します。

.. code-block:: python

   from django_pgroonga import Score
   
   for r in TestModel.objects.annotate(score=Score(TestModel)).order_by('-score').filter(text1__contains='あいうえお'):
       print(r.score, r.text1)


``django_pgroonga.Score()`` は、``pgroonga.score`` 関数を呼び出してスコアを取得します。スコアは、PGroongaインデックスにテーブルのプライマリキーが含まれている場合のみ取得可能で、含まれていなければ常に ``0`` を返します。


LICENSE
----------------


Copyright (c) 2016 Atsuo Ishimoto

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
