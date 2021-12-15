'''

This module has one class, dumbwaiter, which serves as the context object for 
the habitualmachine FSM. 
Dumbwaiter has a list of habitual_convictions (convictions that have been 
validated through the FSM as counting toward hab status). 
Dumbwaiter also stores the defendant's birthdate as dw.birthdate.
Dumbwaiter also has dw.ran (bool--showing it ran successfully).
Dumbwaiter has a bool hab_eligible if the defendant is habitual eligible, and a 
date_eligible for the date at which they became eligible.
Dumbwaiter also has a method taking a new conviction and returning whether it 
is eligible to be raised to habitual status.
'''
from datetime import date

class Dumbwaiter:
    '''This is a context object the HabitualMachine FSM passes around to its 
    internal state objects. Dumbwaiter initializes with: 
    (1) a blank list of habitual convictions (representing the convictions 
    validated by the software as counting toward habitual status);
    (2) hab_eligible set as False (representing that the Defendant is not 
    eligible for habitual status;
    (3) a birthdate, which is required and must be a datetime date object. '''
    def __init__(self, birthdate):
        self.habitual_convictions = []
        self.set_hab_eligible(False)
        self._date_eligible = None
        self.set_birthdate(birthdate)
        self.ran = False                # when the program's run, set as True

    def set_birthdate(self, birthdate):
        '''This should set the birthdate value IFF is is a valid datetime 
        date object.'''
        if (type(birthdate) == date):
            self._birthdate = birthdate
        else:
            raise ValueError("The defendant's birthdate is a prerequisite for \
habitual felon analysis, and it must be a valid datetime 'date' object.")

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
        else:
            raise ValueError("The hab_eligible value must be a boolean.")

    @property
    def hab_eligible(self):
        return self._hab_eligible

    @hab_eligible.setter
    def hab_eligible(self, hab_eligible:bool):
        self.set_hab_eligible(hab_eligible)

    def over18_on_date(self, _date):

        '''This takes a datetime date object and determines whether the 
        defendant was over 18 on that date. Any param but a date will raise 
        ValueError'''
        if type(_date) != date:
            raise ValueError("The method over18_on_date() in Dumbwaiter \
requires a datetime date as a parameter.")
        if _date >= self.eighteenth_birthdate:
            return True
        return False

    @property
    def eighteenth_birthdate(self):
        '''This takes the _brithdate value and returns the eighteenth birthdate
        of the denfendat.'''
        eighteenth = date(  self._birthdate.year + 18, self._birthdate.month, 
                            self._birthdate.day)
        return eighteenth

    def set_date_eligible(self, conviction_date):
        '''This sets the date at which the defendant became habitual-eligible.
        This method takes the conviction date and checks its conviction date.
        If it is a valid datetime date object, then this method sets that 
        value as the date at which the defendant with the given convictions 
        and birthdate became eligible
        for habitual status. Any felony facing possible habitual aggravated
        status must have an offense date later than the date_eligible 
        value.'''
        if type(conviction_date) == date:
            self._date_eligible = conviction_date
        else:
            raise ValueError("The method set_date_eligible() in Dumbwaiter \
requires a datetime date as a parameter.")

    @property
    def date_eligible(self):
        return self._date_eligible

    @date_eligible.setter
    def date_eligible(self, conviction):
        self.set_date_eligible(conviction)

    def offense_date_is_eligible(self, offense_date):
        '''After running a defendant's record, this takes a conviction and 
        determines whether the conviction is eligible for habitual aggravated 
        status.'''
        if self.hab_eligible and offense_date > self.date_eligible:
            return True
        else:
            return False