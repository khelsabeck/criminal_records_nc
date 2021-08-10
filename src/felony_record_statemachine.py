'''
If a class 1 misd from Chapter 14 (general crimes), or a dwi or dwlr/I from chapter 20 is the highest conviction on a given date then that's 1 point in felony level.
Any class A1 misdemeanor (highest conviction on a given date) counts as 1 point for felony level Any H or I felony (highest ...) counts as 2 points.
A date with a E, F, or G is 4 points
A conv date with a C, D, or B2 felony counts as 6
A B1 is 9
A class A conviction is 10 points.

Levels:     Points:
1           0-1 points
2           2-5 
3           6-9
4           10-13
5           14-17
6           18+
'''
import typing
#states: 

class Crimes:
    crimes = [  "Class 1 Misdemeanor", "Class A1 Misdemeanor", "Class I Felony", "Class H Felony", "Class G Felony", "Class F", "Class E", "Class D Felony", 
            "Class C Felony", "Class B1 Felony", "Class B2 Felony", "Class A Felony" ]

class State:
    '''This is the base state for a felony record. Felony records for a person with no NC criminal history start at Level 1.'''
    def __init__(self):
        self.points = 0
        self.level = 1

    def on_event(self, convictions, points): #points starts at 0, record level 1
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

#------- These are the concrete states:------------------
class StartState(State):
    '''This represents the beginning of an FSM analyzing a criminal record based on convictions. Here, if there are no prior convictions, the \
        FinishedState should return. Otherwise, the ScreeningState should pick up the next step, screening out the convictions which do not count for a \
            felony record analysis'''
    def on_event(self, convictions:list, points:int): 
        try:
            if convictions == []:   #there are no priors
                return FinishedState().on_event(convictions, points)
            else:
                return ScreeningState().on_event(convictions, points)
            return self
        except:
            return ErrorState()

class ScreeningState(State):
    '''This State screens out any convictions that should not count in a felony record. At that point, if there are no convictions left, the code should \
        transition to FinishedState . Ortherwise (there are potentially valid convictions for calculating records), transition to RescreeningState.'''
    def on_event(self, convictions:list, points:int): 
        try:
            qualified = { 'Class 1 Misdemeanor', 'Class A1 Misdemeanor', 'Class I Felony', 'Class H Felony', 'Class F Felony', 'Class E Felony', 'Class D Felony', 
                        'Class C Felony', 'Class B1 Felony', 'Class B2 Felony' 'Class A Felony' }
            screened = [ conv for conv in convictions if conv.crime_class in qualified ]
            if screened == []:
                return FinishedState().on_event(screened, points)
            else:
                return RescreeningState().on_event(screened, points)
        except:
            return ErrorState()

class RescreeningState(State): 
    '''The only misdemeanor offenses under Chapter 20 that are assigned points for 
    determining prior record level for felony sentencing are misdemeanor death by vehicle
    [G.S. 20-141.4(a2)] and, for sentencing for felony offenses committed on or after 
    December 1, 1997, impaired driving [G.S. 20-138.1] and commercial impaired driving
    [G.S. 20-138.2]. '''
    def on_event(self, convictions:list, points:int):
        try:
            ineligibles = [ conv for conv in convictions if "20-" in conv.statute and not "20-141.4" in conv.statute and not "20-138.1" in conv.statute \
                and not "138.2" in conv.statute ]
            eligibles = list(set(convictions).difference(ineligibles))
            if eligibles == []:
                return FinishedState().on_event(eligibles, points)
            else:
                return ZippingState().on_event(eligibles, points)
        except:
            return ErrorState()

class ZippingState(State):
    '''THIS GROUPS OFFENSES BY DATE. This represents grouping all of the convictions on a given date. All convictions sharing a date in common
    should be in the same data structure (inner list), because we need to get the highest conviction on a given date.'''
    def on_event(self, convictions:list, points:int):
        try:
            unique_dates = [ conv.conviction_date for conv in convictions if conv.conviction_date not in unique_dates ]
            grouped_cons = [ [] for date in unique_dates ]
            for conv in convictions:
                grouped_cons[ unique_dates.index(conv.conviction_date) ].append(conv)
            return ZippedState().on_event(grouped_cons, points)
        except:
            return ErrorState()

class ZippedState(State):
    '''This method takes a list of lists, each inner list being all the convictions on a particular date. It creates a 1-dimensional list with the highest 
    conviction from each date and passess the list to the HubState (starting the actual calculation.'''
    def on_event(self, list_ofconvictions:list, points:int):
        try:
            l_highs = [ self.highest(convictions_onsamedate) for convictions_onsamedate in list_ofconvictions ]
            return HubState().on_event(l_highs, points)
        except:
            return ErrorState()

    @staticmethod
    def highest(convictions_onsamedate:list):
        '''This helper method takes a (sub)list of felony-point-elligible convictions having the same conviction date and returns just the one with the highest 
        class. If there are several, it only returns the first one, because the rest are redundant for calculating points.'''
        _highest = 0 #this var finds the highest class by having the classes in an ordered list and getting the index
        _conviction = None #this var gets the conviciton itself
        _crimes = Crimes()
        class_indices = _crimes.crimes      # out of the items in this list, the one with the highest index is the highest-level crime
        indices = [ class_indices.index(item.crime_class) for item in convictions_onsamedate ]
        highest = max(indices)                              # this gets the crime class corresponding to the highest class crime in convictions_onsamedate
        idx = indices.index(highest)
        conviction = convictions_onsamedate[idx]
        return conviction

class HubState(State):
    '''This state should cycle a list of the highest offense from each date and should start adding the points from them. Misdemeanors go to the misdemeanor 
    state, and felonies should trickle through a chain of felony states from high to low until their points are allotted. Each time the HubState is called, 
    if the list is non-empty, it pushes the first item through the rest of the FSM.'''

    def on_event(self, convictions:list, points:int):
        try:
            if convictions == []: # each time this is called, we are pulling off one criminal conviction from a list. When empty, FinishedState()
                return FinishedState().on_event(convictions, points)
            elif "Misdemeanor" in convictions[0].crime_class:
                return MisdemeanorState().on_event(convictions, points)
            elif "Felony" in convictions[0].crime_class:
                return FelonyStartState().on_event(convictions, points)
        except:
            return ErrorState()

class MisdemeanorState(State):
    '''An eligible misdemeanor is worth one point. This should add a point and return to HubState.'''
    def on_event(self, convictions:list, points:int):
        try:
            sliced = convictions[1:] #pulling off the first element
            if sliced == []:    
                return FinishedState().on_event(sliced, points + 1)
            else: 
                return HubState().on_event(sliced, points + 1)
        except:
            return ErrorState()

class FelonyStartState(State):
    '''Class H and I felonies are worth 2 points. This should either add 2 points and return HubState or move to the next felony state (FelonyOverHState).'''
    def on_event(self, convictions:list, points:int):
        try:
            if convictions[0].crime_class == "Class H Felony" or convictions[0].crime_class == "Class I Felony":
                return HubState().on_event(convictions[1:], points + 2)
            else:
                return FelonyOverHState().on_event(convictions, points)
        except:
            return ErrorState()

class FelonyOverHState(State):
    '''E, F, and G felonies are worth 4 points. This should either add 4 and return to HubState, or should return the next felony state, FelonyOverEState.'''
    def on_event(self, convictions, points):
        try:
            FourPt = { "Class G Felony", "Class F Felony", "Class E Felony" }
            if convictions[0].crime_class in FourPt:
                return HubState().on_event(convictions[1:], points + 4)
            else:
                return FelonyOverEState().on_event(convictions, points)
        except:
            return ErrorState()
        
class FelonyOverEState(State):
    '''D, C, and B2 felonies are worth 6 points. This should either add 6 and return to HubState or return the next highest state, FelonyOverB2State'''
    def on_event(self, convictions, points):
        try:
            SixPt = { "Class D Felony", "Class C Felony", "Class B2 Felony" }
            if convictions[0].crime_class in SixPt:
                return HubState().on_event(convictions[1:], points + 6)
            else:
                return FelonyOverB2State().on_event(convictions, points)
        except:
            return ErrorState()

class FelonyOverB2State(State):
    '''B1 felonies are worth 9 points, and A felon(y) (IE: murder) is worth 10.'''
    def on_event(self, convictions, points):
        try:
            if convictions[0].crime_class == "Class B1 Felony":
                return HubState().on_event(convictions[1:], points + 9)
            else if convictions[0].crime_class == "Class A Felony":         # murder
                return HubState().on_event(convictions[1:], points + 10)    
        except:
            return ErrorState()

class FinishedState(State):
    '''This is the end of counting up the felonies'''
    def on_event(self, convictions, points):
        try:
            self.level = self.leveler(points)
            self.convictions = convictions
            self.points = points
            return self
        except:
            return ErrorState()

    @staticmethod
    def leveler(points):
        if points < 2:
            return 1
        elif points < 6:
            return 2
        elif points < 10:
            return 3
        elif points < 14:
            return 4
        elif points < 18:
            return 5
        elif points >= 18:
            return 6

class ErrorState(State):
    '''If there is an error in one of the states, ErrorState is likely called.'''
    def on_event(self, convictions:list):
        return self

#--------- The State Machine:-----------------
class Felony_RecordMachine:
    '''Call this in client code as such:
    from felony_record_statemachine import Felony_RecordMachine
    sm = Felony_RecordMachine()
    sm.on_event(convictions)'''
    def __init__(self):
        self.state = StartState() # starting state set
    
    def on_event(self, convictions:list):
        self.state = self.state.on_event(convictions, 0)