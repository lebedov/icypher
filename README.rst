.. -*- rst -*-

.. image:: https://raw.githubusercontent.com/lebedov/icypher/master/icypher.png
    :alt: icypher

Package Description
-------------------
ICypher is an IPython extension for running Cypher queries against a `Neo4J
<http://neo4j.com>`_ graph database within IPython.

.. image:: https://img.shields.io/pypi/v/icypher.svg
    :target: https://pypi.python.org/pypi/icypher
    :alt: Latest Version
.. .. image:: https://img.shields.io/pypi/dm/icypher.svg
..     :target: https://pypi.python.org/pypi/icypher
..    :alt: Downloads

Installation
------------
The package may be installed as follows: ::

    pip install icypher

After installation, the extension may be loaded within an IPython session
with ::

    %load_ext icypher

Usage Examples
--------------
Use default URI ``http://localhost:7474/db/data``: ::

    %cypher

Set name and password, but use default URI: ::
  
    %cypher user:passwd

Set database URI with name and password: ::

    %cypher http://user:passwd@localhost:7474/db/data

Set database URI and return all nodes: ::

    %%cypher http://localhost:7474/db/data
    MATCH (n) RETURN n

Create a node using the most recently configured database (or the default if
none was specified: ::

    %cypher CREATE (n {name: 'foo'}) RETURN n

Retrieve properties of several nodes: ::

    results = %cypher MATCH (n) RETURN n
    print([result.n.properties for result in results])

Development
-----------
The latest release of the package may be obtained from
`GitHub <https://github.com/lebedov/icypher>`_.

Author
------
See the included `AUTHORS.rst
<https://github.com/lebedov/icypher/blob/master/AUTHORS.rst>`_ file for more 
information.

License
-------
This software is licensed under the
`BSD License <http://www.opensource.org/licenses/bsd-license>`_.
See the included `LICENSE.rst
<https://github.com/lebedov/icypher/blob/master/LICENSE.rst>`_ file for more information.
