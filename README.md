# django-polls

[![Build status](https://travis-ci.org/byteweaver/django-polls.svg?branch=master)](https://travis-ci.org/byteweaver/django-polls)

A simple and reusable polls application for django.

## Key features

* basic poll handling (poll, choices, votes)
* easy to extend

## Installation

If you want to install the latest stable release from PyPi:

    $ pip install django-polls

If you want to install the latest development version from GitHub:

    $ pip install -e git://github.com/byteweaver/django-polls#egg=django-polls

Add `polls` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'polls',
        ...
    )

Hook this app into your ``urls.py``:

    urlpatterns = patterns('',
        ...
        url(r'^polls/', include('polls.urls', namespace='polls')),
        ...
    )
