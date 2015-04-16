"""Setup script."""

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.getcwd(), *rnames)).read()


setup(
    name="rod.recipe.mongodb",
    version=read('version.txt').strip(),
    author="Tobias Rodaebel",
    author_email="tobias (dot) rodaebel (at) googlemail (dot) com",
    description="ZC Buildout recipe for setting up mongoDB.",
    license="LGPL 3",
    keywords="mongodb zc.buildout recipe",
    url='http://pypi.python.org/pypi/rod.recipe.mongodb',
    long_description=(
        read('README.txt')
        + '\n' +
        read('src', 'rod', 'recipe', 'mongodb', 'README.txt')
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
    package_data={'rod.recipe.mongodb': ['README.txt']},
    namespace_packages=['rod', 'rod.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        ],
    entry_points={'zc.buildout': ['default = rod.recipe.mongodb:Recipe']},
    zip_safe=False,
    )
