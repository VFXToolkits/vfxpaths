#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''Custom error classes.'''

class VFXBaseError(Exception):
    """Vfx paths error"""


class AnalyseError(VFXBaseError):
    '''Raised when the path cannot be resolved'''


class AnalyseEevError(VFXBaseError):
    '''Error parsing environment variable to true path'''


class FormatError(VFXBaseError):
    '''Raised when data cannot be formatted as a path'''


class NotFound(VFXBaseError):
    '''Raise when an item cannot be found.'''


class ResolveError(VFXBaseError):
    '''Raise when a template reference can not be resolved.'''

