.. -*- rst -*-

ICypher
=======

Package Description
-------------------
ICypher is an IPython extension for running Cypher queries against a Neo4J
graph database within IPython.

.. image:: https://img.shields.io/pypi/v/icypher.svg
    :target: https://pypi.python.org/pypi/icypher
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/icypher.svg
    :target: https://pypi.python.org/pypi/icypher
    :alt: Downloads

Installation
------------
The package may be installed as follows: ::

    pip install icypher

After installation, the extension may be loaded within an IPython session
with ::

    %load_ext icypher

Usage Examples
--------------
Set database URI and return all nodes: ::

    %%cypher http://localhost:7474/db/data
    MATCH (n) RETURN n

Create a node using the most recently configured database (or the default if
none was specified: ::

    %cypher CREATE (n {name: 'foo'}) RETURN n

Development
-----------
The latest release of the package may be obtained from
`GitHub <https://github.com/lebedov/icypher>`_.

Author
------
See the included AUTHORS.rst file for more information.

License
-------
This software is licensed under the
`BSD License <http://www.opensource.org/licenses/bsd-license>`_.
See the included LICENSE.rst file for more information.
