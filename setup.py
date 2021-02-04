import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='rdf_orm',
    version='0.2.0',
    author='Edmond Chuc',
    author_email='e.chuc@uq.edu.au',
    description='Express RDF classes as Python classes with full Python annotation support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ternaustralia/rdf-orm',
    packages=setuptools.find_packages(),
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        'rdflib',
    ]
)