class NotFitSchemaError(Exception):
    """The data doesn't fit with the pre-defined schema.
    """
    pass


class NotAvailableFileError(Exception):
    """File does not exist or can't be found.
    """
    pass


class NotInJsonFormatError(Exception):
    """File not in Json format for parsing stuffs
    """
    pass


class NullFilterConditionError(Exception):
    """Null params for filtering stuffs
    """
    pass


class NotSupportedTypeError(Exception):
    """Type not in our supported list
    """
    pass


class NotExistFieldNameError(Exception):
    """Field name does not exist in the headers
    """
    pass


class NotAvailableValueError(Exception):
    """Data constraints not include negative number or double/float
    """
    pass
