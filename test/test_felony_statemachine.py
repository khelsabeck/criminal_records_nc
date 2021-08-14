from src.felony_record_statemachine import EligibleCrimes, State, StartState, ScreeningState, RescreeningState, ZippingState, ZippedState, HubState, \
    MisdemeanorState, FelonyStartState, FelonyOverHState, FelonyOverEState, FelonyOverB2State, FinishedState, ErrorState, Felony_RecordMachine
from src.conviction import Conviction
from src.defendant import Defendant
import pytest
from datetime import date, datetime, timedelta
import typing

@pytest.fixture
def eligibles():
    '''This is a test list of the values of all crimes eligible for felony points'''
    eligibles = [  "Class 1 Misdemeanor", "Class A1 Misdemeanor", "Class I Felony", "Class H Felony", "Class G Felony", "Class F Felony", "Class E Felony", 
                    "Class D Felony", "Class C Felony", "Class B1 Felony", "Class B2 Felony", "Class A Felony" ]
    return eligibles

@pytest.fixture
def level1_convictions_onepoint():
    '''This represents a low-level criminal with 1 point for felonies (expected value is Level 1).'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")
    level1_convictions_onepoint = [ con1 ]
    return level1_convictions_onepoint

@pytest.fixture
def level1_convictions_nopoints():
    '''This represents a low-level criminal with 0 points for felonies (expected value is Level 1).'''
    con1 = Conviction("Shoplifting", "Class 3 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")
    level1_convictions_nopoints = [ con1 ]
    return level1_convictions_nopoints

@pytest.fixture
def level2_convictions_2points():
    '''This represents a Level 2 record with 2 single class 1 misdemeanors for 2 points'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")
    con2 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")
    level2_convictions_2points = [ con1, con2 ]
    return level2_convictions_2points

@pytest.fixture
def level2_convictions_fivepoints():
    '''This represents a level 2 record with exactly 5 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("Assault on Female", "Class A1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-33")
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")
    con3 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")
    level2_convictions_fivepoints = [ con1, con2, con3 ]
    return level2_convictions_fivepoints

@pytest.fixture
def level3_convictions_sixpoints():
    '''This represents a level 3 record with exactly 6 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")
    con3 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")
    level3_convictions_sixpoints = [ con1, con2, con3, con4 ]
    return level3_convictions_sixpoints

@pytest.fixture
def level3_convictions_ninepoints():
    '''This represents a level 3 record with exactly 9 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")                         # 2 pts
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")                    # 1 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("Telecom Hacking", "Class G Felony", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-113.5")          # 4 pts
    level3_convictions_ninepoints = [ con1, con2, con3, con4, con5 ]
    return level3_convictions_ninepoints

@pytest.fixture
def level4_convictions_tenpoints():
    '''This represents a level 4 record with exactly 10 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")                         # 2 pts
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")                    # 1 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-39")    # 4 pts
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,6, 6), "Randolph County", "14-72")                    # 1 pt
    level4_convictions_tenpoints = [ con1, con2, con3, con4, con5, con6 ]
    return level4_convictions_tenpoints

@pytest.fixture
def level4_convictions_13points():
    '''This represents a level 4 record with exactly 13 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")                         # 2 pts
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")                    # 1 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-39")    # 4 pts
    con6 = Conviction("Involuntary Manslaughter", "Class F Felony", date(2009,1, 1), date(2015,6, 6), "Randolph County", "14-18")    # 4 pts
    level4_convictions_13points = [ con1, con2, con3, con4, con5, con6 ]
    return level4_convictions_13points

@pytest.fixture
def level5_convictions_14points():
    '''This represents a level 5 record with exactly 14 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("PSG", "Class H Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-72")                         # 2 pts
    con3 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3,3), "Randolph County", "14-72")                    # 1 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("Second Degree Kidnapping", "Class E Felony", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-39")    # 4 pts
    con6 = Conviction("Involuntary Manslaughter", "Class F Felony", date(2009,1, 1), date(2015,6, 6), "Randolph County", "14-18")    # 4 pts
    con7 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,7, 7), "Randolph County", "14-72")                    # 1 pt
    level5_convictions_14points = [ con1, con2, con3, con4, con5, con6, con7 ]
    return level5_convictions_14points

@pytest.fixture
def level5_convictions_17points():
    '''This represents a level 5 record with exactly 17 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("Robbery with Dang Weap", "Class D Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-87")      # 6 pt
    con3 = Conviction("Murder in the 2nd", "Class B1 Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-17(b)")       # 9 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    level5_convictions_17points = [ con1, con2, con3, con4 ]
    return level5_convictions_17points

@pytest.fixture
def level5_convictions_17_wb2andC():
    '''This represents a level 5 record with exactly 17 points including a b2 and a c felony'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")  # 6 pt
    con3 = Conviction("Murder in the 2nd", "Class B2 Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-17(c)")       # 6 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-72")                    # 1 pt
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,6, 6), "Randolph County", "14-72")                    # 1 pt
    con7 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,7, 7), "Randolph County", "14-72")                    # 1 pt
    level5_convictions_17_wb2andC = [ con1, con2, con3, con4, con5, con6, con7 ]
    return level5_convictions_17_wb2andC

@pytest.fixture
def level5_convictions_17_redundant_dates():
    '''This represents a level 5 record w  17 points. There are redundant convictions based on the dates/levels.'''
    con1 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")                    # 1 pt
    con2 = Conviction("Assault w Deadly WIKISI", "Class C Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-32(a)")  # 6 pt
    con3 = Conviction("Murder in the 2nd", "Class B2 Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-17(c)")       # 6 pt
    con4 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 1 pt
    con5 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "14-72")                    # 0 pt (same as other date)
    con6 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-72")                    # 0 pt (same as other date)
    con7 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,5, 5), "Randolph County", "14-72")                    # 1 pt
    con8 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,6, 6), "Randolph County", "14-72")                    # 1 pt
    con9 = Conviction("PSG", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,7, 7), "Randolph County", "14-72")                    # 1 pt
    level5_convictions_17_redundant_dates = [ con1, con2, con3, con4, con5, con6, con7, con8, con9 ]
    return level5_convictions_17_redundant_dates

@pytest.fixture
def level6_convictions_18points():
    '''This represents a level 6 record with exactly 18 points from a mix of felonies and misdemeanors'''
    con1 = Conviction("Possess Meth", "Class I Felony", date(2009,1, 1), date(2015,1, 1), "Randolph County", "90-95(d)(2)")          # 2 pts
    con2 = Conviction("Robbery with Dang Weap", "Class D Felony", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-87")      # 6 pt
    con3 = Conviction("Murder First Deg", "Class A Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-17(a)")         # 10 pt
    level6_convictions_18points = [ con1, con2, con3 ]
    return level6_convictions_18points

@pytest.fixture
def screening():
    '''This represents a level 1 record with ineligible misdemeanors (level 3, 2, and infraction don't count'''
    con1 = Conviction("Shoplifting", "Class 3 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "14-72")            # 0 pts
    con2 = Conviction("Simple Assault", "Class 2 Misdemeanor", date(2009,1, 1), date(2015,2, 2), "Randolph County", "14-33")         # 0 pt
    screening = [ con1, con2 ]
    return screening

@pytest.fixture
def rescreening():
    '''This represents specific class 1 misdemeanors that do not count from chapter 20 of the statutes. Only these 3 count:
    20-141.4(a2), 20-138.1, and 20-138.2.'''
    con1 = Conviction("misdemeanor death by vehicle", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,1, 1), "Randolph County", "20-141.4(a2)")        # 1 pts
    con2 = Conviction("Iimpaired driving", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,2, 2), "Randolph County", "20-138.1")                       # 1 pt
    con3 = Conviction("Commercial impaired driving", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,3, 3), "Randolph County", "20-138.2")             # 1 pt
    con4 = Conviction("DWLR/I", "Class 1 Misdemeanor", date(2009,1, 1), date(2015,4, 4), "Randolph County", "20-28(a1")                                  # 0 pts
    rescreening = [ con1, con2, con3, con4 ]
    return rescreening

@pytest.fixture
def one_time_murderer():
    '''This represents a one-time murderer.'''
    con1 = Conviction("Murder First Deg", "Class A Felony", date(2009,1, 1), date(2015,3, 3), "Randolph County", "14-17(a)")         # 10 pt
    one_time_murderer = [ con1 ]
    return one_time_murderer


def test_crimes(eligibles:list):
    '''This tests the values and order of values in the EligibleCrimes.crimes list'''
    frs_crimes = EligibleCrimes()
    assert eligibles == frs_crimes.crimes 

def test_state():
    '''This tests the base state.'''
    state = State()
    assert 0 == state.points 
    assert 1 == state.level
    assert "State" == repr(state) 
    assert "State" == str(state) 
    assert None == state.on_event(0, 0)
    
def test_startstate_onept(level1_convictions_onepoint:list):
    '''This tests the StartState's basic initialization. It also tests the transitions with a one point record.'''
    start = StartState()
    assert "StartState" == str(start)
    assert "StartState" == repr(start)
    finished = start.on_event([], 0)
    assert "FinishedState" == repr(finished)
    assert "FinishedState" == str(finished)
    start = StartState()
    level1 = start.on_event(level1_convictions_onepoint, 0)
    assert "FinishedState" == repr(level1)
    assert "FinishedState" == str(level1)
    assert 1 == level1.points
    assert 1 == level1.level    

def test_startstate_0pt(level1_convictions_nopoints:list):
    '''This tests the StartState's transitions with a 0 point record.'''
    start = StartState()
    level1 = start.on_event(level1_convictions_nopoints, 0)
    assert "FinishedState" == repr(level1)
    assert "FinishedState" == str(level1)
    assert 0 == level1.points
    assert 1 == level1.level        

def test_startstate_2pt(level2_convictions_2points:list):
    '''This tests the StartState's transitions with a 2 point record.'''
    start = StartState()
    level2 = start.on_event(level2_convictions_2points, 0)
    assert "FinishedState" == repr(level2)
    assert "FinishedState" == str(level2)
    assert 2 == level2.points
    assert 2 == level2.level            

def test_startstate_5pt(level2_convictions_fivepoints:list):
    '''This tests the StartState's transitions with a 5 point record.'''
    start = StartState()
    level2 = start.on_event(level2_convictions_fivepoints, 0)
    assert "FinishedState" == repr(level2)
    assert "FinishedState" == str(level2)
    assert 5 == level2.points
    assert 2 == level2.level                

def test_startstate_6pt(level3_convictions_sixpoints:list):
    '''This tests the StartState's transitions with a 6 point record (level 3 low bound).'''
    start = StartState()
    level3 = start.on_event(level3_convictions_sixpoints, 0)
    assert "FinishedState" == repr(level3)
    assert "FinishedState" == str(level3)
    assert 6 == level3.points
    assert 3 == level3.level  

def test_startstate_9pt(level3_convictions_ninepoints:list):
    '''This tests the StartState's transitions with a 9-point record (level 3 high bound).'''
    start = StartState()
    level3 = start.on_event(level3_convictions_ninepoints, 0)
    assert "FinishedState" == repr(level3)
    assert "FinishedState" == str(level3)
    assert 9 == level3.points
    assert 3 == level3.level                    

def test_startstate_10pt(level4_convictions_tenpoints:list):
    '''This tests the StartState's transitions with a 10-point record (level 4 low bound).'''
    start = StartState()
    level4 = start.on_event(level4_convictions_tenpoints, 0)
    assert "FinishedState" == repr(level4)
    assert "FinishedState" == str(level4)
    assert 10 == level4.points
    assert 4 == level4.level                    

def test_startstate_13pt(level4_convictions_13points:list):
    '''This tests the StartState's transitions with a 13-point record (level 4 high bound).'''
    start = StartState()
    level4 = start.on_event(level4_convictions_13points, 0)
    assert "FinishedState" == repr(level4)
    assert "FinishedState" == str(level4)
    assert 13 == level4.points
    assert 4 == level4.level                    

def test_startstate_14pt(level5_convictions_14points:list):
    '''This tests the StartState's transitions with a 14-point point record (level 5 low bound).'''
    start = StartState()
    level5 = start.on_event(level5_convictions_14points, 0)
    assert "FinishedState" == repr(level5)
    assert "FinishedState" == str(level5)
    assert 14 == level5.points
    assert 5 == level5.level                    

def test_startstate_17pt_1(level5_convictions_17points:list):
    '''This tests the StartState's transitions with a 17-point record (level 5 high bound).'''
    start = StartState()
    level5 = start.on_event(level5_convictions_17points, 0)
    assert "FinishedState" == repr(level5)
    assert "FinishedState" == str(level5)
    assert 17 == level5.points
    assert 5 == level5.level                    

def test_startstate_17pt_2(level5_convictions_17_wb2andC:list):
    '''This tests the StartState's transitions with a 17-point record, inclusive of a B2 and C felony.'''
    start = StartState()
    level5 = start.on_event(level5_convictions_17_wb2andC, 0)
    assert "FinishedState" == repr(level5)
    assert "FinishedState" == str(level5)
    assert 17 == level5.points
    assert 5 == level5.level 

def test_zipping_state_uniques(level5_convictions_17_wb2andC:list, level5_convictions_17_redundant_dates:list):
    '''This test should examine the ZippingState's helper method for making a list of unique dates. '''    
    state = ZippingState()
    expected = [date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4), date(2015,5, 5), date(2015,6, 6), date(2015,7, 7)] #all unique
    assert expected == state.make_list_of_unique_dates(level5_convictions_17_wb2andC)
    state = ZippingState()
    expected2 = [ date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4), date(2015,5, 5), date(2015,6, 6), date(2015,7, 7)]
    assert expected2 == state.make_list_of_unique_dates(level5_convictions_17_redundant_dates)  #this contains redundancies. If it works, they're screened out

def test_zipping_state_emptylists(level5_convictions_17_wb2andC:list, level5_convictions_17_redundant_dates:list):
    '''This unit tests the functionality of the helper for creating a list of empties'''
    state = ZippingState()
    uniques = [date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4), date(2015,5, 5), date(2015,6, 6), date(2015,7, 7)] #all unique
    expected = [ [], [], [], [], [], [], [] ]
    assert expected == state.make_list_of_empties(uniques)
    state = ZippingState()
    uniques2 = [ date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4)]
    expected2 = [ [], [], [], [] ]
    assert expected2 == state.make_list_of_empties(uniques2)  #this contains redundancies. If it works, they're screened out

def test_zipping_state_fillempties(level5_convictions_17_wb2andC:list, level5_convictions_17_redundant_dates:list):
    '''This unit tests the functionality of the helper for creating a list of empties'''
    state = ZippingState()
    uniques = [date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4), date(2015,5, 5), date(2015,6, 6), date(2015,7, 7)] #all unique
    empties = [ [], [], [], [], [], [], [] ]
    expected = [    [level5_convictions_17_wb2andC[0]], 
                    [level5_convictions_17_wb2andC[1]], 
                    [level5_convictions_17_wb2andC[2]], 
                    [level5_convictions_17_wb2andC[3]], 
                    [level5_convictions_17_wb2andC[4]], 
                    [level5_convictions_17_wb2andC[5]], 
                    [level5_convictions_17_wb2andC[6]] 
                ]
    assert expected == state.fill_empties(level5_convictions_17_wb2andC, uniques, empties )
    state = ZippingState()
    uniques2 = [ date(2015,1, 1), date(2015,2, 2), date(2015,3, 3), date(2015,4, 4), date(2015,5, 5), date(2015,6, 6), date(2015,7, 7)]
    empties2 = [ [], [], [], [], [], [], [] ]
    expected2 = [   [ level5_convictions_17_redundant_dates[0] ], 
                    [ level5_convictions_17_redundant_dates[1] ], 
                    [ level5_convictions_17_redundant_dates[2], level5_convictions_17_redundant_dates[5] ], 
                    [ level5_convictions_17_redundant_dates[3], level5_convictions_17_redundant_dates[4] ],
                    [ level5_convictions_17_redundant_dates[6] ],
                    [ level5_convictions_17_redundant_dates[7] ],
                    [ level5_convictions_17_redundant_dates[8] ],
                ]
    assert expected2 == state.fill_empties(level5_convictions_17_redundant_dates, uniques2, empties2)  

def test_startstate_17pt_3(level5_convictions_17_redundant_dates:list):
    '''This tests the StartState's transitions with a 17-point record with redundant convictions given dates (only counts if they were on different dates).'''
    start = StartState()
    level5 = start.on_event(level5_convictions_17_redundant_dates, 0)
    assert "FinishedState" == repr(level5)
    assert "FinishedState" == str(level5)
    assert 17 == level5.points
    assert 5 == level5.level                       

def test_startstate_error():
    '''This test confirms the appropriate error-handling in the startstate'''
    start = StartState()
    expected = "There was an exception in the StartState. The parameter values are likely invalid."
    error = start.on_event("bad input", 0)
    assert "ErrorState" == repr(error)
    assert "ErrorState" == str(error)
    assert "An error occured while caluclating the record." == error.points
    assert expected == error.error

def test_screening(screening:list):
    '''This takes a list of convictions that should not count because while they are vali as crimes, they are ineligible for felony sentencing points in
    calculating a felony record.'''
    start = StartState()
    level1 = start.on_event(screening, 0)
    assert "FinishedState" == repr(level1)
    assert "FinishedState" == str(level1)
    assert 0 == level1.points
    assert 1 == level1.level

def test_rescreening(rescreening:list):
    '''This takes a list of convictions that should count or not count and confirms that the ones that should count will count and the one that does not
    will not.'''
    start = StartState()
    level2 = start.on_event(rescreening, 0)
    assert "FinishedState" == repr(level2)
    assert "FinishedState" == str(level2)
    assert 3 == level2.points
    assert 2 == level2.level    
    start2 = StartState()
    level1 = start2.on_event([], 0)
    assert "FinishedState" == repr(level1)
    assert "FinishedState" == str(level1)
    assert 0 == level1.points
    assert 1 == level1.level    

def test_felonyoverb2state(one_time_murderer:list):
    '''This is an attempt to get my coverage up by hitting the FelonyOverB2State with a class A felony stading in isolation'''
    highest_felony = FelonyOverB2State()
    level4 = highest_felony.on_event(one_time_murderer, 0)
    assert "FinishedState" == repr(level4)
    assert "FinishedState" == str(level4)
    assert 10 == level4.points
    assert 4 == level4.level    
    
def test_level6_convictions_18points(level6_convictions_18points:list):
    '''This is a test of a level 6 felon with exactly 18 points (low bound).'''
    start = StartState()
    level6 = start.on_event(level6_convictions_18points, 0)
    assert "FinishedState" == repr(level6)
    assert "FinishedState" == str(level6)
    assert 18 == level6.points
    assert 6 == level6.level    

def test_statemachine():
    '''This is an integration test of the statemachine itself.'''
    recordmachine = Felony_RecordMachine()
    assert Felony_RecordMachine == type(recordmachine)
    assert StartState == type(recordmachine.state)
    recordmachine.on_event([], 0)
    assert 0 == recordmachine.state.points
    assert 1 == recordmachine.state.level
    assert 0 == recordmachine.points
    assert 1 == recordmachine.level

def test_rescreening_transitiontofinished():
    '''In an effprt for 100% coverage, I am trying to test the rescreening state's transition to finishedstate where there is an empty list'''
    start = RescreeningState()
    finished = start.on_event([], 0)
    assert "FinishedState" == repr(finished)
    assert "FinishedState" == str(finished)
