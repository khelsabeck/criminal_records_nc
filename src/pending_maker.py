'''
This module is responsible for creating the pending charges for a given defendant.
'''
from src.charge import Charge
from datetime import date
import typing
import time

class PendingMaker:
    '''This class creates the pending charges in the CLI.'''

    def __init__(self):
        '''This method makes a list of charges and verifies that they have all 
        the appropriate data.'''
        self._stop = False
        self._pendings = []
        print("Follow the prompts to enter all pending charges (not yet \
convicted). At the beginning of each, you will be propted to type stop if \
finished.")
        time.sleep(3)
        while self._stop == False:
            print("Type 'stop' if finished or hit any key to continue!")
            _in = input()
            if "stop" in _in:
                self._stop = True
            else:
                pending = self.make_pending()
                self._pendings.append(pending)

    def make_pending(self):
        print("Type the name of the crime in 50 characters or less:")
        _crime = input()
        print("Type the class (IE: 'Infraction', 'Class 3 Misdemeanor', \
'Class 2 Misdemeanor', 'Class 1 Misdemeanor', 'Class A1 Misdemeanor', ...")
        print("'Class I Felony','Class H Felony', 'Class G Felony', \
'Class F Felony', 'Class E Felony', 'Class D Felony', 'Class C Felony', \
'Class B1 Felony',...")
        print("'Class B2 Felony', 'Class A Felony'")
        _crime_class = input()
        print(f"Type the offense date (4-digit year): ")
        _o_year = input()
        print(f"Type the offense date (month as a digit): ")
        _o_month = input()
        print(f"Type the the offense date (day as a digit): ")
        _o_day = input()
        print("Type the the conviction date (4-digit year): ")
        _conviction_date = None
        print("Type the the location (County/Court) in 50 characters \
or less: ")
        _conviction_loc = input()
        print("Type the statute in 50 characters or less (IE: \
'14-72(a)')")
        _statute = input()
        try:
            return Charge(  _crime, _crime_class, date(int(_o_year), 
                            int(_o_month), int(_o_day)), _conviction_date, 
                            _conviction_loc, _statute)
        except:
            print("There appears to be an exception. Please try again and be \
sure to read all of the prompts carefully.")
            time.sleep(3)
