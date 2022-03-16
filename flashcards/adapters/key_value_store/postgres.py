import json
from typing import Callable, Dict, Any, List

from flashcards.adapters.key_value_store.key_value_store import KeyValueStore, \
    Key, Value
from flashcards.adapters.key_value_store.query import Query, FieldEqual, AndQuery, FieldContains
from flashcards.adapters.transaction.pg_transaction import PGTransaction


class PGKeyValueStore(KeyValueStore[Key, Value]):
    def __init__(
        self,
        transaction: PGTransaction,
        table_name: str,
        dump_key: Callable[[Key], str],
        dump_value: Callable[[Value], str],
        restore_value: Callable[[Dict[str, Any]], Value]
    ) -> None:
        self._transaction = transaction
        self._table_name = table_name
        self._dump_key = dump_key
        self._dump_value = dump_value
        self._restore_value = restore_value

    def set(self, key: Key, value: Value) -> None:
        self._transaction.cursor.execute(
            f'''
            INSERT INTO {self._table_name} (key, data)
            VALUES (%(key)s, %(data)s)
            ON CONFLICT (key)
            DO UPDATE SET data = %(data)s
            ''',
            {
                'key': self._dump_key(key),
                'data': self._dump_value(value)
            }
        )

    def get(self, key: Key) -> Value:
        self._transaction.cursor.execute(
            f'''
            SELECT data FROM {self._table_name} WHERE key=%s;
            ''',
            (self._dump_key(key),)
        )
        raw_data = self._transaction.cursor.fetchone()[0]
        return self._restore_value(raw_data)

    def find(self, query: Query) -> List[Value]:
        self._transaction.cursor.execute(
            f'''
            SELECT data FROM {self._table_name}
            WHERE {self._interpret_query(query)}
            '''
        )
        return [
            self._restore_value(row[0])
            for row in self._transaction.cursor.fetchall()
        ]

    @staticmethod
    def _interpret_query(query: Query) -> str:
        if isinstance(query, FieldEqual):
            query_json = json.dumps({query.field: query.value}, default=str)
            return f'data @>  \'{query_json}\''
        if isinstance(query, AndQuery):
            return ' AND '.join(
                PGKeyValueStore._interpret_query(clause)
                for clause in query.queries
            )
        if isinstance(query, FieldContains):
            raise NotImplementedError(
                'because of pydantic this cannot yet be implemented '
                '(pydantic whines about dicts being mutable and cannot deal with Mappings)'
            )
        raise TypeError
