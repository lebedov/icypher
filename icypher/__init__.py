#!/usr/bin/env python

# Copyright (c) 2014-2017, Lev E. Givon
# All rights reserved.
# Distributed under the terms of the BSD license:
# http://www.opensource.org/licenses/bsd-license

import re

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.display import display_javascript
from IPython.config.configurable import Configurable

try:
    from notebook.services.config.manager import ConfigManager
except:
    from IPython.html.services.config.manager import ConfigManager

import py2neo

js = """
require(['notebook/js/codecell'], function(codecell) {
  codecell.CodeCell.options_default.highlight_modes['magic_application/x-cypher-query'] = {'reg':[/^%%cypher/]};
  Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
      Jupyter.notebook.get_cells().map(function(cell){
          if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;
  });
});
"""

# Use older standalone httpstream package because of possible bug in 
# py2neo-included httpstream package:
from httpstream.packages.urimagic import URI

def parse(cell, self):
    # Set posix=False to preserve quote characters:
    opts, cell = self.parse_options(cell, '', posix=False)

    # Default URI:
    uri = self.default_uri
    user = ''
    passwd = ''
    query = ''

    # Split the line/cell contents into a first line and a remainder:
    parts = [part.strip() for part in cell.split(None, 1)]

    # If the cell is empty, return the default URI, user name, and password:
    if not parts:
        return {'uri': uri, 'user': user, 'passwd': passwd,
                'query': query}

    # Check if a URI was specified:
    if '://' in parts[0]:
        uri = parts[0]
        if len(parts) > 1:
            query = parts[1]

        # Extract user and passwd (if any) from URI:
        u = URI(uri)
        user_info = u.user_info
        if user_info is None:
            pass
        elif ':' not in user_info:
            user = user_info
        else:
            user, passwd = user_info.split(':')

    # Check if a user:passwd string was specified:
    elif re.search('^[^:]+:[^:]+$', parts[0]):
        try:
            user, passwd = parts[0].split(':')
        except:
            raise ValueError('bad user:name or URI specified')
        if len(parts) > 1:
            query = parts[1]
    else:
        query = cell

    # Reconstruct URI without user/passwd:
    u = URI(uri)
    uri = URI.build(scheme=u.scheme, host=u.host, port=u.port,
            absolute_path_reference=u.absolute_path_reference).string

    return {'uri': uri, 'user': user, 'passwd': passwd,
            'query': query.strip()}

@magics_class
class CypherMagic(Magics, Configurable):
    db = None
    user = None
    passwd = None
    uri = None
    default_uri = 'http://localhost:7474/db/data/'

    def __init__(self, *args, **kwargs):
        super(CypherMagic, self).__init__(*args, **kwargs)
        display_javascript(js, raw=True)
        
    @line_magic
    @cell_magic
    def cypher(self, line, cell=''):
        """
        Runs Cypher query against Neo4J database.

        Returns results of a Cypher query as a py2neo.cypher.core.RecordList instance.

        Examples
        --------
        %cypher http://user:passwd@localhost:7474/db/data

        %cypher user:passwd

        %%cypher http://localhost:7474/db/data
        MATCH (n) RETURN n

        %cypher CREATE (n {name: 'foo'}) RETURN n

        Notes
        -----
        If no database URI is specified, the default URI
        http://localhost:7474/db/data/ is assumed. Subsequent invocations of the 
        extension may specify a different user/password and/or database.
        """

        parsed = parse('%s\n%s' % (line, cell), self)

        changed = False
        u = URI(parsed['uri'])
        if self.user is None or (parsed['user'] and self.user != parsed['user']):
            self.user = parsed['user']
            changed = True
        if self.passwd is None or (parsed['passwd'] and self.passwd != parsed['passwd']):
            self.passwd = parsed['passwd']
            changed = True
        if self.uri is None or (parsed['uri'] and self.uri != parsed['uri']):
            self.uri =  parsed['uri']
            changed = True

        if self.user and self.passwd:
            user_info = self.user+':'+self.passwd
        elif self.user:
            user_info = self.user
        else:
            user_info = None

        uri = URI.build(scheme=u.scheme, host=u.host, port=u.port,
                            absolute_path_reference=u.absolute_path_reference,
                            user_info=user_info).string

        # Only update the database connection if the user name, password, or URI
        # have changed:
        if self.db is None or changed:
            self.db = py2neo.Graph(uri)

        if parsed['query']:
            return self.db.cypher.execute(parsed['query'])

def load_ipython_extension(ip):
    ip.register_magics(CypherMagic)
