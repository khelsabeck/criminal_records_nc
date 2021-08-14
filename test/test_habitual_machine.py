from src.habitual_machine import State, StartState, StrikeOne, StrikeTwo, StrikeThree, FinishedState, HabitualMachine
from src.dumbwaiter import Dumbwaiter
from src.conviction import Conviction
from src.defendant import Defendant
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def hab_eligibles():
    '''This is a test list of the values of all crime classes eligible for habitual felony status'''
    hab_eligibles = [   "Class I Felony", "Class H Felony", "Class G Felony", "Class F Felony", "Class E Felony", "Class D Felony", "Class C Felony", 
                        "Class B1 Felony", "Class B2 Felony", "Class A Felony" ]
    return hab_eligibles

@pytest.fixture
def defendant1():
    '''This is a test defendant.'''
    defendant1 = Defendant("John", "Doe", date(1999, 1, 1))
    return defendant1    

@pytest.fixture
def dumbwaiter():
    '''This is a test dumbwaiter.'''
    dumbwaiter = Dumbwaiter(date(1999, 1, 1))
    return dumbwaiter    

@pytest.fixture
def conviction1():
    '''This is a basic conviction for testing the i_eligible method in the fsm itself.'''
    conviction1 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-72")
    return conviction1

@pytest.fixture
def one_strike():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a single strike for habitual status. It is not eligible for habitual status'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-72")                         # -- StrikeOne
    one_strike = [ con1, con2 ]
    return one_strike

@pytest.fixture
def two_strikes():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with 2 strikes. It is not eligible for habitual status'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2018,1, 1),date(2019,5, 5), "Randolph County", "14-39")    # -- StrikeTwo
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1), date(2015,6, 6), "Randolph County", "14-72")                    # 1 pt
    two_strikes = [ con1, con2, con3, con4, con5, con6 ]
    return two_strikes

@pytest.fixture
def one_strike_because18():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with 1 strike because the second happened with the defendant under 18. It is not eligible for habitual status'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2014,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2014,1, 1),date(2016,5, 5), "Randolph County", "14-39")    # -- Still under 18
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2016,1, 1),date(2016,6, 6), "Randolph County", "14-72")                    # 1 pt
    one_strike_because18 = [ con1, con2, con3, con4, con5, con6 ]
    return one_strike_because18    


@pytest.fixture
def screen_pedantic_exceptions():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with 1 strike because the second happened with the defendant under 18. It is not eligible for habitual status'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("Habitual B&E", "Class E Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-7.31")              # -- No  Strike (pedantic)
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Habitual Misdemeanor Assault", "Class H Felony", date(2014,1, 1),date(2019,5, 5), "Randolph County", "14-33.2") # -- No Strike (pedantic)
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,6, 6), "Randolph County", "14-72")                    # 
    screen_pedantic_exceptions = [ con1, con2, con3, con4, con5, con6 ]
    return screen_pedantic_exceptions    

@pytest.fixture
def three_striker():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with 3 strikes. It is eligible for habitual status'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,2, 2), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2017,12, 31),date(2018,1, 1), "Randolph County", "14-39")    # -- Strike2
    con6 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2018,1, 2),date(2018,1, 3), "Randolph County", "14-39")    # -- Strike3
    three_striker = [ con1, con2, con3, con4, con5, con6 ]
    return three_striker   

@pytest.fixture
def one_strike_overlapper():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with three overlapping-timeline felonies. Only one should count.'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2018,1, 1), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2014,12, 31),date(2017,12, 31), "Randolph County", "14-39")    # -- Overlap Strike2
    con6 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2018,1, 1),date(2018,1, 3), "Randolph County", "14-39")    # -- Overlap Strike3
    one_strike_overlapper = [ con1, con2, con3, con4, con5, con6 ]
    return one_strike_overlapper   

@pytest.fixture
def two_strike_overlapper():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with two non-overlapping-timeline felonies. Two should count out of three.'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2016,1, 1), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2016,1, 1),date(2017,12, 31), "Randolph County", "14-39")    # -- Overlap Strike2
    con6 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2018,1, 1),date(2018,1, 3), "Randolph County", "14-39")    # -- Overlap Strike3
    two_strike_overlapper = [ con1, con2, con3, con4, con5, con6 ]
    return two_strike_overlapper   

@pytest.fixture
def two_strike_overlapper2():
    '''FOR USE WITH defendant1, born 1/1/99.
    This represents a record with two non-overlapping-timeline felonies. Two should count out of three.'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                    # 
    con2 = Conviction("PSG", "Class H Felony", date(2014,1, 1),date(2015,1, 1), "Randolph County", "14-72")                         # -- StrikeOne
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,3, 3), "Randolph County", "14-72")                    # 
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2014,1, 1),date(2015,4, 4), "Randolph County", "14-72")                    # 
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2016,1, 1),date(2017,12, 31), "Randolph County", "14-39")    # -- Strike2
    con6 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2017,12, 31),date(2018,1, 3), "Randolph County", "14-39")    # -- Overlaps Strike2
    con7 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2017,12, 31),date(2018,1, 3), "Randolph County", "14-39")    # -- Overlaps Strike2

    two_strike_overlapper2 = [ con1, con2, con3, con4, con5, con6, con7 ]
    return two_strike_overlapper2   


def test_state():
    '''This is a basic initialization test of the base state.'''
    st = State()
    assert State == type(st)
    assert "State" == str(st)
    assert "State" == repr(st)

def test_startstate(dumbwaiter):
    '''This is a test of the start state with a mock dumbwaiter and an empty list of convictions. It should go straight to the FinishedState.'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event([],dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == dumbwaiter.ran 

def test_pedantics(screen_pedantic_exceptions):
    '''This tests the screening out of two pedantic exceptions which would otherwise count. These only count if they were committed before 12/1/2004'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event([],dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [] == expect_finished.convictions

def test_one_strike(one_strike):
    '''This is a test of a one-strike record.'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event(one_strike, dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [ one_strike[1] ] == expect_finished.dumbwaiter.habitual_convictions
    assert False == expect_finished.dumbwaiter.hab_eligible
    assert None == expect_finished.dumbwaiter.date_eligible

def test_2strikes(two_strikes):
    '''This is a test of the expected returns from a 2-strike record'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event(two_strikes, dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [ two_strikes[1], two_strikes[4] ] == expect_finished.dumbwaiter.habitual_convictions
    assert False == expect_finished.dumbwaiter.hab_eligible
    assert None == expect_finished.dumbwaiter.date_eligible

def test_1strike_bc18(one_strike_because18):
    '''This is a test of the expected returns from a 1-strike record because what would have qualified as the second strike was pre-18.'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event(one_strike_because18, dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [ one_strike_because18[1] ] == expect_finished.dumbwaiter.habitual_convictions
    assert False == expect_finished.dumbwaiter.hab_eligible
    assert None == expect_finished.dumbwaiter.date_eligible    

def test_pedantic_exceptions(screen_pedantic_exceptions):
    '''This tests these two particular and pedantic exceptions. These appear to be qualified felonies, but should be screened out'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event(screen_pedantic_exceptions, dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [  ] == expect_finished.dumbwaiter.habitual_convictions
    assert False == expect_finished.dumbwaiter.hab_eligible
    assert None == expect_finished.dumbwaiter.date_eligible    

def test_3strikes(three_striker):
    '''This is a test with a record for someone who has three strikes, two after turning 18'''
    st = StartState()
    dumbwaiter = Dumbwaiter(date(1999,1,1)) 
    expect_finished = st.on_event(three_striker, dumbwaiter)
    assert FinishedState == type(expect_finished)
    assert True == expect_finished.dumbwaiter.ran 
    assert [ three_striker[1],three_striker[4],three_striker[5] ] == expect_finished.dumbwaiter.habitual_convictions
    assert True == expect_finished.dumbwaiter.hab_eligible
    assert date(2018,1, 3) == expect_finished.dumbwaiter.date_eligible    

def test_machine_init():
    '''This is a test of the initialization and type of the habitualmachine itself.'''
    machine = HabitualMachine()
    assert HabitualMachine == type(machine)
    assert StartState == type(machine.state)

def test_machine_strike1(one_strike):
    '''This is an integration test of the habitual machine with a 1-strike record.'''
    machine = HabitualMachine()
    machine.on_event(one_strike, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible
    assert True == machine.dumbwaiter.ran
    assert 1 == len(machine.dumbwaiter.habitual_convictions)

def test_machine_strike2_butfor18(one_strike_because18):
    '''This is an integration test of the habitual machine with a 1-strike record that would be 2 but for he second being pre-18.'''
    machine = HabitualMachine()
    machine.on_event(one_strike_because18, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 1 == len(machine.dumbwaiter.habitual_convictions)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible

def test_machine_strike2(two_strikes):
    '''This is an integration test of the habitual machine with a 2-strike record.'''
    machine = HabitualMachine()
    machine.on_event(two_strikes, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible
    assert 2 == len(machine.dumbwaiter.habitual_convictions)
    assert True == machine.dumbwaiter.ran

def test_machine_strike3(three_striker):
    '''This is an integration test of the habitual machine with a 3-strike record.'''
    machine = HabitualMachine()
    machine.on_event(three_striker, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 3 == len(machine.dumbwaiter.habitual_convictions)
    assert True == machine.hab_eligible
    assert date(2018,1,3) == machine.date_eligible

def test_overlap(one_strike_overlapper):
    '''This is an integration test of the habitual machine with a 1-strike record with overlapping dates of offense/conviction from 3 felonies.'''
    machine = HabitualMachine()
    machine.on_event(one_strike_overlapper, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 1 == len(machine.dumbwaiter.habitual_convictions)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible

def test_overlap_2striker(two_strike_overlapper):
    '''This is an integration test of the habitual machine with a 2-strike record with overlapping dates of offense/conviction from 3 felonies. Excpect 2
    strikes out of the three felonies'''
    machine = HabitualMachine()
    machine.on_event(two_strike_overlapper, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 2 == len(machine.dumbwaiter.habitual_convictions)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible

def test_overlap_2striker(two_strike_overlapper2):
    '''This is an integration test of the habitual machine with a 2-strike record with overlapping dates of offense/conviction from 3 felonies. Excpect 2
    strikes out of the three felonies'''
    machine = HabitualMachine()
    machine.on_event(two_strike_overlapper2, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 2 == len(machine.dumbwaiter.habitual_convictions)
    assert False == machine.hab_eligible
    assert None == machine.date_eligible


def test_machine_offense_date_is_eligible(three_striker, conviction1):
    '''This tests the habitual machine is_eligible method.'''
    machine = HabitualMachine()
    machine.on_event(three_striker, date(1999,1,1))
    assert FinishedState == type(machine.state)
    assert True == machine.dumbwaiter.ran
    assert 3 == len(machine.dumbwaiter.habitual_convictions)
    assert True == machine.hab_eligible
    assert date(2018,1,3) == machine.date_eligible
    assert False == machine.offense_date_is_eligible(conviction1.offense_date)

def test_machine_offense_date_is_eligible_error(three_striker, conviction1):
    '''This tests the habitual machine is_eligible method's error-handling.'''
    machine = HabitualMachine()
    with pytest.raises(Exception) as exc_info:
        machine.offense_date_is_eligible(conviction1.offense_date)
    exception_raised = exc_info.value
    assert type(ValueError()) == type(exception_raised)
    assert "The record has not been successfully caluclated yet." in str(exc_info.__dict__)
