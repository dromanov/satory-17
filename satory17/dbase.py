# -*- coding: utf-8 -*-

ur'''
Extremely simple abstaction of a database (almost a mock).

Database is created using constructor which contains database name, and fields
(both names and types):
    >>> from dbase import DBase

Removing test database file (warning, explicit usage of internal knowledge!):
    >>> import os
    >>> if os.path.isfile('dummy_db.sqlite3'): os.unlink('dummy_db.sqlite3')

Creating database and playing with it:
    >>> db = DBase('dummy_db', key=int, text=unicode, annotation=unicode)
    >>> db.haskey(12)
    False
    >>> db.save(12, text=u'Hi!  مرحباً! Привет!', annotation='Google it :-)')
    >>> db.haskey(12)
    True
    >>> for k, v in sorted(db.load(12).items()): print k, '->', v
    annotation -> Google it :-)
    key -> 12
    text -> Hi!  مرحباً! Привет!
'''

from __future__ import with_statement

import apsw

from satory_error import SatoryError
from say          import say, TODO

class DBase:
    def __init__(self, filename, key, **fields):
        '''Opens database file.'''
        # Persistent connection to read data w/o wasting time on handshakes.
        TODO('do filename sanity checks here')
        say.critical('do filename sanity checks here')
        self.filename = filename + '.sqlite3'
        self.con = apsw.Connection(self.filename)

        self.timeout_millisecs = 2000
        self.con.setbusytimeout(self.timeout_millisecs)

        # 'zip(*arr)' unzips previously zipped array 'arr'.
        items = [('key', key)] + sorted(fields.items())
        keys, values = zip(*items)
	self.fields = keys
	self.types = values
        self.table = filename.replace('.', '_')

	sql = { unicode : 'TEXT',
		str     : 'TEXT',
		int     : 'INTEGER' }
	query = "CREATE TABLE IF NOT EXISTS `{0}` (".format(self.table)
	for field, type in zip(self.fields, self.types):
	    query += ' `{0}` {1} NOT NULL,'.format(field, sql[type])
	query += " PRIMARY KEY (key));"
        with apsw.Connection(self.filename) as dbase:
            dbase.setbusytimeout(self.timeout_millisecs)
            cur = dbase.cursor()
	    cur.execute(query)

    def haskey(self, key):
        c = self.con.cursor()
        query = "SELECT COUNT(*) FROM %s WHERE key=?" % self.table
        values = c.execute(query, (key,)).next()
        c.close ()
        return bool(values[0])

    def load(self, key, **fields):
        '''Loads data and returns record object.'''
        c = self.con.cursor()
        query = "SELECT %s FROM %s WHERE key=?;" % (','.join(self.fields),
						    self.table)
        values = c.execute(query, (key,)).next()
        c.close ()
        return dict(zip(self.fields, values))

    def save(self, key, **fields):
	'''Slow write using separate blocking connection.'''
	keys, values = zip(*sorted(fields.items()))
	if keys != self.fields[1:]:
	    say.error('dbase %s: declared keys = %s', self.filename, self.keys)
	    say.error('dbase %s:    saved keys = %s', self.filename, keys)
	    raise SatoryError('bad save: inconsistent fields')

	values = (t(v) for t, v in zip(self.types, (key,) + values))
	questions = ', '.join('?' for v in self.types)
	query = u"INSERT OR REPLACE INTO %s %s VALUES (%s);" % (self.table,
							self.fields, questions)
        with apsw.Connection(self.filename) as dbase:
            dbase.setbusytimeout(self.timeout_millisecs)
            cur = dbase.cursor()
            cur.execute(query, values)

    def close(self):
        if self.con is not None:
            self.con.close()
            self.con = None

    def __del__(self):
        self.close()


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                               |doctest.NORMALIZE_WHITESPACE)
