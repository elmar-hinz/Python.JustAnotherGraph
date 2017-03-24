from distutils.core import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Read version from central version file
with open(path.join(here, 'version.txt'), encoding='utf-8') as f:
    version = f.read().strip()

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jag',
    version=version,
    description='Just Another Graph',
    long_description=long_description,
    keywords='education challenges bioinformatics Coursera Stepik Rosalind',
    url='https://github.com/elmar-hinz/Python.JustAnotherGraph',
    author='Elmar Hinz',
    author_email='t3elmar@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=['jag'],
    package_data={'jag': ['version.txt'], },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
