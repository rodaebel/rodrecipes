A brief documentation
=====================

This recipe takes a number of options:

darwin-32bit-url
    The URL to download the 32 bit binary package for the darwin platform.

darwin-64bit-url
    The URL to download the 64 bit binary package for the darwin platform.

linux2-32bit-url
    The URL to download the 32 bit binary package for the linux platform.

linux2-64bit-url
    The URL to download the 64 bit binary package for the linux platform.

(And all options of mongod version v1.6.0 as described below.)
 

Tests
=====

We will define a buildout template used by the recipe:

    >>> buildout_cfg = """
    ... [buildout]
    ... parts = mongodb
    ...
    ... [mongodb]
    ... recipe = rod.recipe.mongodb
    ... darwin-32bit-url = http://downloads.mongodb.org/osx/mongodb-osx-i386-1.6.5.tgz
    ... darwin-64bit-url = http://downloads.mongodb.org/osx/mongodb-osx-x86_64-1.6.5.tgz
    ... linux2-32bit-url = http://downloads.mongodb.org/linux/mongodb-linux-i686-1.6.5.tgz
    ... linux2-64bit-url = http://downloads.mongodb.org/linux/mongodb-linux-x86_64-1.6.5.tgz
    ... """

We'll start by creating a buildout:

    >>> import os.path
    >>> write('buildout.cfg', buildout_cfg)

Running the buildout gives us:

    >>> output = system(buildout)
    >>> 'rod.recipe.mongodb: downloading mongoDB distribution...' in output
    True

Check whether the binaries are copied:

    >>> set(os.listdir('bin')).issuperset(['mongo', 'mongod', 'mongodump', 'mongoexport', 'mongofiles', 'mongoimport', 'mongorestore', 'mongos', 'mongosniff', 'mongostat'])
    True

A start script with the format 'start_PART-NAME_mongod.sh' should be generated.

    >>> 'start_mongodb_mongod.sh' in os.listdir('bin')
    True

It is possible to change the name of this start script with the 'script_name'
option. Furthermore all options of mongod (version v1.6.0) are supported via
buildout options. A more comprehensive recipe could be for example:
    
    >>> buildout_cfg = """
    ... [buildout]
    ... parts = mongodb
    ... [mongodb]
    ... recipe = rod.recipe.mongodb
    ... darwin-32bit-url = http://downloads.mongodb.org/osx/mongodb-osx-i386-1.6.5.tgz
    ... darwin-64bit-url = http://downloads.mongodb.org/osx/mongodb-osx-x86_64-1.6.5.tgz
    ... linux2-32bit-url = http://downloads.mongodb.org/linux/mongodb-linux-i686-1.6.5.tgz
    ... linux2-64bit-url = http://downloads.mongodb.org/linux/mongodb-linux-x86_64-1.6.5.tgz
    ... script_name = start_master.sh
    ... quiet=true
    ... fork=true
    ... logpath=${buildout:parts-directory}/mongodb/log
    ... dbpath=${buildout:parts-directory}/mongodb/data
    ... directoryperdb=true
    ... master=true
    ... update=true
    ... """

    >>> write('buildout.cfg', buildout_cfg)

Re-running the buildout:

    >>> output = system(buildout)
