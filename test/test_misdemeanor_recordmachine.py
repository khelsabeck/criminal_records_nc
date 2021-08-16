from src.misdemeanor_recordmachine import State, StartState, ScreeningState, ZippingState, FinishedState, MisdemeanorRecordMachine
from src.conviction import Conviction
from src.defendant import Defendant
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def level1_record():
    '''This represents a level 1 misdemeanor record with no convictions for anything.'''
    level1_record = [  ]
    return level1_record   


@pytest.fixture
def level1_justinfractions():
    '''This represents a level 1 record with only infractions as convictions.'''
    con1 = Conviction("Speeding", "Infraction", date(2011,1, 1),date(2012,1, 1), "Randolph County", "20-141")   
    level1_justinfractions = [ con1 ]
    return level1_justinfractions   

@pytest.fixture
def level2_onepoint():
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("Speeding", "Infraction", date(2011,1, 1),date(2012,1, 1), "Randolph County", "20-141")   
    level2_onepoint = [ con1, con2 ]
    return level2_onepoint

@pytest.fixture
def level2_onepoint_samedate():
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("Larceny", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")   
    level2_onepoint_samedate = [ con1, con2 ]
    return level2_onepoint_samedate

@pytest.fixture
def level2_fourpoint():
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # +1
    con2 = Conviction("Speeding", "Infraction", date(2011,1, 1),date(2012,1, 1), "Randolph County", "20-141")   
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2016,1, 1),date(2017,1, 1), "Randolph County", "14-72")                    # +1
    con4 = Conviction("Larceny", "Class H Felony", date(2016,1, 1),date(2017,1, 2), "Randolph County", "14-72")                     # +1
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2016,1, 1),date(2016,1, 3), "Randolph County", "14-39")    # +1
    level2_fourpoint = [ con1, con2, con3, con4, con5 ]
    return level2_fourpoint

@pytest.fixture
def level3_fivepoint():
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # +1
    con2 = Conviction("Speeding", "Infraction", date(2011,1, 1),date(2012,1, 1), "Randolph County", "20-141")   
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2016,1, 1),date(2017,1, 1), "Randolph County", "14-72")                    # +1
    con4 = Conviction("Larceny", "Class H Felony", date(2016,1, 1),date(2017,1, 2), "Randolph County", "14-72")                     # +1
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2016,1, 1),date(2016,1, 3), "Randolph County", "14-39")    # +1
    con6 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2016,1, 2),date(2016,1, 4), "Randolph County", "14-39")    # +1
    level2_fourpoint = [ con1, con2, con3, con4, con5, con6 ]
    return level2_fourpoint

def test_state():
    '''This is a test of just the initialization test of the base state and its data.'''
    st = State()
    assert State == type(st)
    assert "State" == str(st)
    assert "State" == repr(st)
    assert 0 == st.points
    assert 1 == st.level

def test_startstate_init():
    '''This tests the initialization of screening state and its data.'''
    start = StartState()
    assert StartState == type(start)
    assert "StartState" == str(start)
    assert "StartState" == repr(start)
    assert 0 == start.points
    assert 1 == start.level

def test_start_transitions():
    '''This is a test of the startstate's transition to finished.'''
    start = StartState()
    assert 0 == start.points
    assert 1 == start.level
    expect_finished = start.on_event([],0)
    assert FinishedState == type(expect_finished)
    assert 0 == expect_finished.points
    assert 1 == expect_finished.level

def test_start_error():
    '''This is just a test of the startstate error handling in which there is bad data.'''
    start = StartState()
    with pytest.raises(Exception) as exc_info:
        start.on_event("bad data", "bad data")
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "There was an exception in the StartState. The parameter values are likely invalid." in str(exc_info.__dict__)

def test_screeningstate_init():
    '''This tests the initialization of screening state and its data.'''
    screen = ScreeningState()
    assert ScreeningState == type(screen)
    assert "ScreeningState" == str(screen)
    assert "ScreeningState" == repr(screen)
    assert 0 == screen.points
    assert 1 == screen.level

def test_screening_transitions():
    '''This is a test of the screeningstate's transition to finished.'''
    screen = ScreeningState()
    assert 0 == screen.points
    assert 1 == screen.level
    expect_finished = screen.on_event([],0)
    assert FinishedState == type(expect_finished)
    assert 0 == expect_finished.points
    assert 1 == expect_finished.level

def test_recordmachine_initvalues():
    '''This tests the basic initialization and data of overall machine.'''
    machine = MisdemeanorRecordMachine()
    assert StartState == type(machine.state)
    with pytest.raises(Exception) as exc_info:
        points = machine.points
    exception_raised = exc_info.value
    assert type(Exception()) == type(exception_raised)
    assert "The points cannot be determined until the on_event() method has run with the record." in str(exc_info.__dict__)
    with pytest.raises(Exception) as exc_info:
        points = machine.level
    exception_raised = exc_info.value
    assert type(Exception()) == type(exception_raised)
    assert "The level cannot be determined until the on_event() method has run with the record." in str(exc_info.__dict__)

def test_level1record(level1_record):
    '''This is an integration test with a level 1 record without points.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level1_record)
    assert 0 == machine.points 
    assert 1 == machine.level
    assert FinishedState == type(machine.state)

def test_level1_justinfractions(level1_justinfractions):
    '''This is an integration test with a level 1 record with no convictions except for infractions.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level1_justinfractions)
    assert 0 == machine.points 
    assert 1 == machine.level
    assert FinishedState == type(machine.state)

def test_level2_onepoint(level2_onepoint):
    '''This is a test of a level 2 record with one point.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level2_onepoint)
    assert 1 == machine.points 
    assert 2 == machine.level
    assert FinishedState == type(machine.state)

def test_level2_onepoint_samedate(level2_onepoint_samedate):
    '''This is an integration test with a level two record having one point with 2 convictions on the same date.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level2_onepoint_samedate)
    assert 1 == machine.points 
    assert 2 == machine.level
    assert FinishedState == type(machine.state)

def test_level2_fourpoint(level2_fourpoint):
    '''This is an integration test with a level two record having 4 points.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level2_fourpoint)
    assert 4 == machine.points 
    assert 2 == machine.level
    assert FinishedState == type(machine.state)

def test_level3_fivepoint(level3_fivepoint):
    '''This is an integration test having a level 3 record with five points.'''
    machine = MisdemeanorRecordMachine()
    machine.on_event(level3_fivepoint)
    assert 5 == machine.points 
    assert 3 == machine.level
    assert FinishedState == type(machine.state)
