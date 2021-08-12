from datetime import date, datetime, timedelta
import typing

class Conviction:
    def __init__(self, crime:str, crime_class:str, conviction_date, conviction_loc:str, statute:str):
        self._valid_classes = [ "Infraction", "Class 3 Misdemeanor", "Class 2 Misdemeanor", "Class 1 Misdemeanor", "Class A1 Misdemeanor", "Class I Felony",
                        "Class H Felony", "Class G Felony", "Class F Felony", "Class E Felony", "Class D Felony", "Class C Felony", "Class B1 Felony",
                        "Class B2 Felony", "Class A Felony" ]
        self.set_crime(crime)
        self.set_crime_class(crime_class)
        self.set_conviction_date(conviction_date)
        self.set_conviction_loc(conviction_loc)
        self.set_statute(statute)

    def set_crime_class(self, crime_class:str):
        '''This should validate a crime_class from a list of valid crime_classes.'''
        if crime_class in self._valid_classes:
            self._crime_class = crime_class
        else:
            raise ValueError(f"The crime class is not a valid crime class. Valid Crime classes are {str(self._valid_classes)}.")

    def validate_contiguous_str(self, s:str):
        '''This method validates that the input is a string of non-zero length and that it has no whitespace between chars'''
        if type(s) == str and len(s) > 0 and len(s.split()) == 1:
            return True
        else:
            raise ValueError("The value failed to validate. It should be a string of non-zero length with no whitespace.")

    @property
    def crime_class(self):
        '''This returns the _crime_class value when crime_class is dereferenced.'''
        return self._crime_class

    @crime_class.setter
    def crime_class(self, crime_class:str):
        '''This ensures the validation runs before setting the _crime_class value'''
        self.set_crime_class(crime_class)

    def validate_date(self, conviction_date):
        if type(conviction_date) == date:
            return True
        else:
            raise ValueError("The conviction_date must be a valid datetime date object.")

    def set_conviction_date(self, conviction_date):
        '''This validates the conviction_date is a datetime date object, or raises a ValueError with an appropriate message'''
        if self.validate_date(conviction_date):
            self._conviction_date = conviction_date

    @property
    def conviction_date(self):
        return self._conviction_date

    @conviction_date.setter
    def conviction_date(self, conviction_date):
        self.set_conviction_date(conviction_date)

    def set_crime(self, crime:str):
        if type(crime) == str and len(crime) > 0:
            self._crime = crime[:50]
        else:
            raise ValueError("A crime should be a string of non-zero length (up to 50 chars).")

    @property
    def crime(self):
        return self._crime

    @crime.setter
    def crime(self, crime):
        self.set_crime(crime)
    
    def set_conviction_loc(self, conviction_loc:str):
        '''This runs the validation and setting logic for the conviction_loc value (location)'''
        if type(conviction_loc) == str and len(conviction_loc) > 0:
            self._conviction_loc = conviction_loc[:50]
        else:
            raise ValueError("A conviction location value should be a string of non-zero length (up to 50 chars).")
    
    @property
    def conviction_loc(self):
        return self._conviction_loc

    @conviction_loc.setter
    def conviction_loc(self, conviction_loc):
        self.set_conviction_loc(conviction_loc)

    def set_statute(self, statute:str):
        if type(statute) == str and len(statute) > 0:
            self._statute = statute[:50]
        else:
            raise ValueError("The Statute should be a string valud between 1 and 50 characters.")

    @property
    def statute(self):
        return self._statute

    @statute.setter
    def statute(self, statute:str):
        self.set_statute(statute)