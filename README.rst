=====================
django-link-shortener
=====================

django-link-shortener is a simple time and usage quantity sensitive 
url shortening app

Quick start
-----------

1. Add "shortener" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'shortener',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('s/', include('shortener.urls')),

3. Run `python manage.py migrate` to create the shortener models.

4. Start the development server and visit http://127.0.0.1:8000/s/
   to create a test link

5. Visit http://127.0.0.1:8000/<insert_test_code_here>/ to be redirected