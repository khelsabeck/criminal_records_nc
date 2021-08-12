from src.defendant import Defendant
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def d1():
    d1 = Defendant("John", "Smith", date(2010,1, 1))
    return d1

def test_initialization():
    '''This tests an initialization with valid data.'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    assert "John" == my_defendant._first
    assert "John" == my_defendant.first
    assert "Smith" == my_defendant._last
    assert "Smith" == my_defendant.last
    assert date(2010,1, 1) == my_defendant._birthdate
    assert date(2010,1, 1) == my_defendant.birthdate

def test_set_first_over25():
    '''This tests that only the first 25 chars of a first name are included'''
    my_defendant = Defendant("aaaaaaaaaaaaaaaaaaaaaaaabc", "Smith", date(2010,1, 1))
    assert "aaaaaaaaaaaaaaaaaaaaaaaab" == my_defendant._first
    assert "aaaaaaaaaaaaaaaaaaaaaaaab" == my_defendant.first

def test_set_first_noncontiguous():
    '''This tests that a non-contiguous string for a first name yields the appropriate error.'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("a a", "Smith", date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_set_first_tooshort():
    '''This tests that a string of zero length will not set and will raise the appropriate error'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("", "Smith", date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_set_first_non_string():
    '''This tests that a non-string inut for first will not set and will raise the appropriate error'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant(42, "Smith", date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_property_first_setter():
    '''This tests the property.setter for first.'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    assert "John" == my_defendant._first
    assert "John" == my_defendant.first
    my_defendant.first = "Mike"
    assert "Mike" == my_defendant._first
    assert "Mike" == my_defendant.first

def test_set_last_over25():
    '''This tests that only the first 25 chars of a last name are included'''
    my_defendant = Defendant("John", "aaaaaaaaaaaaaaaaaaaaaaaabc", date(2010,1, 1))
    assert "aaaaaaaaaaaaaaaaaaaaaaaab" == my_defendant._last
    assert "aaaaaaaaaaaaaaaaaaaaaaaab" == my_defendant.last

def test_set_last_noncontiguous():
    '''This tests that a non-contiguous string for a last name yields the appropriate error.'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("John", "a a", date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_set_last_tooshort():
    '''This tests that a last name of zero length will not set and will raise the appropriate error'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("John", "", date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_set_first_non_string():
    '''This tests that a non-string inut for first will not set and will raise the appropriate error'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("John", 42, date(2010,1, 1))
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_set_birthdate():
    '''This tests that a non-string inut for first will not set and will raise the appropriate error'''
    with pytest.raises(Exception) as exc_info:
        my_defendant = Defendant("John", "Smith", "bad input")  # test from init
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The birthdate must be a datetime date object." in str(exc_info.__dict__)
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    with pytest.raises(Exception) as exc_info:
        my_defendant.birthdate = "bad_data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The birthdate must be a datetime date object." in str(exc_info.__dict__)
    assert date(2010,1, 1) == my_defendant._birthdate
    assert date(2010,1, 1) == my_defendant.birthdate
    with pytest.raises(Exception) as exc_info:
        my_defendant.set_birthdate("bad_data")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The birthdate must be a datetime date object." in str(exc_info.__dict__)
    assert date(2010,1, 1) == my_defendant._birthdate
    assert date(2010,1, 1) == my_defendant.birthdate


def test_property_birthdate_setter():
    '''This tests the property.setter for birthdate resetting a valid value'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    assert date(2010,1, 1) == my_defendant._birthdate
    assert date(2010,1, 1) == my_defendant.birthdate
    new_date = date(2010,1, 2)
    my_defendant.birthdate = new_date
    assert date(2010,1, 2) == my_defendant._birthdate
    assert date(2010,1, 2) == my_defendant.birthdate


def test_property_fullname():
    '''This tests the return of the property fullname.'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    assert "John Smith" == my_defendant.fullname

def test_validate_contiguous_str():
    '''This should test the validation of a contiguous string with the helper method.'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    with pytest.raises(Exception) as exc_info:
        my_defendant.validate_contiguous_str('')    # too short
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        my_defendant.validate_contiguous_str(42)    # wrong type
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        my_defendant.validate_contiguous_str('a a') # whitespace between chars
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_last_setter():
    '''This tests the last setter. requires a contiguous string with no intervening whitespace, non-zero length'''
    my_defendant = Defendant("John", "Smith", date(2010,1, 1))
    my_defendant.last = "Helsabeck"
    assert "Helsabeck" == my_defendant.last
    assert "Helsabeck" == my_defendant._last
    with pytest.raises(Exception) as exc_info:
        my_defendant.last = ''    # too short
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        my_defendant.last =42    # wrong type
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        my_defendant.last = 'a a' # whitespace between chars
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)