from distutils.core import setup

setup(
    name='Later',
    version='0.1.0',
    author='Milan Cermak',
    author_email='milan.cermak@gmail.com',
    packages=['later'],
    scripts=[],
    url='http://pypi.python.org/pypi/Later/',
    license='LICENSE.txt',
    description='A simple in-process thread-safe scheduler.',
    long_description=open('README.rst').read()
)
