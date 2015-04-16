"""Setup script."""

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.getcwd(), *rnames)).read()


setup(
    name="rod.recipe.appengine",
    version=read('version.txt').strip(),
    author="Tobias Rodaebel",
    author_email="tobias.rodaebel@googlemail.com",
    description="ZC Buildout recipe for setting up a Google App Engine "
                "development environment.",
    license="LGPL 3",
    keywords="appengine gae zc.buildout recipe zope",
    url='http://code.google.com/p/rodrecipes',
    long_description=(
        read('README.txt')
        + '\n' +
        read('src', 'rod', 'recipe', 'appengine', 'README.txt')
        + '\n' +
        read('CHANGES.txt')
        ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    package_data={'rod.recipe.appengine': ['README.txt']},
    namespace_packages=['rod', 'rod.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        ],
    entry_points={'zc.buildout': ['default = rod.recipe.appengine:Recipe']},
    zip_safe=False,
    )
