# BOTD - python3 IRC channel daemon.
#
# errors. 

""" errors that could be raised. """

class EOVERLOAD(Exception):

    """ item is already available. """

    pass

class EBLOCKING(Exception):

    """ blocking error. """

    pass

class ENOCLASS(Exception):

    """ class cannot be found. """

    pass

class ECLASS(Exception):

    """ wrong class. """

    pass

class EDEBUG(Exception):

    """ debug error. """

    pass

class EEMPTY(Exception):

    """ no data provided. """

    pass

class EJSON(Exception):

    """ json decode/encode error. """

    pass

class ENOFILE(Exception):

    """ no file found. """

    pass

class ENOFUNCTION(Exception):

    """ function is not provided. """

    pass

class ENOMODULE(Exception):

    """ no module found. """

    pass

class ENOTFOUND(Exception):

    """ item cannot be found. """

    pass

class ENOTIMPLEMENTED(Exception):

    """ method is not implemented. use method overloading. """

    pass

class ENOTXT(Exception):

    """ empty string was entered. """

    pass

class ENOUSER(Exception):

    """ no matching user found. """

    pass

class ENOTYPE(Exception):

    """ no type provided. """

    pass

class ETYPE(Exception):

    """ wrong type. """

    pass

class EOWNER(Exception):

    """ is not owner. """

    pass

class ERESERVED(Exception):

    """ is a reserved word. """

    pass

class ESET(Exception):

    """ cannot set item. """

    pass

class EINIT(Exception):

    """ initialisation problem. """
