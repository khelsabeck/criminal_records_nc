'''
This is a tool for calculating a defendant's misdemeanor record level. It should take a list of convictions and return:
    (1) the points, 
    (2) the record level,   
    (3) a list of qualified convictions, 
    (4) the date the Defendant qualifies as a record level 2 and/or 3 (if so).
'''

class State:
    '''This is the base state for a misdemeanor record. Misdemeanor records for a person with no NC criminal history start at Level 1with 0 points.'''
    def __init__(self):
        self.points = 0
        self.level = 1

    def on_event(self, convictions:list, points:int): 
        '''This method in concrete states will take two positional params (list of convictions and int for number of points. It will cary out the 
        work of each concrete state and move to the next. points start at 0, record level at 1'''
        pass 

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

#------- These are the concrete states:------------------
class StartState(State):
    '''This represents the beginning of an statemachine analyzing a criminal record based on convictions. Here, if there are no prior convictions, the \
        FinishedState should return. Otherwise, the ScreeningState should pick up the next step, screening out the convictions which do not count for a \
            misdemeanot record.'''
    def on_event(self, convictions:list, points:int): 
        if convictions == []:     # there are no priors
            return FinishedState().on_event(convictions, points)
        elif type(convictions) == list and len(convictions) >= 1:   # apparently there are one or more convictions
            return ScreeningState().on_event(convictions, points)
        else:
            raise ValueError("There was an exception in the StartState. The parameter values are likely invalid.")

class ScreeningState(State):
    '''This State screens out any convictions that cannot count in a misdemeanor record. At that point, if there are no convictions left, the code should \
        transition to FinishedState . Ortherwise, transition to RescreeningState for further pre-processing steps.'''
    def on_event(self, convictions:list, points:int): 
        screened = [ conv for conv in convictions if conv.is_felony or conv.is_misdemeanor ]    # felonies and misdemeanors count for misdemeanor records
        if screened == []:
            return FinishedState().on_event(screened, points)
        else:
            return ZippingState().on_event(screened, points)

class ZippingState(State):
    '''THIS GROUPS OFFENSES BY DATE. This represents grouping all of the convictions on a given date. All convictions sharing a date in common
    should be in the same data structure (inner list), because we need to get the highest conviction on a given date.'''
    def on_event(self, convictions:list, points:int):
        unique_dates = self.make_list_of_unique_dates(convictions)
        empties = self.make_list_of_empties(unique_dates)
        grouped_convictions = self.fill_empties(convictions, unique_dates, empties)
        return FinishedState().on_event(grouped_convictions, points)
    
    def make_list_of_unique_dates(self, convictions:list):
        '''This takes a list of convictions and returns a list of all the unique conviction dates.'''
        all_dates = [ c.conviction_date for c in convictions ]
        uniques = list(set(all_dates))
        return uniques   # should return datetime dates in chronological order (earliest to latest)

    def make_list_of_empties(self, unique_dates:list):
        '''This takes a list of unique dates and returns a 2-D list with an (inner) empty list for each unique date. Plan to fill each list with the
        convictions from the corresponding date'''
        empties = [ [] for date in unique_dates ]
        return empties

    def fill_empties(self, convictions:list, unique_dates:list, empties:list):
        '''This helper puts convictions with the same conviction_date value in the same inner list of a 2-D list.'''
        convictions_grouped_bydate = empties
        for c in convictions:
            index_matchingdate = unique_dates.index(c.conviction_date)
            convictions_grouped_bydate[ index_matchingdate ].append(c)
        return convictions_grouped_bydate

class FinishedState(State):
    '''This is the end state and hanles calculating the points.'''
    def on_event(self, convictions_grouped_bydate:list, points:int):
        '''This mehtod takes a list of lists. Each inner list represents all the convictions on a given date, having screened out the non-qualified offenses for
        misdemeanor sentencing (ie: infractions). Each separate conviction date counts as 1 point. 0 points returns level 1; 1-4 points returns level 2; and 
        5+ points returns level 3.'''
        self.points = len(convictions_grouped_bydate)
        self.level = self.leveler()
        self.convictions = self.flattener(convictions_grouped_bydate)
        return self

    def leveler(self):
        '''This simply takes the misdemeanor points for a record and returns the appropriate level for the number of points. 0 points returns level 1; 
        1-4 points returns level 2; and 5+ points returns level 3.'''
        if self.points < 1:
            return 1
        elif 1 <= self.points < 5:
            return 2
        else:
            return 3
    
    def flattener(self, convictions_grouped_bydate:list):
        '''This flattens out a 2-D list (lists of convictions grouped by date.'''
        convictions = []
        for _list in convictions_grouped_bydate:
            convictions.extend(_list)
        return convictions

#--------- The State Machine:-----------------
class MisdemeanorRecordMachine:
    '''MisdmeanorRecordMachine calculates a defendant's misdemeanor record from a list of convictions. The on_event() method and determines the number of 
    points and the level for misdemeanor sentencing.

    It will return these values:
    (1) the points, 
    (2) the record level,   
    (3) a list of qualified convictions, 
    (4) the date the Defendant qualifies as a record level 2 and/or 3 (if so).
'''
    def __init__(self):
        self.state = StartState() # starting state set
    
    def on_event(self, convictions:list):
        '''This method takes a list of convictions and runs the logic of determining the level and points. '''
        self.state = self.state.on_event(convictions, 0)

    @property
    def points(self):
        if FinishedState == type(self.state):
            return self.state.points
        else:
            raise Exception("The points cannot be determined until the on_event() method has run with the record.")

    @property
    def level(self):
        if FinishedState == type(self.state):
            return self.state.level
        else:
            raise Exception("The level cannot be determined until the on_event() method has run with the record.")
