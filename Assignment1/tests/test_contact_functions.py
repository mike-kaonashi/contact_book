import unittest
from contactbook import ContactBook
from contactbook.helpers.datahelper import TypeEnum
from contactbook.helpers.datahelper \
    import FileNotAvailableError, NotInJsonFormatError, \
    NotFitSchemaError, NullFilterConditionError, \
    TypeNotSupportedError, NotAvailableValueError


class TestCreateFunction(unittest.TestCase):

    def test_add_blank(self):
        ...

    def test_add_lack_props(self):
        ...

    def test_add_wrong_format(self):
        ...

    def test_add_perfect(self):
        self.assertEqual(
            ContactBook.add('David', '0123456789', 'KMS', 'HCM city', 23),
            {
                'name': 'David',
                'phone': '0123456789',
                'company': 'KMS',
                'address': 'HCM city',
                'age': '23'
            }
        )


class TestGetFunction(unittest.TestCase):
    def test_list_perfect(self):
        ...


class TestFilterFunction(unittest.TestCase):
    def test_none_params(self):
        ...

    def test_age_not_number_format(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte='string')

    def test_age_not_positive_number(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte=-5)

    def test_age_not_integer_format(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte=5.9)

    def test_lack_of_params(self):
        ...

    def test_filter_perfect(self):
        ...
