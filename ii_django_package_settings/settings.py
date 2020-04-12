from importlib import import_module

from django.conf import settings


def perform_import(val, setting_name, setting_label):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name, setting_label)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(
            item, setting_name, setting_label) for item in val]
    return val


def import_from_string(val, setting_name, setting_label):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}' for {} setting '{}'. {}: {}.".format(
            val, setting_label, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class PackageSettings(object):
    """
    A settings object, that allows Package settings to be accessed as
    properties.

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    NAME = None
    DEFAULTS = ()
    IMPORT_STRINGS = ()
    REMOVED_SETTINGS = ()

    def __init__(self, user_settings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = self.DEFAULTS
        self.import_strings = self.IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, self.NAME, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid {} setting: "{}"'.format(
                self.NAME, attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr, self.NAME)

        # Cache the result
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in self.REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    'The "{}" setting has been removed. Please refer to "{}" '
                    'for available settings.'.format(
                        setting, self.SETTINGS_DOC))
        return user_settings
