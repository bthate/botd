class EJSON(Exception):
    """wrong json."""

class ENOCLASS(Exception):
    """no such class."""

class ENOFILE(Exception):
    """no such file."""

class EOVERLOAD(Exception):
    """overloading is not permitted."""

class ETYPE(Exception):
    """wrong type."""

class EINIT(Exception):
    """ error occured during initialisation. """

class ENOMODULE(Exception):
    """ module could not be found. """

class ENOTXT(Exception):
    """ no text provided. """
