#!/usr/bin/env python

# Copyright (c) 2014, Lev Givon
# All rights reserved.
# Distributed under the terms of the BSD license:
# http://www.opensource.org/licenses/bsd-license/

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.config.configurable import Configurable

from py2neo import neo4j

def parse(cell, self):
    opts, cell = self.parse_options(cell, '')

    uri = 'http://localhost:7474/db/data/'
    parts = [part.strip() for part in cell.split(None, 1)]
    if not parts:
        return {'uri': uri, 'query': ''}
    if '://' in parts[0]:
        uri = parts[0]
        if len(parts) > 1:
            query = parts[1]
        else:
            query = ''
    else:
        query = cell
    return {'uri': uri.strip(), 'query': query.strip(), 'opts': opts}

@magics_class
class CypherMagic(Magics, Configurable):    
    db = None

    @line_magic
    @cell_magic
    def cypher(self, line, cell=''):
        """
        Runs Cypher query against Neo4J database.

        Returns results of a Cypher query as a list of py2neo class instances.

        Examples
        --------
        %%cypher http://localhost:7474/db/data
        MATCH (n) RETURN n

        %cypher CREATE (n {name: 'foo'}) RETURN n

        Notes
        -----
        If no database URI is specified, the default URI 
        http://localhost:7474/db/data/ is assumed.
        """

        parsed = parse('%s\n%s' % (line, cell), self)

        if self.db is None or self.db.__uri__ != parsed['uri']:
            self.db = neo4j.GraphDatabaseService(parsed['uri'])

        if not parsed['query']:
            raise Exception('no Cypher query specified')
        q = neo4j.CypherQuery(self.db, parsed['query'])

        if 'n' in parsed['opts']:
            pass
        else:
            return [r.values for r in q.execute().data]

def load_ipython_extension(ip):
    ip.register_magics(CypherMagic)
