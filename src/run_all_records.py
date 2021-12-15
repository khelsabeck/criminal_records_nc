'''
This module runs all of the criminal records for a single defendant and 
gives the appropriate output.

Responsibility:

(1) run misdemeanorrecordmachine
(2) run felonyrecordmachine
(3) run habitual_machine
(4) run dwi_factormachine
'''
from src.charge import Charge
from src.defendant import Defendant
from src.felony_record_statemachine import Felony_RecordMachine
from src.habitual_machine import HabitualMachine
from src.misdemeanor_recordmachine import MisdemeanorRecordMachine
from src.defendant_maker import DefendantMaker
from src.record_maker import RecordMaker
from src.pending_maker import PendingMaker
import typing
import copy

class Runner:
    '''This class runs the record.'''

    def __init__(self):
        '''This method takes the defendant and the convictions and runs 
        the records.'''
        self._defendant = DefendantMaker()._defendant
        self._convictions = RecordMaker()._convictions
        self._pendings = PendingMaker()._pendings
        self._misdemeanor_recordmachine = MisdemeanorRecordMachine()
        self._misdemeanor_recordmachine.on_event(copy.copy(self._convictions))
        self._felony_recordmachine = Felony_RecordMachine()
        self._felony_recordmachine.on_event(copy.copy(self._convictions))
        self._habitualmachine = HabitualMachine()
        self._habitualmachine.on_event( \
            copy.copy(self._convictions), self._defendant.birthdate)
        self.get_printout()

    @property
    def is_habitual(self):
        '''This returns True if the Defendant is habitual eligible, or else 
        false.'''
        return self._habitualmachine.hab_eligible

    @property
    def date_eligible(self):
        '''This returns the date at which the Defendant became eligible for 
        habitual status.'''
        return self._habitualmachine.date_eligible

    @property
    def misdemeanorpoints(self):
        '''This returns the number of misdmenaor record points.'''
        return self._misdemeanor_recordmachine.points

    @property
    def misdemeanorlevel(self):
        '''This returns the misdmenaor record level.'''
        return self._misdemeanor_recordmachine.level

    @property
    def felonypoints(self):
        '''This returns the number of felony record points.'''
        return self._felony_recordmachine.points

    @property
    def felonylevel(self):
        '''This returns the felony record level.'''
        return self._felony_recordmachine.level

    def get_printout(self):
        '''This prints out the takeaway information.'''
        print(f"{self._defendant.first} {self._defendant.last}, \
born {self._defendant.birthdate.isoformat()}:")
        print(f"Convictions:\t{str(self._convictions)}")
        print(f"Misdemeanor points:\t{self.misdemeanorpoints}")
        print(f"Misdemeanor level:\t{self.misdemeanorlevel}")
        print(f"Felony points:\t\t{self.felonypoints}")
        print(f"Felony level:\t\t{self.felonylevel}")
        print(f"Habitual Felony Eligible:\t{self.is_habitual}")
        print(f"Habitual Eligible as of:\t{self.date_eligible}")
        print()
        print(f"Pending Charges:\t{str(self._pendings)}")