# django-link-shortener

[![image](https://github.com/ronaldgrn/django-link-shortener/actions/workflows/django-tests.yml/badge.svg)](https://github.com/ronaldgrn/django-link-shortener/actions/workflows/django-tests.yml)
[![PyPI - License](https://img.shields.io/pypi/l/django-link-shortener.svg)](https://pypi.org/project/django-link-shortener/)
[![PyPI](https://img.shields.io/pypi/v/django-link-shortener.svg)](https://pypi.org/project/django-link-shortener/)
[![Codecov](https://img.shields.io/codecov/c/github/ronaldgrn/django-link-shortener?token=PQ19R9VGTP)](https://codecov.io/gh/ronaldgrn/django-link-shortener)


django-link-shortener is a Django app for creating time-limited and usage-capped short URLs.


## Features

*   Generate short links for URLs.
*   Time-sensitive links (configurable lifespan).
*   Usage-limited links (configurable maximum uses).
*   Per-user override of default settings via Django admin.
*   Test endpoint for easy shortcode creation during development.
*   Character set for shortcodes excludes I, i, 1.


## Usage

1.  Install with `pip install django-link-shortener`

2.  Add `shortener` to your INSTALLED_APPS setting:

    ```python
    INSTALLED_APPS = [
        ...
        'shortener',
    ]
    ```

3.  Include `shortener.urls` in your project urls.py:

    ```python
    path('s/', include('shortener.urls')),
    ```

4.  Run `python manage.py migrate` to create the shortener models.

5. Use `shortener.create(user, link)` to generate a shortcode.

    ```python
    from shortener import shortener
    
    user = User.objects.first()
    shortener.create(user, "https://example.com")
    ```

6. To expand the shortcode use `shortener.expand(shorlink_id)`, 
   or visit `http://127.0.0.1:8000/s/<shortcode>/`.


## Test Endpoint

1.  To enable the test endpoint, add the following to settings:
    ```python
    SHORTENER_ENABLE_TEST_PATH = True
    ```

2.  Start the development server and visit
    `http://127.0.0.1:8000/s/test/<my-url-here>` to create a test shortcode.

3. Visit `http://127.0.0.1:8000/s/<shortcode>/` to be redirected


## Configuration Options

Place in settings.py. Each setting can be overridden on a per-user basis
using the UrlProfile section in the Django admin.


**SHORTENER_ENABLED**  
Default: `True`

Controls whether users without a shortener profile can create shortlinks.


**SHORTENER_MAX_URLS**  
Default: `-1`

Controls the default maximum limit of generated urls per account.
-1 sets infinite.


**SHORTENER_MAX_CONCURRENT**  
Default: `-1`

Controls the default maximum limit of *concurrent* (active)
generated urls per account. -1 sets infinite.


**SHORTENER_LIFESPAN**  
Default: `-1`

Sets the default lifespan of links in seconds. -1 sets infinite.


**SHORTENER_MAX_USES**  
Default: `-1`

Sets the default amount of times a link can be followed. -1 sets infinite.


**SHORTENER_LENGTH**  
Default: `5`

Note: Omitted from UrlProfile.

Sets how many digits should be used for links. Tries up to three
times to generate a unique shortcode where Each failure will result
in length temporarily being increased by 1.


**SHORTENER_ENABLE_TEST_PATH**  
Default: `False`

If true, creates shortlinks on authenticated requests to `s/test/<url>/` 
and returns a shortcode.


## Common Use Cases

goo.gl type usage (default). Unlimited concurrent links for an unlimited
length of time

```python
SHORTENER_ENABLED = True
SHORTENER_MAX_URLS = -1
SHORTENER_MAX_CONCURRENT = -1
SHORTENER_LIFESPAN = -1
SHORTENER_MAX_USES = -1
```

Internal temporary link usage. 
100 active links with a lifespan of 1 hour. 1 usage per link.

```python
SHORTENER_ENABLED = True
SHORTENER_MAX_URLS = -1
SHORTENER_MAX_CONCURRENT = 100
SHORTENER_LIFESPAN = 600
SHORTENER_MAX_USES = 1
```



## Changelog

**v0.5**

-   Replaced NullBooleanField with BooleanField (Credit: sen-den)
-   Replaced travis-ci with github actions

**v0.4**

-   Allow null values in UrlProfile; null fields will use global values
-   str representation of UrlProfile in admin
-   add user to str representation of UrlMap
-   removed 256 char limit on full_url (Credit: Khaeshah)

