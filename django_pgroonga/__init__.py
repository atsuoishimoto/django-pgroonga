from django.db.models import Field, FloatField
from django.db.models.expressions import CombinedExpression, Func, Value
from django.db.models.lookups import Lookup

__all__ = ['Score', 'Query']
class Score(Func):
    function = ''
    _output_field = FloatField()

    def __init__(self, model, **extra):
        super().__init__(**extra)
        self._model = model

    def as_sql(self, compiler, connection, function=None, template=None):
        return 'pgroonga.score(%s)' % self._model._meta.db_table, []


class Query(Lookup):
    lookup_name = 'groonga'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s @@ %s' % (lhs, rhs), params

Field.register_lookup(Query)
