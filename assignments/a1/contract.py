"""
CSC148, Winter 2023
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class MTMContract(Contract):
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract

    end:
        ending date for contract

    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """

    start: datetime.datetime
    end: Optional[datetime.datetime] = None
    bill: Optional[Bill] = None

    def __init__(self, start: datetime.date) -> None:
        """ Create a new MTMContract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)
        self._end = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        bill.add_fixed_cost(MTM_MONTHLY_FEE)
        bill.set_rates('MTM', MTM_MINS_COST)
        self.bill = bill


class TermContract(Contract):
    """ A contract for a phone line

        === Public Attributes ===
        start:
             starting date for the contract

        end:
            ending date for contract

        bill:
             bill for this contract
        """

    start: datetime.date
    _end: Optional[datetime.date] = None
    _curr: datetime.datetime
    bill: Optional[Bill]
    _free: int

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)
        self.end = None
        self._free = TERM_MINS
        self._curr = start

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        bill.set_rates('TERM', TERM_MINS_COST)
        bill.add_fixed_cost(TERM_MONTHLY_FEE)
        if month == self.start.month and year == self.start.year:
            bill.add_fixed_cost(TERM_DEPOSIT)
        self._curr = datetime.datetime(year, month, 1)

        self.bill = bill

        def bill_call(self, call: Call) -> None:
            """ Add the <call> to the bill.

            Precondition:
            - a bill has already been created for the month+year when the <call>
            was made. In other words,
            you can safely assume that self.bill has been
            already advanced to the right month+year.
            """

            minutes = ceil(call.duration / 60.0)
            if self._free >= minutes:
                self._free -= minutes
                self.bill.add_free_minutes(minutes)
            elif minutes >= self._free >= 0:
                self.bill.add_free_minutes(self._free)
                self.bill.add_billed_minutes(minutes - self._free)
                self._free = 0
            else:
                self.bill.add_billed_minutes(minutes)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # self.start = None
        # return self.bill.get_cost()

        self.start = None
        if self._curr > self.end:
            return self.bill.get_cost() - TERM_DEPOSIT
        else:
            return self.bill.get_cost()


class PrepaidContract(Contract):
    """ A contract for a phone line

        This class is not to be changed or instantiated.
        It is an Abstract Class.

        === Public Attributes ===
        start:
             starting date for the contract
        bill:
             bill for this contract for the last month of
             call records loaded from the input dataset
        balance :
                balance

        """

    start: datetime.datetime
    _end: datetime.datetime
    bill: Optional[Bill]
    _balance: int

    def __init__(self, start: datetime.date, balance) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)
        self._end = None
        self._balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """

        PREPAID_BALANCE_THRESHOLD = -10

        bill.set_rates('PREPAID', PREPAID_MINS_COST)
        if self.bill is not None:
            self._balance += self.bill.get_cost()
        self._balance -= PREPAID_BALANCE_THRESHOLD
        if self._balance < 0:
            bill.add_fixed_cost(abs(self._balance))
            self._balance = 0
        self.bill = bill

        def cancel_contract(self) -> float:
            """ Return the amount owed in order to close the
            phone line associated with this contract.

            Precondition:
            - a bill has already been created for the month+year
            when this contract is being cancelled.
            In other words, you can safely assume that self.bill
            exists for the right month+year when the cancelation is requested.
            """

            self.start = None
            if self.bill.get_cost() > 0:
                return self.bill.get_cost()
            else:
                return 0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
