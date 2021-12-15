from src.charge import Charge
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def charge1():
    charge1 = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    return charge1

def test_initialization():
    '''This tests an initialization with valid data.'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert "Simple Assault" == charge._crime
    assert "Simple Assault" == charge.crime
    assert "Class 2 Misdemeanor" == charge.crime_class
    assert "Class 2 Misdemeanor" == charge._crime_class
    assert date(2010,1, 1) == charge.conviction_date
    assert date(2010,1, 1) == charge._conviction_date
    assert "Randolph" == charge.conviction_loc
    assert "Randolph" == charge._conviction_loc
    assert "NCGS 14-33" == charge._statute
    assert "NCGS 14-33" == charge.statute


def test_set_crime_class():
    '''This tests an initialization with an invalid crime.'''
    with pytest.raises(Exception) as exc_info:
        charge = Charge("Simple Assault", "Bad data", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33") # and valid
    assert "Class 2 Misdemeanor" == charge.crime_class
    assert "Class 2 Misdemeanor" == charge._crime_class
    with pytest.raises(Exception) as exc_info:
        charge.set_crime_class("bad data")
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    assert "Class 2 Misdemeanor" == charge.crime_class
    assert "Class 2 Misdemeanor" == charge._crime_class

def test_validate_contiguous_str():
    '''This tests the validate_contiguous_str method. It should only validate a string of non-zero length and that it has no whitespace between chars'''    
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert True == charge.validate_contiguous_str("hello")    
    with pytest.raises(Exception) as exc_info:
        charge.validate_contiguous_str("")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        charge.validate_contiguous_str(42)
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        charge.validate_contiguous_str("a a")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The value failed to validate. It should be a string of non-zero length with no whitespace." in str(exc_info.__dict__)

def test_crimeclass_property_andsetter():
    '''This tests the behavior of the property and setter. They should shunt the logic through the validation and prevent direct setting.'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    charge.crime_class = "Class 3 Misdemeanor"
    assert "Class 3 Misdemeanor" == charge.crime_class
    assert "Class 3 Misdemeanor" == charge._crime_class
    with pytest.raises(Exception) as exc_info:
        charge.crime_class = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The crime class is not a valid crime class. Valid Crime classes are" in str(exc_info.__dict__)
    assert "Class 3 Misdemeanor" == charge.crime_class
    assert "Class 3 Misdemeanor" == charge._crime_class

def test_validate_convictiondate():
    '''This tests the validate_date method, ensuring the date is a datetime date object by type. If not, it should return the error: 
    ValueError("The dates of conviction and offense must be a valid datetime date objects. conviction_date may be None if charge still pending.")'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    with pytest.raises(Exception) as exc_info:
        charge.validate_date("bad data")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects. conviction_date may be None if charge still pending."\
         in str(exc_info.__dict__)

def test_validate_date_setter():
    '''This tests the validate_date *setter*, ensuring the date is a datetime date object by type. If not, it should return the error: 
    ValueError("The dates of conviction and offense must be a valid datetime date objects. conviction_date may be None if charge still pending.")'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    with pytest.raises(Exception) as exc_info:
        charge.conviction_date = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects." in str(exc_info.__dict__)

def test_set_crime():
    '''This tests the setter for the crime itself. Crime should be a non-zero length string of up to 50 chars'''
    charge = Charge("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), \
        "Randolph", "NCGS 14-33")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge._crime
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge.crime
    charge.crime = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge._crime
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge.crime
    with pytest.raises(Exception) as exc_info:
        charge.crime = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A crime should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        charge.crime = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A crime should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)

def test_conviction_loc():
    '''This tests the setter for the conviction_loc itself. It should be a non-zero length string of up to 50 chars'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", \
        "NCGS 14-33")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge._conviction_loc
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge.conviction_loc
    charge.conviction_loc = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge._conviction_loc
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge.conviction_loc
    with pytest.raises(Exception) as exc_info:
        charge.conviction_loc = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A conviction location value should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        charge.conviction_loc = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "A conviction location value should be a string of non-zero length (up to 50 chars)." in str(exc_info.__dict__)

def test_statute():
    '''This tests the setter for the statute . It should be a non-zero length string of up to 50 chars'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "conviction location", \
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1")
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge._statute
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" == charge.statute
    charge.statute = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb1"
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge._statute
    assert "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" == charge.statute
    with pytest.raises(Exception) as exc_info:
        charge.statute = ""
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The Statute should be a string valud between 1 and 50 characters." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        charge.statute = 42
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The Statute should be a string valud between 1 and 50 characters." in str(exc_info.__dict__)

def test_offensedate():
    '''I refactored and added an offense date field to convictions. This tests the offense date, ensuring the date is a datetime date object by type. 
    If not, it should return the error: 
    ValueError("The conviction_date must be a valid datetime date object.")'''
    charge = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert date(2009,1, 1) == charge.offense_date
    with pytest.raises(Exception) as exc_info:
        charge.offense_date = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects. conviction_date may be None if charge still pending." \
        in str(exc_info.__dict__)

def test_is_felony():
    '''This tests the added property is_felony, which returns true if the conviction is a felony, and otherwise false'''
    charge1 = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert False == charge1.is_felony
    charge2 = Charge("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert True == charge2.is_felony

def test_is_misdemeanor():
    '''This tests the added property is_misdemeanor, which returns true if the conviction is a misdemeanor, and otherwise false'''
    charge1 = Charge("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 14-33")
    assert True == charge1.is_misdemeanor
    charge2 = Charge("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert False == charge2.is_misdemeanor

def test_is_infraction():
    '''This tests the added property is_infraction, which returns true if the conviction is an infraction, and otherwise false'''
    charge1 = Charge("Speeding", "Infraction", date(2009,1, 1), date(2010,1, 1), "Randolph", "NCGS 20-141")
    assert True == charge1.is_infraction
    charge2 = Charge("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")
    assert False == charge2.is_infraction

def conviction_date_none():
    '''I just added code to allow a None value for conviction dates and this is just a test for that functionality.'''
    charge1 = Charge("Speeding", "Infraction", date(2009,1, 1), None, "Randolph", "NCGS 20-141")
    assert None == charge1.conviction_date
    assert None == charge1._conviction_date
    charge1.conviction_date = date(2020,1,1)
    assert date(2020,1,1) == charge1.conviction_date
    assert date(2020,1,1) == charge1._conviction_date
    charge1.conviction_date = None
    assert None == charge1.conviction_date
    assert None == charge1._conviction_date
    with pytest.raises(Exception) as exc_info:
        charge.conviction_date = "bad data"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The dates of conviction and offense must be a valid datetime date objects. conviction_date may be None if charge still pending." \
        in str(exc_info.__dict__)
    charge1.set_conviction_date(date(2020,1,1))
    assert date(2020,1,1) == charge1.conviction_date
    assert date(2020,1,1) == charge1._conviction_date
    charge1.set_convictiondate_date(None)
    assert None == charge1.conviction_date
    assert None == charge1._conviction_date
