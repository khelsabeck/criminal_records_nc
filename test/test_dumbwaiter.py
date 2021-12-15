from src.dumbwaiter import Dumbwaiter
from src.charge import Charge
from src.defendant import Defendant
import pytest
from datetime import date, datetime, timedelta
import typing

def test_dw_initialization():
    '''This is a basic test of the Dumbwaiter initializing and establishing its state.'''
    dw = Dumbwaiter(date(1999, 1, 1))
    assert Dumbwaiter == type(dw)
    assert date(1999, 1, 1) == dw.birthdate
    assert date(1999, 1, 1) == dw._birthdate
    assert 0 == len(dw.habitual_convictions) 
    assert list == type(dw.habitual_convictions)
    assert False == dw.hab_eligible
    assert False == dw._hab_eligible
    assert None == dw.date_eligible
    assert None == dw._date_eligible
    assert None == dw._date_eligible
    assert date(2017, 1, 1) == dw.eighteenth_birthdate
    assert False == dw.over18_on_date(date(2016, 12, 31))
    assert True == dw.over18_on_date(date(2017, 1, 1))
    assert False == dw.ran

def test_set_birthdate():
    '''This should test that the birthdate can be reset and should test the error-handling for a bad attempt'''
    dw = Dumbwaiter(date(1999, 1, 1))
    dw.birthdate = date(1999, 1, 2)
    assert date(1999, 1, 2) == dw.birthdate
    assert date(1999, 1, 2) == dw._birthdate
    with pytest.raises(Exception) as exc_info:
        dw.birthdate = "bad data input"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The defendant's birthdate is a prerequisite for habitual felon analysis, and it must be a valid datetime 'date' object." in str(exc_info.__dict__)

def test_set_hab_eligible():
    '''This should test that the hab_eligible value can be reset and should test the error-handling for a bad attempt'''
    dw = Dumbwaiter(date(1999, 1, 1))
    assert False == dw.hab_eligible
    dw.hab_eligible = True
    assert True == dw.hab_eligible
    with pytest.raises(Exception) as exc_info:
        dw.hab_eligible = "bad data input"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The hab_eligible value must be a boolean." in str(exc_info.__dict__)

def test_over18_ondate_error():
    '''This tests the error handling for when a non-datetime date object is given as a parameter in the test_over18 method.'''
    dw = Dumbwaiter(date(1999, 1, 1))
    with pytest.raises(Exception) as exc_info:
        dw.over18_on_date("bad input")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The method over18_on_date() in Dumbwaiter requires a datetime date as a parameter." in str(exc_info.__dict__)

def test_set_date_eligible():
    '''This tests the resetting of the date at which a defendant is eligible for habitual felon status'''
    dw = Dumbwaiter(date(1999, 1, 1))
    assert False == dw.hab_eligible
    dw.hab_eligible = True
    assert True == dw.hab_eligible
    dw.date_eligible = date(2021, 1, 1)
    with pytest.raises(Exception) as exc_info:
        dw.date_eligible = "bad data input"
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The method set_date_eligible() in Dumbwaiter requires a datetime date as a parameter." in str(exc_info.__dict__)

def test_offense_date_is_eligible():
    '''This tests the method offense_date_is_eligible, confirming that the offense_date given is eligible when eligible, and not when not.'''
    dw = Dumbwaiter(date(1999, 1, 1))
    assert False == dw.hab_eligible
    dw.hab_eligible = True
    assert True == dw.hab_eligible
    dw.date_eligible = date(2021, 1, 1)
    assert True == dw.offense_date_is_eligible(date(2021, 1, 2))
    assert False == dw.offense_date_is_eligible(date(2020, 12, 31))