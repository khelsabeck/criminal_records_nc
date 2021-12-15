'''
This is a custom data structure for getting all of the charges for a given D. 
A rewrite, it could clean up the fsms for analyzing pending
charges and criminal records/points and habitual felon eligibility.

It has a list for all of the pending charges, and add and remove functions.

Remember, a D can be charged more than once with crimes/charges having 
identical data. IE: John Doe is charged with two counts of larceny on the 
same date, or
Jane Doe is charged with resisting, delaying, and obstructing (or 
assaulting) two officers out of the same incident.
'''
import typing
from .charge import Charge

class Charge_Collection:
    '''This is a class for making and storing pending charges. A 
    Pending_Charges instance stores charges in the _pending list structure, and 
    creates
    this list on initilaization. Pending_Charges has a method add_charge for 
    adding another pending charge to the private list structure (takes the charge
    to be added as a param). It also has a remove_charge method for removing a 
    given charge (takes the charge to be removed as a param). It also has an 
    is_in method for determining if a given charge is in the _pendings (takes 
    a charge as a param). The instance.pending property returns a COPY of the 
    _pendings.'''

    def __init__(self):
        self._reset_charges()

    def _reset_charges(self):
        '''This sets _charges as an empty list.'''
        self._charges = []
    
    def add_charge(self, charge):
        '''This adds a pending charge after validating that it is a charge 
        object.'''
        if Charge == type(charge):
            self._charges.append(charge)
        else:
            raise ValueError("Only valid Charge objects may be added to a \
Defendant's charges.")

    def remove_charge(self, index):
        '''This deletes a charge from the charges by index. There is no remove 
        by value because there can be multiple identical charges (same data 
        fields) for a given defendant. IE: John Doe is charged with two counts 
        of larceny on the same date, or Jane Doe is charged with resisting, 
        delaying, and obstructing (or assaulting) two officers out of the 
        same incident.'''
        try:
            del self._charges[index]
        except:
            raise ValueError("This charge is not in _charges.")

    def is_in(self, charge):
        '''This returns True if the charge is present in _charges, and \
otherwise False.'''
        if charge in self.charges:
            return True
        else:
            return False

    @property
    def charges(self):
        '''This returns a COPY of the _charges list, and not the actual list 
        structure.'''
        return self._charges.copy()

class Pending_Charges(Charge_Collection):
    '''This is the custom collection model for a defendant's convictions'''
    def __init__(self):
        super().__init__(self):

    def sort_byoffensedate(self):
        '''This sorts the collection by the conviction dates of the charges 
        from earliest to latest.'''
        return self.charges.sort(key=lambda x: x.offense_date) 

class Charges_Convicted(Charge_Collection):
    '''This is the custom collection model for a defendant's convictions'''

    def __init__(self):
        super().__init__(self):

    def sort_collection_byconviction(self):
        '''This sorts the collection by the conviction dates of the charges 
        from earliest to latest.'''
        return copy( self.charges.sort(key=lambda x: x.conviction_date) )

    def group_collection_byconvictiondate(self):
        '''This groups the collection by the conviction dates of the charges 
        from earliest to latest, returning a 2-d list, each inner list being 
        all the convictions on a given day.'''
        sorted_charges = self.sort_collection_byconviction()
        unique_dates = []
        for charge in sorted_charges:
            if charge.conviction_date not in unique_dates:
                unique_dates.append(charge.conviction_date)
        empty_lists = [ [] for date in unique_dates ]
        current_date = sorted_charges[0].conviction_date
        index = 0
        for charge in sorted_charges:
            if charge.conviction_date != current_date:
                current_date = charge.conviction_date
                index += 1
                empty_list[index].append(charge)
            else:
                empty_list[index].append(charge)