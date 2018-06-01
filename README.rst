=====================
django-link-shortener
=====================

django-link-shortener is a simple time and usage sensitive url shortening app

Quick start
-----------
    
1. pip install git+git://github.com/ronaldgrn/django-link-shortener.git#egg=django-link-shortener
   
   or
   
   pip install --user django-link-shortener/dist/django-link-shortener-0.1.tar.gz
   
2. Add "shortener" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'shortener',
    ]

3. Include the polls URLconf in your project urls.py like this::

    path('s/', include('shortener.urls')),

4. Run `python manage.py migrate` to create the shortener models.

5. Start the development server and visit http://127.0.0.1:8000/s/
   to create a test link

6. Visit http://127.0.0.1:8000/<insert_test_code_here>/ to be redirected
