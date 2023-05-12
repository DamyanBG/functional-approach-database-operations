from psycopg2 import connect
from psycopg2.extensions import cursor, connection
from typing import Optional, Callable, Any, Tuple
from os import environ


def database_connect(cursor_factory: Optional[Any] = None) -> connection:
    return connect(
        user=environ["USER"],
        password=environ["PASSWORD"],
        database=environ["DATABASE_BANE"],
        host=environ["HOST"],
        port=environ["POST"],
        cursor_factory=cursor_factory,
    )


def execute_query(
    connect_func: Callable[[Optional[Any]], connection],
    sql_query: str,
    fetch_func: Optional[Callable[[cursor], Optional[Tuple[Any, ...]]]] = None,
    cursor_factory: Optional[cursor] = None,
):
    result = None
    conn = connect_func(cursor_factory)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            if fetch_func:
                result = fetch_func(cursor)
    conn.close()
    return result


def execute_transaction(
    connect_func, sql_queries, fetch_func=None, cursor_factory=None
):
    result = []
    conn = connect_func(cursor_factory)
    with conn:
        with conn.cursor() as cursor:
            for sql_query in sql_queries:
                cursor.execute(sql_query)
                if fetch_func:
                    result.append(fetch_func(cursor))
    conn.close()
    return result


def insert_query_builder(table_name: str, columns: list[str], values: list[str]) -> str:
    return f"""
    INSERT INTO {table_name} (
      {",".join(columns)}
    ) VALUES (
      {",".join(map(lambda string: f"'{string}'", values))}
    ) Returning id;
  """
