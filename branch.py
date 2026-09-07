from datetime import datetime


class Branch:
    """Store a branch's details and open or closed status.

    Attributes
    ----------
    __next_number : int
        The next available branch number.
    __number : int
        The branch's unique number.
    __name : str or None
        The branch name.
    __suburb : str or None
        The suburb where the branch is located.
    __phone_number : str or None
        The branch phone number.
    __is_open : bool
        Whether the branch is open.

    Methods
    -------
    __str__()
        Return readable branch information.
    __repr__()
        Return detailed branch information.
    open()
        Open the branch.
    close()
        Close the branch.
    set_phone_number(new_number)
        Update the branch phone number.
    get_number()
        Return the branch number.
    """
    __next_number = 1

    def __init__(self, name: str, suburb: str, phone_number: str):
        """Create a closed branch.

        Parameters
        ----------
        name : str
            The branch name.
        suburb : str
            The suburb where the branch is located.
        phone_number : str
            The branch phone number.
        """

        self.__number = Branch.__next_number
        Branch.__next_number += 1
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = None
        if isinstance(suburb, str):
            self.__suburb = suburb
        else:
            self.__suburb = None
        if isinstance(phone_number, str):
            self.__phone_number = phone_number
        else:
            self.__phone_number = None
        self.__is_open = False

    def __str__(self):
        if self.__is_open:
            branch_status = 'Open'
        else:
            branch_status = 'Closed'

        return (
            f'Branch number: {self.__number}, '
            f'Name: {self.__name}, '
            f'Suburb: {self.__suburb}, '
            f'Phone number: {self.__phone_number}, '
            f'Status: {branch_status}'
        )

    def __repr__(self):
        return (
            f'Branch('
            f'number={self.__number!r}, '
            f'name={self.__name!r}, '
            f'suburb={self.__suburb!r}, '
            f'phone_number={self.__phone_number!r}, '
            f'is_open={self.__is_open!r}'
            f')'
        )

    def open(self):
        """Open the branch and print the time of the change."""
        self.__is_open = True
        print(f'{self.__name} is open as of {datetime.now()}')
        return

    def close(self):
        """Close the branch and print the time of the change."""
        self.__is_open = False
        print(f'{self.__name} is closed as of {datetime.now()}')
        return

    # --------
    # Getter
    # --------

    def get_number(self):
        return self.__number

    # ---------
    # Setter
    # ---------

    def set_phone_number(self, new_number: str):
        if isinstance(new_number, str):
            old_number = self.__phone_number
            self.__phone_number = new_number
            print(
                f'Phone number is updated successfully: '
                f'{old_number} -> {self.__phone_number} '
                f'as of {datetime.now()}.'
            )

    # ----------
    # Properties
    # ----------

    number = property(get_number)
    phone_number = property(fset=set_phone_number)
