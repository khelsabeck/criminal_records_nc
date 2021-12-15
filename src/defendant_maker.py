'''
This makes the Defendant for the CLI.
'''
from src.defendant import Defendant
from datetime import date
import typing
import time

class DefendantMaker:
    '''This class object just runs prompts in the CLI to make a Defendant and 
    returns the Defendant.'''

    def __init__(self):
        '''This prompts the user for the data to make a Defendant and returns 
        the D.'''
        self._defendant = self.get_defendant()

    def get_defendant(self):
        '''This runs the prompts and returns the defendant.'''
        _stop = False
        while _stop == False:
            print("Please enter the Defendant's first name:")
            _first = input()
            print("Please enter the Defendant's last name:")
            _last = input()
            print("Please enter the Defendant's birth year as a 4-digit number \
(ie: 1990):")
            _year = input()
            print("Please enter the Defendant's birth month in digits (ie: \
August is 8, October is 10):")
            _month = input()
            print("Please enter the day of the month the Defendant was born \
in digits (ie: '5' or '19'):")
            _day = input()
            try:
                return Defendant(   _first, _last, date(int(_year), int(_month), 
                                    int(_day)))
                _stop = True
            except:
                print("There was a problem making a defendant with the \
information you provided. Please try again and follow the prompts carefully.")