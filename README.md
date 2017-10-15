# ideallical Django package settings

[![pypi-version]][pypi]

## Acknowledgments

This package is heavily inspired by [django-restframework] settings.

## Requirements

* Python (3.5)

## Installation in your Django package

Install in your package's `setup.py`:
```python
setup(
    [..]
    install_requires=[
        'ii-django-package-settings>=0.1'
    ],
    [..]
)
```

## Configuration for your Django package

Create a `settings.py` file in the root of your package with the following
content (based on [ii-django-backup]):

```python
from ii_django_package_settings.settings import PackageSettings


class BackupSettings(PackageSettings):
    NAME = 'II_DJANGO_BACKUP'
    DOC = 'https://github.com/ideallical/ii-django-backup/'
    DEFAULTS = {
        'NAME_GENERATOR_FUNC': 'ii_django_backup.name_generators.default',
        'DROPBOX_ACCESS_TOKEN': None,
        'DROPBOX_DIR': None,
        'USE_GZIP': True,
    }
    IMPORT_STRINGS = ('NAME_GENERATOR_FUNC', )
    REMOVED_SETTINGS = ()


backup_settings = BackupSettings(None)
```

Then in your package you can refer to these settings like so:
```python
from ii_django_backup.settings import backup_settings


backup_settings.DROPBOX_ACCESS_TOKEN
```

[pypi-version]: https://img.shields.io/pypi/v/ii-django-package-settings.svg
[pypi]: https://pypi.python.org/pypi/ii-django-package-settings
[django-restframework]: https://github.com/encode/django-rest-framework
[ii-django-backup]: https://github.com/ideallical/ii-django-backup
