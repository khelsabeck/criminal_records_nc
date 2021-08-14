'''
Author: Keith Hinkleman Helsabeck

The plan for this module is to determine whether a given set of convictions qualify a defendant as a habitual felon in North Carolina. I am adapting 
this from a prior program I wrote for internal use in a Django project (not currently online).

Habitual Felony in NC:
Habitual status is an OPTIONAL consideration in NC sentencing and can allow a prosecutor and judge to raise the sentence of a felony crime to a sentence 
corresponding with a felony offense four classes higher (up to C at maximum) than the actual crime. 

A defendant is eligible for habitual status if and only if:
(1) The Defendant has had three prior periods of non-overlapping offense dates and convictions for eligible felonies. IE: Jim commits Offense 1 on Date 1, then 
Offense1 is convicted on Date2, and THEN (after that conviction) he commits Offense2 on Date3, and Offense2 is convicted on Date4.
(2) No more than one of those can count if the Defendant was under 18.
'''
from datetime import date, timedelta
from src.dumbwaiter import Dumbwaiter

# #------- Base State:------------------
class State:
    '''This is the base state for the HabitualMachine FSM. It is the template from which they all inherit.'''
    def __init__(self):
        pass

    def on_event(self, convictions:list, dumbwaiter): 
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

# #------- These are the concrete states:------------------
class StartState(State):
    '''This is the starting state for a state machine made to determine if a Defendant is eligible as a habitual felon in NC. It runs scripts to get rid of any
    non-eligible. Some of the rules get picky (see https://www.sog.unc.edu/sites/www.sog.unc.edu/files/reports/aojb0804.pdf).'''
    def on_event(self, convictions:list, dumbwaiter): 
        screened = [ con for con in convictions if con.is_felony ]                                                          # eliminate all cons but felonies
        screened = [ con for con in screened if not "14-7.31" in con.statute and not con.conviction_date < date(2004, 12, 1) ]  # pedantic exception.
        screened = [ con for con in screened if not "14-33.2" in con.statute and not con.conviction_date < date(2004, 12, 1) ]  # pedantic exception. 
        screened.sort(key=lambda x: x.offense_date)                                                               # sort by offense date
        if screened == []:
            return FinishedState().on_event(screened, dumbwaiter)
        return StrikeOne().on_event(screened, dumbwaiter)

class StrikeOne(State):
    '''StrikeOne represents the first felony for which the Defendant is convicted. These should already be sorted in order of conviction date. Only one
    conviction for felonies can count if the offense date happened before the Defendant's 18th birthday.'''
    def on_event(self, convictions:list, dumbwaiter): 
        dumbwaiter.habitual_convictions.append(convictions.pop(0))  # then add the first to dw.habitual_convictions and remove it from convictions
        return StrikeTwo().on_event(convictions, dumbwaiter)

class StrikeTwo(State): 
    '''StrikeTwo represents a defendant's second prior conviction eligible for reckoning whether they have habitual felon status. 
    The OFFENSE DATE of the second crime must be AFTER the conviction date of the first felony to count. Only one felony can count for habitual 
    felon purposes from when the Defendant was under 18.'''
    def on_event(self, convictions:list, dumbwaiter):
        adult_cons = [ c for c in convictions if dumbwaiter.over18_on_date(c.offense_date) ]    # sreen out remaining juvenile-aged offenses
        if len(adult_cons) > 0 and adult_cons[0].offense_date > dumbwaiter.habitual_convictions[-1].conviction_date: # new offense is after prior conviction
            dumbwaiter.habitual_convictions.append(adult_cons.pop(0))
            return StrikeThree().on_event(adult_cons, dumbwaiter)
        elif len(adult_cons) > 0 and adult_cons[0].offense_date <= dumbwaiter.habitual_convictions[-1].conviction_date: # new offense !after prior
            adult_cons.pop(0)       # trash it because it overlaps
            return StrikeTwo().on_event(adult_cons, dumbwaiter)   # Calling itself recursively after getting rid of the first felony (not eligible)
        else:
            return FinishedState().on_event(convictions, dumbwaiter)

class StrikeThree(State):
    def on_event(self, convictions:list, dumbwaiter):
        '''This represents the third conviction that may be eligible for habitual felony status. This will run algorithms to confirm the offense does
        qualify, and if so, will mark the status and date at which the defendant qualifies in dumbwaiter for the statemachine.'''
        if len(convictions) > 0 and convictions[-1].offense_date > dumbwaiter.habitual_convictions[-1].conviction_date:
            dumbwaiter.habitual_convictions.append(convictions.pop(0))  # add a conviction to habitual convictions and pop the first conviction
            dumbwaiter.hab_eligible = True
            dumbwaiter.date_eligible = dumbwaiter.habitual_convictions[-1].conviction_date
            return FinishedState().on_event(convictions, dumbwaiter)
        elif len(convictions) > 0 and convictions[-1].offense_date <= dumbwaiter.habitual_convictions[-1].conviction_date:
            convictions.pop(0)                                          # ditch the first conviction
            return StrikeThree().on_event(convictions, dumbwaiter)
        else:
            return FinishedState().on_event(convictions, dumbwaiter)

class FinishedState(State):
    '''This represents the end of the processing. Here, all convictions have been examined and the final results tallied in dumbwaiter.'''
    def on_event(self, convictions, dumbwaiter):
        self.convictions = convictions
        self.dumbwaiter = dumbwaiter
        self.dumbwaiter.ran = True
        return self

#--------- The actual state machine itself:-----------------
class HabitualMachine:
    '''HabitualMachine will allow a user to pass convictions to the on_event method and determine whether the record is eligible for habitual status. 
    Once this is done, the user may pass a later criminal conviction into conviction_is_eligible and the HabitualMachine instance will return whether the
    conviciton would be eligible for habitual status.'''
    def __init__(self):
        self.state = StartState() 

    def on_event(self, convictions:list, defendant_birthdate):
        _dumbwaiter = Dumbwaiter(defendant_birthdate)
        self.state = self.state.on_event(convictions, _dumbwaiter)
        self.dumbwaiter = self.state.dumbwaiter
        self.hab_eligible = self.state.dumbwaiter.hab_eligible
        self.date_eligible = self.state.dumbwaiter.date_eligible

    def offense_date_is_eligible(self, offense_date):
        '''After running a defendant's record, this takes a subsequent conviction/crime's offense date and returns whether it is eligible for habitual status.'''
        try:
            if self.dumbwaiter.ran == True:
                return self.state.dumbwaiter.offense_date_is_eligible(offense_date)
        except:
            raise ValueError("The record has not been successfully caluclated yet.")