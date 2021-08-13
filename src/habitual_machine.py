'''
Author: Keith Hinkleman Helsabeck

The plan for this module is to determine whether a given set of convictions qualify a defendant as a habitual felon in North Carolina. I am adapting 
this from a prior program I wrote for internal use in a Django project (not currently online).

Habitual Felony in NC:
Habitual status is an OPTIONAL consideration in NC sentencing and can allow a prosecutor and judge to raise the sentence of a felony crime to a sentence 
corresponding with a felony offense three levels higher than the actual crime (which is a BIG JUMP!). 

A defendant is eligible for habitual status if and only if:
(1) The Defendant has had three prior periods of non-overlapping offense dates and convictions for eligible felonies. IE: Jim commits Offense 1 on Date 1, then 
Offense1 is convicted on Date2, and THEN (after that conviction) he commits Offense2 on Date3, and Offense2 is convicted on Date4.
(2) No more than one of those can count if the Defendant was under 18.
'''
from datetime import date, timedelta

class Dumbwaiter:
    '''This is a context object the HabitualMachine FSM passes around to its internal state objects. Dumbwaiter initializes with: 
    (1) a blank list of habitual convictions (representing the convictions validated by the software as counting toward habitual status);
    (2) hab_eligible set as False (representing that the Defendant is not eligible for habitual status;
    (3) a birthdate, which is required and must be a datetime date object. '''
    def __init__(self, birthdate):
        self.habitual_convictions = []
        self.set_hab_eligible()
        self._date_eligible = None
        self.set_birthdate(birthdate)

    def set_birthdate(self, birthdate):
        '''This should set the birthdate value IFF is is a valid datetime date object.'''
        if (type(birthdate) == date):
            self._birtdate = birthdate
        else:
            raise ValueError("The defendant's birthdate is a prerequisite for habitual felon analysis, and it must be a valid datetime 'date' object.")

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, birthdate):
        self.set_birthdate(birthdate)

    def set_hab_eligible(self, hab_eligible:bool):
        '''This should set hab_eligible if the input value is a boolean'''
        if type(hab_eligible) == bool:
            self._hab_eligible = hab_eligible

    @property
    def hab_eligible(self):
        return self._hab_eligible

    @hab_eligible.setter
    def hab_eligible(self, hab_eligible):
        self.set_hab_eligible(hab_eligible)

    def over18_on_date(self, _date):
        '''This takes a datetime date object and determines whether the defendant was over 18 on that date. Any param but a date will raise ValueError'''
        if type(_date) != date:
            raise ValueError("The method over18_on_date() in Dumbwaiter requires a datetime date as a parameter.")
        if _date > self.eighteenth_birthdate:
            return True
        return False

    @property
    def eighteenth_birthdate(self):
        '''This takes the _brithdate value and returns the eighteenth birthdate of the denfendat.'''
        eighteenth = date(self._birthdate.year + 18, self._birthdate.month, self._birthdate.day)
        return eighteenth

    def set_date_eligible(self, conviction):
        '''This sets the date at which the defendant became habitual-eligible. This method takes the conviction object and checks its conviction date. If it is
        a valid datetime date object, then this method sets that value as the date at which the defendant with the given convictions and birthdate became eligible
        for habitual status. Any felony facing possible habitual aggravated status must have an offense date later than the date_eligible value.'''
        if type(conviction.conviction_date) == date:
            self._date_eligible = conviction.conviction_date
        else:
            raise ValueError("The method set_date_eligible() in Dumbwaiter requires a datetime date as a parameter.")

    @property
    def date_eligible(self):
        return self._date_eligible

    @date_eligible.setter
    def date_eligible(self, conviction):
        self.set_date_eligible(conviction)

    @property
    def conviction_is_eligible(self, conviciton):
        '''After running a defendant's record, this takes a conviction and determines whether the conviction is eligible for habitual aggravated status.'''
        if self.hab_eligible and conviction.offense_date > self.date_eligible:
            return True
        else:
            return False

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
    non-eligible '''
    def on_event(self, convictions:list, dumbwaiter): 
        try:
            eligible = [ 'Class I Felony', 'Class H Felony','Class G Felony', 'Class F Felony',
            'Class E Felony','Class D Felony','Class C Felony','Class B2 Felony','Class B1 Felony',
            'Class A Felony' ]
            eligible_convs = [ c for c in convs if c.crime_class in eligible ]                                              # eliminate all cons but felonies
            eligible_convs = [ c for c in eligible_convs if "14-7.31" not in c.statute and "14-33.2" not in c.statute ]     # pedantic exceptions
            eligible_convs.sort(key=lambda x: x.offense_date)                                                               # sort by offense date
            if eligible_convs == []:
                return FinishedState().on_event(eligible_convs, context)
            return FirstConviction().on_event(eligible_convs, context)
        except:
            dumbwaiter.error = "An unknwon error occured in StartState."
            return ErrorState().on_event(convictions, context)

class FirstConviction(State):
    '''FirstConviction represents the first felony for which the Defendant is convicted. These should already be sorted in order of conviction date. Only one
    conviction for felonies can count if the offense date happened before the Defendant's 18th birthday.'''
    def on_event(self, convictions:list, dumbwaiter): 
        try:
            if len(convictions) > 0:                                        # if there are one or more convictions left after screening out ineligibles
                dumbwaiter.habitual_convictions.append(convictions.pop(0))
                return SecondConviction().on_event(convictions, dumbwaiter)
            else:
                return FinishedState().on_event(convictions, dumbwaiter)    # there are no habitual-eligibles
        except:
            dumbwaiter.error = "An unknwon error occured in FirstConviction."
            return ErrorState().on_event(convictions, dumbwaiter)

class SecondConviction(State): 
    '''SecondConviction represents a defendant's second prior conviction eligible for reckoning whether they have habitual felon status. 
    The OFFENSE DATE of the second crime must be AFTER the conviction date of the first felony to count. Only one felony can count for habitual 
    felon purposes from when the Defendant was under 18.'''
    def on_event(self, convictions:list, dumbwaiter):
        convictions = self.remove_convictions_under18(convictions)
        try:    
            if len(convictions) > 0 and convictions[0].offense_date > dumbwaiter.habitual_convictions[0].conviction_date: 
                dumbwaiter.habitual_convictions.append(convictions.pop(0))
                return ThirdConviction().on_event(convictions, dumbwaiter)
            elif len(convictions) > 0 and convictions[0].offense_date <= dumbwaiter.habitual_convictions[0].conviction_date:
                dumbwaiter.habitual_convictions.append(convictions.pop(0))
                return SecondConvition(convictions, dumbwaiter)   # Calling itself recursively after getting rid of the first felony (not eligible)
            else:
                return FinishedState().on_event(convs, dumbwaiter)
        except:
            dumbwaiter.error = "An unknwon error occured in SecondConviction."
            return ErrorState().on_event(convs, dumbwaiter)

    def remove_convictions_under18(self, convictions:list, dumbwaiter):
        '''Upstream code ordered all convictions by date, and then found a conviction. If this second habitual-eligible felony conviction happened when
        the defendant was 18, then the first did too, and therefore we should ditch it.'''
        try:                                                                # screening out convictions where offense date prior to 18th bday
            convictions = [ c for c in convictions if dumbwaiter.overeighteen_ondate(c.offense_date) ]
        except:
            return ErrorState().on_event(convictions, dumbwaiter)

class ThirdConviction(State):
    def on_event(self, convictions:list, dumbwaiter):
        '''This represents the third conviction that may be eligible for habitual felony status. This will run algorithms to confirm the offense does
        qualify, and if so, will mark the status and date at which the defendant qualifies in dumbwaiter for the statemachine.'''
        try:
            if len(convictions) > 0 and convictions[1].offense_date > dumbwaiter.habitual_convictions[1].conviction_date:
                dumbwaiter.habitual_convictions.append(convictions.pop(0))
                dumbwaiter.habitual_eligible = True
                dumbwaiter.date_eligible = convictions[1].offense_date
                return FinishedState().on_event(convictions, dumbwaiter)
            else:
                convictions.pop(0)
                return FinishedState().on_event(convictions, dumbwaiter)
        except:
            dumbwaiter.error = "An unknwon error occured in ThirdConviction."
            return ErrorState().on_event(convictions, dumbwaiter)

class FinishedState(State):
    '''This represents the end of the processing. Here, all convictions have been examined and the final results tallied in dumbwaiter.'''
    def on_event(self, convictions, dumbwaiter):
        self.convictions = convictions
        self.dumbwaiter = dumbwaiter
        return self

class ErrorState(State):
    '''This represents an error from the code in the previous states.'''
    def on_event(self, convictions, dumbwaiter):
        self.convictions = convictions
        self.dumbwaiter = dumbwaiter
        return self

#--------- The actual state machine itself:-----------------
class HabitualMachine:
    '''HabitualMachine will allow a user to pass convictions to the on_event method and determine whether the record is eligible for habitual status. 
    Once this is done, the user may pass a later criminal conviction into conviction_is_eligible and the HabitualMachine instance will return whether the
    conviciton would be eligible for habitual status.'''
    def __init__(self):
        self.state = StartState() 

    def on_event(self, convictions):
        dumbwaiter = Dumbwaiter()
        self.state = self.state.on_event(convictions, dumbwaiter)
        self.hab_eligible = self.state.hab_eligible
        self.date_eligible = self.state.date_eligible

    def conviction_is_eligible(self, conviction):
        '''After running a defendant's record, this takes a subsequent conviction/crime and returns whether it is eligible for habitual status.'''
        return self.state.dumbwaiter.conviction_is_eligible(conviction)
