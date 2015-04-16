A brief documentation
=====================

This recipe takes a number of options:

erlang-path
    The path where to find the erlc command (default = find it in PATH).

url
    The URL to download the RabbitMQ source distribution.

cookie 
    Optional string passed as cookie to the erl runtime (-setcookie).

make
    Alternate make command (e.g. gmake).

To further customize your RabbitMQ server configuration, create a rabbitmq-env
file in the etc/ directory of your buildout, following the `RabbitMQ
configuration guide`_ to set environment variables.

You can also create a rabbitmq.config file in the same location to provide
erlang configuration statements.

.. _RabbitMQ configuration guide: http://www.rabbitmq.com/configure.html


Tests
=====

We will define a buildout template used by the recipe:

    >>> buildout_cfg = """
    ... [buildout]
    ... parts = rabbitmq
    ... offline = true
    ...
    ... [rabbitmq]
    ... recipe = rod.recipe.rabbitmq
    ... url = http://www.rabbitmq.com/releases/rabbitmq-server/v2.4.1/rabbitmq-server-2.4.1.tar.gz
    ... """

We'll start by creating a buildout:

    >>> import os.path
    >>> write('buildout.cfg', buildout_cfg)

Running the buildout gives us:

    >>> output = system(buildout)
    >>> if output.endswith("ebin ebin/rabbit.app < ebin/rabbit_app.in\n"): True
    ... else: print output
    True
