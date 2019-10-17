import unittest
import collections
from unittest.mock import Mock, MagicMock, mock_open, patch
from contactbook import ContactBook
from contactbook.helpers.datahelper import TypeEnum
from contactbook.errors.exceptions \
    import NotAvailableFileError, NotInJsonFormatError, \
    NotFitSchemaError, NullFilterConditionError, \
    NotSupportedTypeError, NotAvailableValueError

headers = "name phone company address age"
values = ["Hieu", "0128493281", "Global", "Phu Yen", 27]


class TestCreateFunction(unittest.TestCase):

    @patch("json.dump")
    @patch("json.load")
    @patch("builtins.open")
    def test_add_blank(self, m_open, m_load, m_dump):
        m_open.return_value = MagicMock()
        m_load.return_value = [{}]
        m_dump.return_value = ''
        with self.assertRaises(NotFitSchemaError):
            ContactBook.add()

    @patch("json.dump")
    @patch("json.load")
    @patch("builtins.open")
    def test_add_lack_props(self, m_open, m_load, m_dump):
        input_ = ('Minh', '0123456789', 'KMS', 'HCM')
        m_open.return_value = MagicMock()
        m_load.return_value = [{}]
        m_dump.return_value = ''
        with self.assertRaises(NotFitSchemaError):
            ContactBook.add(*input_)

    @patch("json.dump")
    @patch("json.load")
    @patch("builtins.open")
    def test_add_wrong_format(self, m_open, m_load, m_dump):
        input_ = (1, 1, 1, 1, 1)
        m_open.return_value = MagicMock()
        m_load.return_value = [{}]
        m_dump.return_value = ''
        with self.assertRaises(NotFitSchemaError):
            ContactBook.add(*input_)

    @patch("json.dump")
    @patch("json.load")
    @patch("builtins.open")
    def test_add_perfect(self, m_open, m_load, m_dump):
        expect = {'name': 'Minh',
                  'phone': '0123456789',
                  'company': 'KMS',
                  'address': 'HCM',
                  'age': '23'}
        m_open.return_value = MagicMock()
        m_load.return_value = [{}]
        m_dump.return_value = ''
        input_ = ('Minh', '0123456789', 'KMS', 'HCM', 23)
        actual = ContactBook.add(*input_)
        assert actual['name'] == expect['name']
        assert actual['phone'] == expect['phone']
        assert actual['company'] == expect['company']
        assert actual['address'] == expect['address']
        assert actual['age'] == expect['age']


class TestFilterFunction(unittest.TestCase):
    expect = collections.namedtuple('Object', headers)
    expect = expect._make(values)

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

    @patch("json.load")
    @patch("builtins.open")
    def test_filter_perfect(self, m_open, m_json):
        m_open.return_value
        m_json.return_value = [{'name': 'Hieu',
                                'phone': '0128493281',
                                'company': 'Global',
                                'address': 'Phu Yen',
                                'age': '27'}]
        actual = ContactBook.age_filter(age=27)
        assert len(actual) == 1
        assert getattr(actual[0], 'name') == getattr(self.expect, 'name')
        assert getattr(actual[0], 'phone') == getattr(self.expect, 'phone')
        assert getattr(actual[0], 'company') == getattr(self.expect, 'company')
        assert getattr(actual[0], 'address') == getattr(self.expect, 'address')
        assert getattr(actual[0], 'age') == getattr(self.expect, 'age')
