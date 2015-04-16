====================
rod.recipe.appengine
====================

The rod.recipe.appengine is a zc.buildout recipe to build, test and deploy
projects for the Google App Engine. It makes it easy to use eggs and resolve
their dependencies automatically.

To be honest, this is a recipe for scrambled eggs. It produces a zip file
containing all configured external packages in a traditional folder hierarchy.


Copyright and license
=====================

Copyright 2009, 2010, 2011 Tobias Rodaebel

This software is released under the GNU Lesser General Public License,
Version 3.


Credits
=======

Thanks to Attila Olah who provided a patch which fixes two issues where the
recipe wasn't able to find the original pkg_resources.py file. He also enabled
the recipe to be used together with distribute as a replacement for setuptools.

Attila Olah also provided a patch for supporting regular expressions when using
the exclude option.

Thanks to Tom Lynn for submitting a patch which fixes an issue with symlink on
platforms other than UNIX.

Lots of thanks to Gael Pasgrimaud for submitting a patch that allows for
zc.recipe.egg options such as extra-paths and entry-points.
