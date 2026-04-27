"""
Veritabanı Bağlantısı ve İşlemleri
SQLite backend — MySQL arayüzüyle uyumlu
"""
import sqlite3
import re
from flask import g, current_app


# ─────────────────────────────────────────────────────────────────────────────
# Query dönüştürücü  (MySQL → SQLite sözdizimi)
# ─────────────────────────────────────────────────────────────────────────────

def _adapt(query: str) -> str:
    """MySQL sorgusunu SQLite'a uyarla — hiçbir model/controller değişmez."""
    # %s → ?
    query = query.replace('%s', '?')
    # INSERT IGNORE → INSERT OR IGNORE
    query = re.sub(r'\bINSERT\s+IGNORE\b', 'INSERT OR IGNORE', query, flags=re.IGNORECASE)
    # LIMIT x,y  →  LIMIT y OFFSET x
    query = re.sub(
        r'\bLIMIT\s+(\d+)\s*,\s*(\d+)',
        lambda m: f'LIMIT {m.group(2)} OFFSET {m.group(1)}',
        query, flags=re.IGNORECASE
    )
    return query


# ─────────────────────────────────────────────────────────────────────────────
# Cursor wrapper  — fetchone/fetchall her zaman dict döner
# ─────────────────────────────────────────────────────────────────────────────

class _CursorWrapper:
    def __init__(self, cursor):
        self._cur = cursor

    def execute(self, query, params=None):
        query = _adapt(query)
        if params is not None:
            self._cur.execute(query, params)
        else:
            self._cur.execute(query)
        return self

    def executemany(self, query, seq):
        query = _adapt(query)
        self._cur.executemany(query, seq)
        return self

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        return dict(row) if hasattr(row, 'keys') else row

    def fetchall(self):
        rows = self._cur.fetchall()
        if not rows:
            return []
        return [dict(r) if hasattr(r, 'keys') else r for r in rows]

    @property
    def lastrowid(self):
        return self._cur.lastrowid

    @property
    def rowcount(self):
        return self._cur.rowcount

    def close(self):
        self._cur.close()

    def __iter__(self):
        return iter(self.fetchall())

    def __getattr__(self, name):
        return getattr(self._cur, name)


# ─────────────────────────────────────────────────────────────────────────────
# Connection proxy  — mysql.connection.cursor() / commit() / rollback()
# ─────────────────────────────────────────────────────────────────────────────

class _ConnectionProxy:
    """
    mysql.connection ile erişilen nesne.
    base.py ve controller'lardaki doğrudan .cursor() / .commit() çağrılarını karşılar.
    """

    def cursor(self, *args, **kwargs):
        """DictCursor gibi argümanlar yoksayılır; wrapper zaten dict döndürür."""
        return _CursorWrapper(_get_connection().cursor())

    def commit(self):
        conn = g.get('_db')
        if conn:
            conn.commit()

    def rollback(self):
        conn = g.get('_db')
        if conn:
            conn.rollback()

    def close(self):
        pass  # teardown halleder


# ─────────────────────────────────────────────────────────────────────────────
# MySQL proxy  — `from app.utils.database import mysql`  değişmez
# ─────────────────────────────────────────────────────────────────────────────

class _MySQLProxy:
    @property
    def connection(self):
        return _ConnectionProxy()

    def init_app(self, app):
        pass  # init_db halleder


mysql = _MySQLProxy()


# ─────────────────────────────────────────────────────────────────────────────
# SQLite bağlantı yönetimi  (request/context başına tek bağlantı)
# ─────────────────────────────────────────────────────────────────────────────

def _get_connection() -> sqlite3.Connection:
    if '_db' not in g:
        path = current_app.config.get('SQLITE_PATH', 'sqlite.db')
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA foreign_keys=ON')

        # SQLite REGEXP fonksiyonunu tanımla (MySQL uyumluluğu)
        def regexp(pattern, text):
            if text is None:
                return False
            return bool(re.search(pattern, text))

        conn.create_function('REGEXP', 2, regexp)
        g._db = conn
    return g._db


def _teardown(exc):
    conn = g.pop('_db', None)
    if conn is not None:
        if exc:
            conn.rollback()
        else:
            conn.commit()
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Dışa açık API  — imzalar değişmedi
# ─────────────────────────────────────────────────────────────────────────────

def init_db(app):
    """app/__init__.py'de çağrılır — değişmez."""
    app.teardown_appcontext(_teardown)
    app.logger.info('[DB] SQLite  →  %s', app.config.get('SQLITE_PATH', 'sqlite.db'))


def get_dict_cursor() -> _CursorWrapper:
    """Sözlük imleçi döndür"""
    return _CursorWrapper(_get_connection().cursor())


def get_cursor() -> _CursorWrapper:
    """Normal imleç döndür"""
    return _CursorWrapper(_get_connection().cursor())


def commit_db():
    """Değişiklikleri kaydet"""
    try:
        conn = g.get('_db')
        if conn:
            conn.commit()
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# MySQLdb uyumluluk katmanı
# `import MySQLdb` veya `import MySQLdb.cursors` olan dosyalar patlamasın
# ─────────────────────────────────────────────────────────────────────────────

try:
    import MySQLdb as _real_mysqldb  # noqa: F401
except ImportError:
    import types as _types, sys as _sys

    _mod = _types.ModuleType('MySQLdb')
    _cur_mod = _types.ModuleType('MySQLdb.cursors')

    class _DictCursor:
        pass

    _cur_mod.DictCursor = _DictCursor

    class _DBError(Exception):
        pass

    class _OperationalError(_DBError):
        pass

    class _ProgrammingError(_DBError):
        pass

    _mod.cursors          = _cur_mod
    _mod.Error            = _DBError
    _mod.OperationalError = _OperationalError
    _mod.ProgrammingError = _ProgrammingError

    _sys.modules['MySQLdb']         = _mod
    _sys.modules['MySQLdb.cursors'] = _cur_mod