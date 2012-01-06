=====================
Simple Connecton Pool
=====================

A simple connection pool handler that maintains a pool of connection objects
(of whatever type you specify) attached to each thread.

Sample usage
~~~~~~~~~~~~

::

    from mylibrary import MyConnectionClass
    from cpool import CPool

    MyPool= CPool(MyConnectionClass)
    MyPool.configure(host = 'myhost', port = '12345')
    conn = MyPool()
    conn.do_comething()

Download
~~~~~~~~

* https://github.com/ex-nerd/cpool
* http://pypi.python.org/pypi/cpool/
