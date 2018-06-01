import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-link-shortener',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django Link Shortener.',
    long_description=README,
    url='https://github.com/ronaldgrn/django-link-shortener',
    download_url='https://github.com/ronaldgrn/django-link-shortener/archive/0.2.tar.gz',
    author='Petronald Green',
    author_email='petronaldgreen@gmail.com',
    keywords = ['url shortener', 'link shortener'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)