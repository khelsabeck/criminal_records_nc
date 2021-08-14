from src.conviction import Conviction
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def conviction1():
    conviction1 = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    return conviction1

def test_initialization():
    '''This tests an initialization with valid data.'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert "Simple Assault" == conviction._crime
    assert "Simple Assault" == conviction.crime
    assert "Class 2 Misdemeanor" == conviction.crime_class
    assert "Class 2 Misdemeanor" == conviction._crime_class
    assert date(2010,1, 1) == conviction.conviction_date
    assert date(2010,1, 1) == conviction._conviction_date
    assert "Randolph" == conviction.conviction_loc
    assert "Randolph" == conviction._conviction_loc
    assert "NCGS 14-33" == conviction._statute
    assert "NCGS 14-33" == conviction.statute


def test_set_crime_class():
    '''This tests an initialization with an invalid crime.'''
    with pytest.raises(Exception) as exc_info:
        conviction = Conviction("Simple Assault", "Bad data", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33") # and valid
    assert "Class 2 Misdemeanor" == conviction.crime_class
    assert "Class 2 Misdemeanor" == conviction._crime_class
    with pytest.raises(Exception) as exc_info:
        conviction.set_crime_class("bad data")
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    assert "Class 2 Misdemeanor" == conviction.crime_class
    assert "Class 2 Misdemeanor" == conviction._crime_class

def test_validate_contiguous_str():
    '''This tests the validate_contiguous_str method. It should only validate a string of non-zero length and that it has no whitespace between chars'''    
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert True == conviction.validate_contiguous_str("hello")    
    with pytest.raises(Exception) as exc_info:
        conviction.validate_contiguous_str("")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        conviction.validate_contiguous_str(42)
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        conviction.validate_contiguous_str("a a")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_crimeclass_property_andsetter():
    '''This tests the behavior of the property and setter. They should shunt the logic through the validation and prevent direct setting.'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    conviction.crime_class = "Class 3 Misdemeanor"
    assert "Class 3 Misdemeanor" == conviction.crime_class
    assert "Class 3 Misdemeanor" == conviction._crime_class
    with pytest.raises(Exception) as exc_info:
        conviction.crime_class = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    assert "Class 3 Misdemeanor" == conviction.crime_class
    assert "Class 3 Misdemeanor" == conviction._crime_class

def test_validate_convictiondate():
    '''This tests the validate_date method, ensuring the date is a datetime date object by type. If not, it should return the error: 
    ValueError("The dates of conviction and offense must be a valid datetime date objects.")'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    with pytest.raises(Exception) as exc_info:
        conviction.validate_date("bad data")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects." in str(exc_info.__dict__)

def test_validate_date_setter():
    '''This tests the validate_date *setter*, ensuring the date is a datetime date object by type. If not, it should return the error: 
    ValueError("The dates of conviction and offense must be a valid datetime date objects.")'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    with pytest.raises(Exception) as exc_info:
        conviction.conviction_date = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects." in str(exc_info.__dict__)

def test_set_crime():
    '''This tests the setter for the crime itself. Crime should be a non-zero length string of up to 50 chars'''
    conviction = Conviction("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), \
        "Randolph", "NCGS 14-33")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction._crime
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction.crime
    conviction.crime = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction._crime
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction.crime
    with pytest.raises(Exception) as exc_info:
        conviction.crime = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A crime should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        conviction.crime = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A crime should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)

def test_conviction_loc():
    '''This tests the setter for the conviction_loc itself. It should be a non-zero length string of up to 50 chars'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", \
        "NCGS 14-33")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction._conviction_loc
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction.conviction_loc
    conviction.conviction_loc = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction._conviction_loc
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction.conviction_loc
    with pytest.raises(Exception) as exc_info:
        conviction.conviction_loc = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A conviction location value should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        conviction.conviction_loc = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A conviction location value should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)

def test_statute():
    '''This tests the setter for the statute . It should be a non-zero length string of up to 50 chars'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "conviction location", \
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction._statute
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == conviction.statute
    conviction.statute = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction._statute
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == conviction.statute
    with pytest.raises(Exception) as exc_info:
        conviction.statute = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The Statute should be a string valud between 1 and 50 characters." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        conviction.statute = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The Statute should be a string valud between 1 and 50 characters." in str(exc_info.__dict__)

def test_offensedate():
    '''I refactored and added an offense date field to convictions. This tests the offense date, ensuring the date is a datetime date object by type. 
    If not, it should return the error: 
    ValueError("The conviction_date must be a valid datetime date object.")'''
    conviction = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert date(2009,1, 1) == conviction.offense_date
    with pytest.raises(Exception) as exc_info:
        conviction.offense_date = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects." in str(exc_info.__dict__)

def test_is_felony():
    '''This tests the added property is_felony, which returns true if the conviction is a felony, and otherwise false'''
    conviction1 = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert False == conviction1.is_felony
    conviction2 = Conviction("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert True == conviction2.is_felony

def test_is_misdemeanor():
    '''This tests the added property is_misdemeanor, which returns true if the conviction is a misdemeanor, and otherwise false'''
    conviction1 = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert True == conviction1.is_misdemeanor
    conviction2 = Conviction("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert False == conviction2.is_misdemeanor


def test_is_infraction():
    '''This tests the added property is_infraction, which returns true if the conviction is an infraction, and otherwise false'''
    conviction1 = Conviction("Speeding", "Infraction", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 20-141")
    assert True == conviction1.is_infraction
    conviction2 = Conviction("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert False == conviction2.is_infraction
