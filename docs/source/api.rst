API documentation
=======================

Analysis
-------------
.. automodule:: structuregraph_helpers.analysis
    :members:

Create
--------------
.. automodule:: structuregraph_helpers.create
    :members:

Delete
---------
.. automodule:: structuregraph_helpers.delete
    :members:

Plotting
---------------
.. automodule:: structuregraph_helpers.plotting
    :members:

Subgraph
-----------
.. automodule:: structuregraph_helpers.subgraph
    :members:

Hash
------- -
.. automodule:: structuregraph_helpers.hash
    :members:



Logging 
---------

structuregraph_helpers uses the `loguru <https://loguru.readthedocs.io/en/stable/index.html>`_  for logging. 
By default, logging from structuregraph_helpers is disabled to not interfere with your logs.

However, you can easily customize the logging:

.. code-block:: python

    import sys
    from loguru import logger

    # enable structuregraph_helpers logging 
    logger.enable("structuregraph_helpers")
    
    # define the logging level
    LEVEL = "INFO || DEBUG || WARNING || etc."

    # set the handler
    # for logging to stdout
    logger.add(sys.stdout, level=LEVEL) 
    # or for logging to a file
    logger.add("my_log_file.log", level=LEVEL, enqueue=True) 


In many cases, however, you might find it convenient to simply call :py:meth:`~structuregraph_helpers.utils.enable_logging`

.. code-block:: python

    from structuregraph_helpers.utils import enable_logging

    enable_logging()

which will enable logging with sane defaults (i.e. logging to ``stderr`` for ``INFO`` and ``WARNING`` levels).