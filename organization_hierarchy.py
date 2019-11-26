"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    return_list = []

    # This checks to see if any of the lists are empty.
    if len(lst1) == 0:
        return_list.extend(lst2)
        return return_list

    if len(lst2) == 0:
        return_list.extend(lst1)
        return return_list

    # Our index counters:
    i = 0
    j = 0
    length_lst1 = len(lst1)
    length_lst2 = len(lst2)

    while i < length_lst1 or j < length_lst2:
        # This finishes off the other list if one of them had all of its
        # elements already added in.
        if i == length_lst1:
            return_list.extend(lst2[j:])
            break

        if j == length_lst2:
            return_list.extend(lst1[i:])
            break

        # This appends a single element.
        if lst1[i] < lst2[j]:
            return_list.append(lst1[i])
            i += 1
        else:
            return_list.append(lst2[j])
            j += 1

    return return_list


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        return self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        # Note that this class keeps _subordinates in order, so we don't need to
        # sort it.
        return_list = []
        return_list.extend(self._subordinates)
        return return_list

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        ans = []
        subs = self.get_direct_subordinates()
        if not subs:
            return []

        else:
            for sub in subs:
                ans = merge(ans, [sub])
                ans = merge(ans, sub.get_all_subordinates())

        return ans

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        top_employee = self.get_superior()

        if top_employee is None:
            top_employee = self
        else:
            # This loops until we reach the top of the hierarchy.
            while top_employee._superior is not None:
                top_employee = top_employee._superior

        return top_employee

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        if self.get_superior() is not None:
            self.get_superior().remove_subordinate_id(self.eid)

        self._superior = superior

        if superior is not None:
            superior.add_subordinate(self)

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """
        count = 0

        for subordinate in self._subordinates:
            if subordinate.eid == eid:
                self._subordinates.pop(count)
                return

            count += 1

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        # NOTE: This adds the subordinate such that the eid order of
        # self.subordinates is preserved.
        for i in range(len(self._subordinates)):
            subordinate_2 = self._subordinates[i]

            if subordinate_2.eid > subordinate.eid:
                self._subordinates.insert(i, subordinate)
                return

        self._subordinates.append(subordinate)

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        if self.eid == eid:
            return self

        for subordinate in self.get_direct_subordinates():
            if subordinate.eid == eid:
                return subordinate

            employee = subordinate.get_employee(eid)

            if employee is not None:
                return employee

        return None

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        ans = []

        if self.salary > amount:
            ans.append(self)

        if not self.get_direct_subordinates():
            return ans

        for sub in self.get_direct_subordinates():
            ans = merge(ans, sub.get_employees_paid_more_than(amount))

        return ans

    def get_higher_paid_employees(self) -> List[Employee]:
        """Get all employees of the organization that have a salary higher than
        this employee's salary.

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than = e2.get_higher_paid_employees()
        >>> len(more_than) == 1
        True
        >>> more_than[0].name
        'Bigg Boss'
        """
        return self.get_organization_head() \
            .get_employees_paid_more_than(self.salary)

    def get_closest_common_superior(self, eid: int) -> Employee:
        """Get the common superior to this employee and the employee with
        the given id. If one of the employees is a direct or indirect
        subordinate of the other, the superior employee is the closest common
        superior.

        Precondition: <eid> exists in the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e3)
        >>> e2.become_subordinate(e3)
        >>> superior = e1.get_closest_common_superior(3)
        >>> superior.eid
        3
        """
        if self.eid == eid or self.get_employee(eid) is not None:
            return self

        # The line commented out below cannot happen if eid exists in the
        # organization:
        # if self._superior is None:

        return self.get_superior().get_closest_common_superior(eid)

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        if isinstance(self, Leader):
            return self.get_department_name()

        superior = self.get_superior()

        while superior is not None:
            if isinstance(superior, Leader):
                return superior.get_department_name()

            superior = superior.get_superior()

        return ""

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        return_string = self.position
        superior = self.get_superior()

        while superior is not None:
            if isinstance(superior, Leader):
                return_string += ', ' + superior.get_department_name()

            superior = superior.get_superior()

        return return_string

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Leader]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        if isinstance(self, Leader):
            return self

        superior = self.get_superior()

        while superior is not None:
            if isinstance(superior, Leader):
                return superior

            superior = superior.get_superior()

        return None

    def change_department_leader(self) -> Employee:
        """Changes the leader of this organization's department to this
        employee. The old leader becomes a direct subordinate of this employee.
        If the old leader was a subordinate of another employee, they get
        swapped out for this employee. This employee is returned.

        If this employee is the leader of its own department, nothing happens.

        >>> e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
        >>> e2 = Employee(3, "Sandra", "Secretary", 20000, 30)
        >>> e3 = Employee(3, "Sofia", "Manager", 25000, 30)
        >>> e4 = Employee(4, "Senya", "Grunt", 5000, 30)
        >>> e5 = Employee(5, "Sylvia", "Grunt", 5000, 30)
        >>> e2.become_subordinate(e1)
        >>> e3.become_subordinate(e1)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e3)
        >>> new_head = e3.change_department_leader()
        >>> new_head.name
        'Sofia'
        >>> subordinates = new_head.get_direct_subordinates()
        >>> len(subordinates)
        3
        """
        old_leader = self.get_department_leader()

        if old_leader is None or old_leader == self:
            # nothing happens because there is no department or because self
            # is already the leader
            return self.get_organization_head()

        old_lead_superior = old_leader.get_superior()
        new_leader = self.become_leader(old_leader.get_department_name())
        new_employee = old_leader.become_employee()

        if old_lead_superior:
            old_lead_superior.remove_subordinate_id(new_employee.eid)
        new_employee.remove_subordinate_id(self.eid)
        new_leader.become_subordinate(old_lead_superior)
        new_employee.become_subordinate(new_leader)

        return new_leader.get_organization_head()

    def become_leader(self, department_name: str) -> Leader:
        """ Creates a Leader version of this employee and replaces this employee
        with the leader version in the organization hierarchy. Returns the
        newly constructed Leader object.
        """
        leader = Leader(self.eid, self.name, self.position, self.salary,
                        self.rating, department_name)
        superior = self.get_superior()

        if superior is not None:
            superior.remove_subordinate_id(self.eid)
            leader.become_subordinate(superior)

        # This makes a copy of the subordinates list.
        subordinates = []

        for subordinate in self.get_direct_subordinates():
            subordinates.append(subordinate)

        for subordinate in subordinates:
            subordinate.become_subordinate(leader)

        return leader

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        highest_rating = -1
        employee = None

        for subordinate in self.get_direct_subordinates():
            # note that since subs are returned by increasing eid, ties
            # are broken by lower eid
            if subordinate.rating > highest_rating:
                highest_rating = subordinate.rating
                employee = subordinate

        return employee

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        old_superior = self.get_superior()
        super_superior = old_superior.get_superior()
        old_superior.remove_subordinate_id(self.eid)

        if isinstance(self, Leader):
            # Turns the past superior being swapped into a leader.
            new_superior = Leader(old_superior.eid, old_superior.name,
                                  self.position, self.salary,
                                  old_superior.rating,
                                  self.get_department_name())
        else:
            # Turns the past superior being swapped into an employee.
            new_superior = Employee(old_superior.eid, old_superior.name,
                                    self.position, self.salary,
                                    old_superior.rating)

        if isinstance(old_superior, Leader):
            # Turns the past superior being swapped into a leader.
            new_self = Leader(self.eid, self.name,
                              old_superior.position, old_superior.salary,
                              self.rating,
                              old_superior.get_department_name())
        else:
            # Turns the past superior being swapped into an employee.
            new_self = Employee(self.eid, self.name,
                                old_superior.position, old_superior.salary,
                                self.rating)

        # This creates a copy of the subordinate lists.
        old_superior_subordinates = []
        old_self_subordinates = []

        for subordinate in old_superior.get_direct_subordinates():
            old_superior_subordinates.append(subordinate)

        for subordinate in self.get_direct_subordinates():
            old_self_subordinates.append(subordinate)

        # This swaps the subordinates.
        for subordinate in old_superior_subordinates:
            subordinate.become_subordinate(new_self)

        for subordinate in old_self_subordinates:
            subordinate.become_subordinate(new_superior)

        if super_superior is not None:
            # This gives the swapped employee a new superior.
            super_superior.remove_subordinate_id(old_superior.eid)
            new_self.become_subordinate(super_superior)

        new_superior.become_subordinate(new_self)
        return new_self

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """Set the employees with IDs in ids as subordinates of
        self. Returns the new organization head.

        If those employees have subordinates, the superior of those subordinates
        becomes the employee's original superior.

        If the head of an organization is taken as a subordinate, then the
        highest-rated direct subordinate of the head (i.e. the one with the
        largest ‘rating’ value: if multiple subordinates have the same
        rating, then the lowest eid is used) becomes the new head.

        Pre-condition: self.eid is not in ids.
        """
        head = self.get_organization_head()

        for eid in ids:
            # This gets the employee to be moved/obtained.
            employee = head.get_employee(eid)

            if employee is None:
                continue

            old_superior = employee.get_superior()

            if old_superior is None:
                # The employee being moved is the organization head. A new head
                # needs to be found. Chosen by rating.
                highest_rated = head.get_highest_rated_subordinate()

                new_subs = head.get_direct_subordinates()
                new_subs.pop(new_subs.index(highest_rated))
                for sub in new_subs:
                    # subs of employee being moved (which in this case is head)
                    # are added to new head: highest_rated
                    # note: highest_rated is not added as a sub of itself
                    sub.become_subordinate(highest_rated)

                # Highest rating becomes head of organization
                highest_rated.become_subordinate(None)
            else:
                # employee being moved is not org. head

                for subordinate in employee.get_direct_subordinates():
                    # subs of employee become subs of superior of employee
                    subordinate.become_subordinate(old_superior)

            employee.become_subordinate(self)
            # The head of the organization is saved, in order to be returned
            head = self.get_organization_head()

        return head


def _get_average_salary_helper(employee: Employee,
                               position: Optional[str] = None) -> list:
    """A helper method for get_average_salary. Returns a list lst in which
    lst[0] = total salary of the employee and its subordinates. lst[1]
    = total employees (including this one).
    """
    total_salary = 0.0
    total_employees = 0

    # This adds this employee to the statistics.
    if position is None or employee.position == position:
        total_salary += employee.salary
        total_employees += 1

    subordinates = employee.get_all_subordinates()

    # This adds the subordinates to the statistics.
    for subordinate in subordinates:
        if position is None or subordinate.position == position:
            total_salary += subordinate.salary
            total_employees += 1

    return [total_salary, total_employees]


def _fire_lowest_rated_employee_helper(head: Employee) -> Employee:
    """Helper method for firing the employee with the lowest rating.
    This method specifically gets the employee to be fired.

    Precondition: head is not None.
    """
    lowest_rating = head.rating
    employee = head

    for subordinate in head.get_all_subordinates():
        if subordinate.rating < lowest_rating:
            lowest_rating = subordinate.rating
            employee = subordinate

    return employee


def _get_employees_under_rating(head: Employee, rating: int) \
        -> List[Employee]:
    """A helper method which returns all employees as a subordinate of
    head (including head) which have a rating below the passed in value.
    """
    ans = []
    ans2 = []

    # This appends head.
    if head.rating < rating:
        ans.append(head)

    if not head.get_direct_subordinates():
        return ans

    # This appends all the other subordinates.
    for sub in head.get_all_subordinates():
        if sub.rating < rating:
            ans2.append(sub)

    ans = merge(ans, ans2)
    return ans


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        head = self.get_head()
        if head is None:
            return None
        if head.eid == eid:
            return head
        return head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        head = self.get_head()
        if superior_id is None:
            # This checks if no id was given. No ID means this employee becomes
            # the head of the organization.
            if head is not None:
                # This organization is non-empty and the old head needs to
                # become a subordinate of the new employee.
                head.become_subordinate(employee)
            self.set_head(employee)
            return

        if head.eid == superior_id:
            employee.become_subordinate(head)
            return

        superior = head.get_employee(superior_id)
        employee.become_subordinate(superior)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0.0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        if self.get_head() is None:
            return 0.0

        # This uses a helper method to get the total salary and the number of
        # employees as lst[0] and lst[1].
        lst = _get_average_salary_helper(self.get_head(), position)

        if lst[1] == 0:
            return 0.0
        else:
            return lst[0] / lst[1]

    def get_next_free_id(self) -> int:
        """Gets the next unused id. The returned id > 0.
        """
        taken_ids = self._get_ids_of_subordinates(self.get_head())
        count = 1

        while True:
            if count not in taken_ids:
                return count

            count += 1

    def _get_ids_of_subordinates(self, employee: Employee) -> List[int]:
        """Returns all used ids of all subordinates to this employee in a list.
        Includes the id of this employee.
        """
        subordinate_ids = [employee.eid]

        for subordinate in employee.get_direct_subordinates():
            subordinate_ids = merge(subordinate_ids,
                                    self._get_ids_of_subordinates(subordinate))

        return subordinate_ids

    def get_employees_with_position(self, position: str) -> List[Employee]:
        """Returns all subordinates, as well as this employee, in a list
        such that the employees in the list hold the passed in position.
        The employees in the returned list are sorted by id.
        """
        lst = []

        # This adds subordinates to lst.
        for subordinate in self.get_head().get_all_subordinates():
            if subordinate.position == position:
                lst.append(subordinate)

        # This adds self to lst.
        if self.get_head().position == position:
            lst = merge(lst, [self.get_head()])

        return lst

    def get_head(self) -> Optional[Employee]:
        """Returns the head of the organization, or None if the organization
        is empty.
        """
        return self._head

    # === TASK 3 ===
    def set_head(self, head: Employee) -> None:
        """Sets the head of the organization to a new head.
        """
        self._head = head

    # === TASK 4 ===
    def fire_employee(self, eid: int) -> None:
        """Fire the employee with ID eid from this organization.

        Pre-condition: there is an employee with the eid <eid> in
        this organization.
        """
        employee = self.get_employee(eid)
        superior = employee.get_superior()

        if superior is None:
            # This runs only if the employee being fired is the organization
            # head.
            superior = employee.get_highest_rated_subordinate()
            superior.become_subordinate(None)

            for sub in employee.get_direct_subordinates():
                sub.become_subordinate(superior)

            self._head = superior
        else:
            employee.get_superior().remove_subordinate_id(eid)

            # This reassigns the subordinates.
            for subordinate in employee.get_direct_subordinates():
                subordinate.become_subordinate(superior)

    def fire_lowest_rated_employee(self) -> None:
        """Fires the employee with the lowest rating.

        Precondition: head is not None.
        """
        employee = _fire_lowest_rated_employee_helper(self.get_head())
        self.fire_employee(employee.eid)

    def fire_under_rating(self, rating: int) -> None:
        """Fire all employees with a rating below rating.

        Employees should be fired in order of increasing rating: the lowest
        rated employees are to be removed first. Breaks ties in order of eid.
        """
        employees = _get_employees_under_rating(self.get_head(), rating)

        for employee in employees:
            # changed to employee.eid from employee
            self.fire_employee(employee.eid)

    def _get_employees_under_rating(self, head: Employee, rating: int) -> \
            [Employee]:
        """
        """
        employee_dict = {}
        employee_ids = []

        if head.rating > rating:
            employee_ids.append(head.eid)
            employee_dict[head.eid] = head

        for subordinate in head.get_direct_subordinates():
            sub_employees = self._get_employees_under_rating(subordinate,
                                                             rating)
            sub_ids = []

            for employee in sub_employees:
                employee_dict[employee.eid] = employee
                sub_ids.append(employee.eid)

            employee_ids = merge(employee_ids, sub_ids)

        return_list = []

        for eid in employee_ids:
            return_list.append(employee_dict[eid])

        return return_list

    def promote_employee(self, eid: int) -> None:
        """Promote the employee with the eid <eid> in self.current_organization
        until they have a superior with a higher rating than them or until they
        are the head of the organization.

        Precondition: There is an employee in self.current_organization with
        eid <eid>.
        """
        employee = self.get_employee(eid)
        superior = employee.get_superior()

        # This continuously swaps up our employee until we no longer need to.
        while superior is not None and superior.rating <= employee.rating:
            employee = employee.swap_up()
            superior = employee.get_superior()

        if superior is None:
            self._head = employee


# === TASK 2: Leader ===
# Complete the Leader class and its methods according to their docstrings.
#       You will also need to revisit Organization and Employee to implement
#       additional methods.
#       Go through client_code.py to find additional methods that you must
#       implement.
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.
class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        super().__init__(eid, name, position, salary, rating)
        self._department_name = department

    def get_department_name(self) -> str:
        """Returns the name of the leader's department as a string.
        """
        return self._department_name

    def get_department_employees(self) -> List[Employee]:
        """Returns a list of all employees who are in this leader's department.
        The employees in the list are in order of eid.
        """
        # From piazza: If you call ceo.get_department_employees() (assuming
        # the ceo is the leader of the whole company/head of the
        # organization), you would get back a list containing every single
        # employee/leader (including the ceo themselves) in sorted order by eid.
        return merge(self.get_all_subordinates(), [self])

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        return_string = self.position + ', ' + self.get_department_name()
        superior = self.get_superior()

        while superior is not None:
            if isinstance(superior, Leader):
                return_string += ', ' + superior.get_department_name()

            superior = superior.get_superior()

        return return_string

    # === TASK 3 ===
    def become_leader(self, department_name: str) -> Leader:
        """Overrides Employee.become_leader. Changes this leader's
        department name.
        """
        self._department_name = department_name
        return self

    def become_employee(self) -> Employee:
        """Creates an Employee version of this leader and replaces this leader
        with the Employee version in the organization hierarchy. Returns the
        newly constructed Employee object.
        """
        employee = Employee(self.eid, self.name, self.position, self.salary,
                            self.rating)
        superior = self.get_superior()

        if superior is not None:
            superior.remove_subordinate_id(self.eid)
            employee.become_subordinate(superior)

        # This makes a copy of the subordinates list.
        subordinates = []

        for subordinate in self.get_direct_subordinates():
            subordinates.append(subordinate)

        for subordinate in subordinates:
            subordinate.become_subordinate(employee)

        return employee

    # === TASK 4 ===


# === TASK 5 ===
class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    head = organization.get_head()

    if head is None:
        # empty Organization
        return None
    if head.get_department_name() == '':
        # no departments in organization
        return None
    return _get_dept_tree(head)


def _get_dept_tree(e: Employee) -> Optional[DepartmentSalaryTree]:
    """ A helper method which returns a DepartmentSalaryTree from <e> when
    <e> is a leader or None otherwise.
    """
    if isinstance(e, Leader):
        return DepartmentSalaryTree(e.get_department_name(), _get_dept_avg(e),
                                    _dept_tree_helper(e))
    else:
        return None


def _dept_tree_helper(e: Employee) -> [DepartmentSalaryTree]:
    """ A helper method for _get_dept_tree() that returns a list of DSTs
    from <e>.
    """
    subtrees = []
    for sub in e.get_direct_subordinates():
        # if <sub> is a leader, that sub has their own department
        if isinstance(sub, Leader):
            tree = _get_dept_tree(sub)
            if tree is not None:
                subtrees.append(tree)
        else:
            # otherwise, there still may be leaders as non-direct subordinates
            # of <sub>, so we have to add them
            subtrees += _dept_tree_helper(sub)
    return subtrees


def _get_dept_avg(e: Leader) -> float:
    """This returns the average salary of the leader's department.
     """
    lst = e.get_department_employees()
    lst2 = []

    for employee in lst:
        if employee.get_department_name() == e.get_department_name():
            lst2.append(employee)

    capital = 0

    for emp in lst2:
        capital += emp.salary

    return capital / len(lst2)


# === TASK 6 ===
def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    org = Organization()

    # We store our employees here.
    employees = []

    # The index in the employees list where the leader is located.
    leader_index = -1

    # A counter for our loop.
    count = 0

    # This loops through every line to generate a new employee.
    for line in file.readlines():
        data = line.split(",")

        # This generates the employee.
        if len(data) == 7:
            employee = Leader(int(data[0]), data[1], data[2],
                              float(data[3]), int(data[4]), data[6].rstrip())
        else:
            employee = Employee(int(data[0]), data[1], data[2],
                                float(data[3]), int(data[4]))

        if data[5] == '':
            # This is a leader!
            employees.append((employee, -1))
            leader_index = count
        else:
            employees.append((employee, int(data[5])))

        count += 1

    # This sets the organization head. Note that the head is not always on the
    # first line of the file.
    org.set_head(employees[leader_index][0])

    while employees:
        count = 0

        for t in employees:
            if t[1] == -1:
                continue

            if org.get_employee(t[1]) is not None:
                org.add_employee(t[0], t[1])
                employees.pop(count)

            count += 1

    return org


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    # python_ta.check_all(config={
    #     'allowed-import-modules': ['python_ta', 'doctest', 'typing',
    #                                '__future__'],
    #     'max-args': 7})
