from django.test import TestCase

from testapp.models import TestModel

#from django.db.models import Field, FloatField
#from django.db.models.expressions import CombinedExpression, Func, Value
#from django.db.models.lookups import Lookup
#
#class Score(Func):
#    function = ''
#    _output_field = FloatField()
#
#    def __init__(self, model, **extra):
#        super().__init__(**extra)
#        self._model = model
#
#    def as_sql(self, compiler, connection, function=None, template=None):
#        return 'pgroonga.score(%s)' % self._model._meta.db_table, []
#
#
#class GroongaQuery(Lookup):
#    lookup_name = 'groonga'
#
#    def as_sql(self, qn, connection):
#        lhs, lhs_params = self.process_lhs(qn, connection)
#        rhs, rhs_params = self.process_rhs(qn, connection)
#        params = lhs_params + rhs_params
#        return '%s @@ %s' % (lhs, rhs), params
#
#Field.register_lookup(GroongaQuery)
from django_pgroonga import *

class PgroonTestCase(TestCase):
    def test_score(self):
        TestModel(text1='あいうえお').save()
        ret = TestModel.objects.annotate(score=Score(TestModel)).order_by('-score').filter(text1__contains='あいうえお')
        r = list(ret)
        print(r)

    def test_query(self):
        TestModel(text1='あいうえお').save()
        TestModel(text1='かきくけこ').save()
        ret = TestModel.objects.filter(text1__groonga='あいうえお OR かきくけこ')
        a=list(ret)
        print(a)

