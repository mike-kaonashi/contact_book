import unittest
from unittest.mock import Mock, MagicMock
from contactbook import ContactBook
from contactbook.helpers.datahelper import TypeEnum
from contactbook.errors.exceptions \
    import NotAvailableFileError, NotInJsonFormatError, \
    NotFitSchemaError, NullFilterConditionError, \
    NotSupportedTypeError, NotAvailableValueError


class TestCreateFunction(unittest.TestCase):

    def test_add_blank(self):
        ...

    def test_add_lack_props(self):
        ...

    def test_add_wrong_format(self):
        ...

    def test_add_perfect(self):
        agent = ContactBook
        actual_obj = ('Test', '0123456789', 'KMS', 'HCM', 23)
        expect_obj = {'name': 'Test', 'phone': '0123456789', 'company': 'KMS', 'address': 'HCM', 'age': '23'}
        #
        # agent.add = MagicMock(return_value=expect_obj)
        # agent.add(*actual_obj)

        self.assertEqual(agent.add(*actual_obj), expect_obj)
        print('ok')

class TestGetFunction(unittest.TestCase):
    def test_list_perfect(self):
        ...
        # self.assertCountEqual()


class TestFilterFunction(unittest.TestCase):
    def test_none_params(self):
        self.assertIsNone(ContactBook.age_filter())

    def test_age_not_number_format(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte='string')

    def test_age_not_positive_number(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte=-5)

    def test_age_not_integer_format(self):
        with self.assertRaises(NotAvailableValueError):
            ContactBook.age_filter(age_gte=5.9)

    def test_filter_perfect(self):
        ...
        # self.assertCountEqual()
