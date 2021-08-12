from datetime import date, datetime, timedelta
import typing

class Defendant:
    def __init__(self, first:str, last:str, birthdate):
        '''This takes three arguments: a firstname, lastname, and birthdate. The names should be non-zero-length strings without whitespace. The birthdate
        should be a valid datetime date object. The values will be given basic validation and encapsulated. They will return (here) as properties returning
        private vars.'''
        self.set_first(first)
        self.set_last(last)
        self.set_birthdate(birthdate)

    def set_first(self, first:str):
        '''This sets an empty string as the default for _first and validates that the first name value is a contiguous string without whitespace of 
        1 to 25 chars. Otherwise it creates a ValueError with an appropriate message'''
        self._first = ''
        if self.validate_contiguous_str(first):
            self._first = first[:25]

    def set_last(self, last:str):
        '''This sets an empty string as the default for _last and validates that the last name value is a contiguous string without whitespace of 
        1 to 25 chars. Otherwise it creates a ValueError with an appropriate message'''
        if self.validate_contiguous_str(last):
            self._last = last[:25]

    def validate_contiguous_str(self, s:str):
        '''This validates that the value is a string of non-zero length without any whitespace/blanks between chars'''
        if type(s) == str and len(s) > 0 and len(s.split()) == 1:
            return True
        else:
            raise ValueError("The value failed to validate. It should be a string of non-zero length with no whitespace.")
    
    def set_birthdate(self, birthdate):
        '''This validates the birthdate as a proper datetime date object.'''
        if type(birthdate) == date:
            self._birthdate = birthdate
        else:
            raise ValueError("The birthdate must be a datetime date object.")

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, first:str):
        if self.validate_contiguous_str(first):
            self._first = first

    @property
    def last(self):
        return self._last    

    @last.setter
    def last(self, last:str):
        if self.validate_contiguous_str(last):
            self._last = last

    @property
    def fullname(self):
        '''This returns a full name value'''
        return f"{self._first} {self._last}"

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, birthdate):
        self.set_birthdate(birthdate)