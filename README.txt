=====================
Simple Connecton Pool
=====================

A simple connection pool handler that maintains a pool of connection objects
(of whatever type you specify) attached to each thread.

This was designed for managing oursql database connections in a thread-safe
manner (under a multithreaded wsgi server) but will work for anything that
needs a thread-safe connection manager.

Sample usage
~~~~~~~~~~~~

::

    from mylibrary import MyConnectionClass
    from cpool import Pool

    PoolFactory = Pool(MyConnectionClass)
    PoolFactory.configure(host = 'myhost', port = '12345')
    conn = PoolFactory()
    conn.do_comething()

Download
~~~~~~~~

* https://github.com/ex-nerd/cpool
* http://pypi.python.org/pypi/cpool/
