=====================
django-link-shortener
=====================

.. image:: https://travis-ci.org/ronaldgrn/django-link-shortener.svg?branch=master
    :target: https://travis-ci.org/ronaldgrn/django-link-shortener
    
.. image:: https://img.shields.io/pypi/l/django-link-shortener.svg
    :alt: PyPI - License
    :target: https://pypi.org/project/django-link-shortener/

.. image:: https://img.shields.io/pypi/v/django-link-shortener.svg
    :alt: PyPI
    :target: https://pypi.org/project/django-link-shortener/

.. image:: https://coveralls.io/repos/github/ronaldgrn/django-link-shortener/badge.svg?branch=master
    :target: https://coveralls.io/github/ronaldgrn/django-link-shortener?branch=master


django-link-shortener is a simple time and usage sensitive url shortening app.

Uses A-Za-z0-9 with the exception of I, i and 1.

Requires user to be logged in for link creation.


Usage
-----
    
1. pip install django-link-shortener
   
2. Add "shortener" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'shortener',
    ]

3. Include the polls URLconf in your project urls.py like this::

    path('s/', include('shortener.urls')),

4. Run `python manage.py migrate` to create the shortener models.


Testing
-------
1. Add the following to settings

```
SHORTENER_ENABLE_TEST_PATH = True
```

1. Start the development server and visit http://127.0.0.1:8000/s/test/<My-URL-HERE>
   to create a test shortcode.

   or

   Use shortener.create(user, link) to generate a link via code. Use shortener.expand(link)
   to revert

6. Visit http://127.0.0.1:8000/s/<shortcode>/ to be redirected

Configuration Options
---------------------
Place in settings.py. Each setting be overridden on a per-user basis using the admin UrlProfile section

SHORTENER_ENABLED
  Default: True
  
  Controls whether users without a shortener profile can create shortlinks.
  
SHORTENER_MAX_URLS
  Default: -1
  
  Controls the default maximum limit of generated urls per account. 
  -1 sets infinite.
  
SHORTENER_MAX_CONCURRENT
  Default: -1
  
  Controls the default maximum limit of *concurrent* (active) generated urls per account.
  -1 sets infinite

SHORTENER_LIFESPAN
  Default: -1
  
  Sets the default lifespan of links in seconds
  -1 sets infinite
  
SHORTENER_MAX_USES
  Default: -1
  
  Sets the default amount of times a link can be followed
  -1 sets infinite
  
SHORTENER_LENGTH
  Default: 5
  
  Note: Omitted from UrlProfile
  
  Sets how many digits should be used for links. 
  Tries up to three times to generate a unique shortcode where
  Each failure will result in length temporaily being increased by 1.

SHORTENER_ENABLE_TEST_PATH
  Default: False

  If true, creates shortlinks for logged in users at s/test/<<url>>/

  The response is the shortcode to use used at s/<<shortcode>>


Common Use Cases
----------------
goo.gl type usage (default). Unlimited concurrent links for an unlimited length of time

::

  SHORTENER_ENABLED = True
  SHORTENER_MAX_URLS = -1
  SHORTENER_MAX_CONCURRENT = -1
  SHORTENER_LIFESPAN = -1
  SHORTENER_MAX_USES = -1
  
  
Internal temporary link usage (such as on nodeferret.com). 100 Temp links per minute. 1 usage per link.

::

  SHORTENER_ENABLED = True
  SHORTENER_MAX_URLS = -1
  SHORTENER_MAX_CONCURRENT = 100 # To prevent spamming
  SHORTENER_LIFESPAN = 600
  SHORTENER_MAX_USES = 1


Changelog
---------

**v0.4**

- Allow null values in UrlProfile; null fields will use global values
- str representation of UrlProfile in admin
- add user to str representation of UrlMap
- removed 256 char limit on full_url (Credit: Khaeshah)

Upgrade Instructions
--------------------

**0.3 -> 0.4**

::

  pip install django-link-shortener==0.4
  python manage.py migrate