"""
A simple connection pool handler that maintains a pool of connection objects
(of whatever class you specify) attached to each thread.

Sample usage::

    from mylibrary import MyConnectionClass
    from cpool import Pool

    MyPool= Pool(MyConnectionClass)
    MyPool.configure(host = 'myhost', port = '12345')
    conn = MyPool()
    conn.do_comething()
"""

try:
    import threading
except ImportError:
    import dummy_threading as threading


class Pool(object):
    """
    Simple Connection pool based on sqlalchemy.orm.ScopedSession and
    sqlalchemy.util.ThreadLocalRegistry

    @todo Option to function as a queue-based pool so we can limit the total
          number of conections instead of just ending up with one per
          thread.  Or maybe bring in stuff from sqlalchemy's ScopedSession.

    @todo Add features like SQLAlchemy's Pool.recycle that will provide new
          connections if enough time has lapsed between requests.  See
          sqlalchemy/pool.py
    """

    def __init__(self, connection):
        self.registry = threading.local()
        # If the specified connection is actually a class, put it inside of
        # our Connection object so that it can be configured and instantiated
        # properly later.
        if type(connection) is type:
            self.factory = self._connection_maker(connection)
        # Otherwise, assume the developer knows what he/she is doing.
        else:
            self.factory = connection

    def __call__(self, **kwargs):
        if kwargs:
            self.registry.connection = self.factory(**kwargs)
        else:
            try:
                return self.registry.connection
            except AttributeError:
                self.registry.connection = self.factory()
        return self.registry.connection

    def configure(self, **kwargs):
        """
        Reconfigure the connection_maker used by this ConnectionPool.
        """
        if hasattr(self.registry, "connection"):
            warn('At least one connection is already present.  configure()'
                 ' cannot affect sessions that have already been created.')
        self.factory.configure(**kwargs)

    def _connection_maker(self, cls, **kwargs):
        """
        This method monkey-patches the provided class into our own special
        connection class, and then returns the hybrid.  This allows us to store
        configuration arguments when the pool is created, without actually
        instantiating the connection itself until the user requests it from
        the pool later.
        """
        class CPoolConnection(object):
            def __init__(self, **local_kwargs):
                for k in kwargs:
                    local_kwargs.setdefault(k, kwargs[k])
                super(CPoolConnection, self).__init__(**local_kwargs)
            @classmethod
            def configure(self, **new_kwargs):
                """
                (Re)configure the arguments for this CPoolConnection.

                e.g.::

                    Connection = cpool.Pool(MyClass)
                    Connection.configure(kwarg1 = "value1")
                """
                kwargs.update(new_kwargs)

        return type('CPoolConnection', (CPoolConnection, cls), {})
