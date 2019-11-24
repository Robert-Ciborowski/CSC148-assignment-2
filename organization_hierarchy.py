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


# === TASK 1 ===
# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    # note, we are merging employees, so assume no duplicates (no equality)
    lst1_copy = []
    for e in lst1:
        lst1_copy.append(e)
    lst2_copy = []
    for e in lst2:
        lst2_copy.append(e)
    ans = []
    while lst1_copy != []:
        if lst2_copy == []:
            ans.append(lst1_copy.pop(0))
        while lst2_copy != []:
            if lst1_copy == []:
                ans.append(lst2_copy.pop(0))
                continue
            if lst1_copy[0] < lst2_copy[0]:
                ans.append(lst1_copy.pop(0))
            else:
                ans.append(lst2_copy.pop(0))
    while lst2_copy != []:
        ans.append(lst2_copy.pop(0))
    return ans


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
        if self._subordinates == []:
            return []
        subs = []
        subs.append(self._subordinates[0])
        for sub in self._subordinates[1:]:
            if sub < subs[0]:
                subs.insert(0, sub)
            else:
                for i in range(len(subs)):
                    if i == len(subs) - 1:
                        subs.append(sub)
                        continue
                    if sub < subs[i + 1]:
                        subs.insert(i, sub)
        return subs

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
        if self._subordinates == []:
            return []
        else:
            for sub in self._subordinates:
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
        if self._superior is None:
            return self
        return self._superior.get_organization_head()

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
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
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
        for sub in self.get_direct_subordinates():
            if sub.eid == eid:
                self._subordinates.pop(self._subordinates.index(sub))

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
        if self._subordinates == []:
            return None
        for sub in self._subordinates:
            e = sub.get_employee(eid)
            if e is not None:
                return e
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
        if self._subordinates == []:
            return ans
        for sub in self._subordinates:
            ans = merge(ans, sub.get_employees_paid_more_than(amount))
        return ans

    # Go through client_code.py for additional methods you need to
    #       implement in Task 1. Write their headers and bodies below.

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
        """ Docstring """
        # test
        self_sups = self._get_sups()
        other_sups = self.get_organization_head().get_employee(eid)._get_sups()
        if len(self_sups) == 1:
            return self_sups[0]
        if len(other_sups) == 1:
            return other_sups[0]
        i = 1
        while self_sups[-i] == other_sups[-i]:
            i += 1
        return self_sups[-i + 1]

    def _get_sups(self) -> List:
        """ Docstring """
        val = [self]
        current = self.get_superior()
        while current is not None:
            val.append(current)
            current = current.get_superior()
        return val

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
            return self._department_name
        elif self.get_superior() is not None:
            return self.get_superior().get_department_name()
        else:
            return ''

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
        sups = self._get_sups()
        positions = [self.position]
        for p in sups:
            d = p.get_department_name()
            # note: this is okay because department names are unique
            if d and d not in positions:
                positions.append(d)
        string = ''
        for s in positions:
            if s != positions[-1]:
                string += s + ', '
            else:
                string += s
        return string

    # Go through client_code.py for additional methods you need to
    #       implement in Task 2.

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
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
        curr = self
        while (not isinstance(curr, Leader)) and (curr is not None):
            curr = self.get_superior()
        return curr

    def change_department_leader(self) -> Optional[Leader]:
        """ Docstring """
        # TODO: test
        # I am going to mutate the current dept leader, hereafter called prev
        # leader (p in code), to have the attributes of self,
        # and create a new Employee
        # with the attributes of prev leader
        # this is to avoid trying to cast self into a new type (Leader)
        # note: self will still refer to an Employee, not a leader
        # but this is okay because client code updates current displayed to
        # match the old self.eid (so it will find the mutated Leader)

        # is it okay to keep salary, position, rating, the same?
        if isinstance(self, Leader):
            return None
        if self.get_department_name() == '':
            return None

        p = self.get_department_leader()
        new_sub = Employee(p.eid, p.name, p.position, p.salary, p.rating)
        new_sub.become_subordinate(self)
        new_sub._add_subs(p.get_direct_subordinates())
        # I think this is unnecessary because become_sub should remove current
        # superior
        # p._remove_subs()
        p._add_subs(self.get_direct_subordinates())
        p.eid, p.position, p.name, p.salary, p.rating = self.eid, self.name, \
                                                        self.position, self.salary, self.rating
        # note: this doesn't remove the sup as a sup of self, but we should
        # lose reference to self after this, so it should be okay

        # given that my setup didn't require me to return anything, I may have
        # implemented this wrong
        self.get_superior().remove_subordinate_id(self.eid)
        return p

    def _add_subs(self, subs: [Employee]) -> None:
        """ Docstring """
        for sub in subs:
            sub.become_subordinate(self)

    # def _remove_subs(self) -> None:
    #     for sub in self.get_direct_subordinates():
    #         self.remove_subordinate_id(sub.eid)

    def become_leader(self, department_name: str) -> Leader:
        """ Docstring """
        # TODO: test
        # can clean up by moving shared code with take over to helper
        new_lead = Leader(self.eid, self.name, self.position, self.salary,
                          self.rating, department_name)
        p = self.get_department_leader()
        new_sub = Employee(p.eid, p.name, p.position, p.salary, p.rating)
        new_sub.become_subordinate(self)
        new_sub._add_subs(p.get_direct_subordinates())
        new_lead._add_subs(self.get_direct_subordinates())
        self.get_superior().remove_subordinate_id(self.eid)
        return new_lead

    # Go through client_code.py for additional methods you need to
    #       implement in Task 3.

    def become_leader(self, department_name: str) -> Leader:
        """Creates a Leader version of this employee and replaces this employee
        with the leader version in the organization hierarchy. Returns the
        newly constructed Leader object.
        """
        leader = Leader(self.eid, self.name, self.position, self.salary,
                        self.rating, department_name)

        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
            leader.become_subordinate(self._superior)

        # This makes a copy of the subordinates list.
        subordinates = []

        for subordinate in self._subordinates:
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
        highest_sub = self.get_direct_subordinates()[0]
        highest_rating = highest_sub.rating
        for sub in self.get_direct_subordinates():
            if sub.rating > highest_rating:
                highest_rating = sub.rating
                highest_sub = sub
        return highest_sub

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
        # TODO: test
        sup = self.get_superior()
        if isinstance(sup, Leader):
            new = Leader(self.eid, self.name, sup.position, sup.salary,
                         self.rating, sup.get_department_name())
            sup.remove_subordinate_id(self.eid)
            new.become_subordinate(sup.get_superior())
            new_sub = Employee(sup.eid, sup.name, self.position, self.salary,
                               sup.rating)
            sup_sup = sup.get_superior()
            if sup_sup is not None:
                sup_sup.remove_subordinate_id(sup.eid)
                sup_sup.add_subordinate(new_sub)
            new_sub.become_subordinate(self)
            new._add_subs(self.get_direct_subordinates())
            return new
        else:
            self.become_subordinate(sup.get_superior())
            sup.become_subordinate(sup)
            self.position, self.salary, sup.position, sup.salary = \
                sup.position, sup.salary, self.position, self.salary
            return self

    # Go through client_code.py for additional methods you need to
    #       implement in Task 4.

    def obtain_subordinates(self, ids: [int]) -> Leader:
        """ Docstring """
        # I don't know why this returns anything, why set head is called in
        # client code
        # TODO: needs lots of testing
        ids2 = []
        for eid in ids:
            ids2.append(eid)
        head = self.get_organization_head()
        if head.eid in ids2:
            runners_up = head.get_direct_subordinates()
            winner = runners_up[0]
            max_rating = winner.rating
            invalids = []
            for r in runners_up:
                # I am going to assume there will be a valid runner left
                if r.eid in ids2:
                    while r.eid in ids2:
                        invalids.append(runners_up.pop(runners_up.index(r)))
                elif r.rating > max_rating:
                    max_rating = r.rating
                    winner = r
            winner_subs = winner.get_direct_subordinates()
            winner.swap_up()
            winner._add_subs(winner_subs)
            head._add_subs(invalids)

        head = self.get_organization_head()
        for eid in ids2:
            emp = head.get_employee(eid)
            for sub in emp.get_direct_subordinates():
                # what if no valid sup?
                valid_sup = emp.get_superior()
                while valid_sup.eid in ids2:
                    valid_sup = valid_sup.get_superior()
                sub.become_subordinate(valid_sup)
            emp.become_subordinate(self)
        return self.get_department_leader()


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
        if head is None:
            self._head = None
        else:
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
        h = self._head
        if h is None:
            return None
        else:
            return h.get_employee(eid)

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
        # what if org. is non-empty and there is no superior id
        # what if super. id doesn't exist

        # currently adds current head as sub of emp
        # if super. id is None
        # (as per create dept hier. doctest)

        # currently does nothing if superior id not in organization
        if superior_id is None:
            old_head = self.get_head()
            self._head = employee
            if old_head is not None:
                self.get_head().add_subordinate(old_head)
        else:
            x = self.get_employee(superior_id)
            if x is not None:
                employee.become_subordinate(x)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        # why does doctest want 0 instead of 0.0
        if self.get_head() is None:
            return 0
        elif position is None:
            head = self.get_head()
            lst = head.get_all_subordinates()
            num_employees = 1 + len(lst)
            total_salary = head.salary
            for emp in lst:
                total_salary += emp.salary
            return total_salary / num_employees
        else:
            num_employees = 0
            total_salary = 0
            head = self.get_head()
            if head.position == position:
                num_employees = 1
                total_salary = head.salary
            for emp in head.get_all_subordinates():
                if emp.position == position:
                    num_employees += 1
                    total_salary += emp.salary

            if num_employees == 0:
                return 0.0
            return total_salary / num_employees

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1.

    def get_head(self) -> Optional[Employee]:
        """ Docstring """

        return self._head

    def get_next_free_id(self) -> int:
        """ Docstring """
        h = self.get_head()
        if h is None:
            return 1
        else:
            prev_id = h.eid
            for emp in h.get_all_subordinates():
                if emp.eid > prev_id:
                    prev_id = emp.eid
            return prev_id + 1

    def get_employees_with_position(self, position: str) -> [Employee]:
        """ Docstring """
        h = self.get_head()
        if h is None:
            return []
        all_emps = merge([h], h.get_all_subordinates())
        emps_with_pos = []
        for emp in all_emps:
            if emp.position == position:
                emps_with_pos.append(emp)
        return emps_with_pos

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

    # === TASK 3 ===
    # Go through client_code.py for the methods you need to implement in
    #       Task 3.

    def set_head(self, organization_head: Leader) -> None:
        """ Docstring """
        self._head = organization_head

    # === TASK 4 ===
    # Go through client_code.py for the methods you need to implement in
    #       Task 4.

    def fire_employee(self, eid: int) -> None:
        """ Docstring """
        emp = self.get_employee(eid)
        if not emp == self.get_head():
            sup = emp.get_superior()
            for e in emp.get_direct_subordinates():
                e.become_subordinate(sup)
            sup.remove_subordinate_id(eid)
        else:
            subs = emp.get_direct_subordinates()
            if subs != []:
                best_sub = subs[0]
                if len(subs) > 1:
                    highest_rating = best_sub.rating
                    for sub in subs:
                        if sub.rating > highest_rating:
                            highest_rating = sub.rating
                            best_sub = sub
                    subs.pop(subs.index(best_sub))
                    for sub in subs:
                        sub.become_subordinate(best_sub)
                    self.set_head(best_sub)
                else:
                    self.set_head(best_sub)

    def fire_lowest_rated_employee(self) -> None:
        """ Docstring """
        if self.get_head() is None:
            return
        head = self.get_head()
        eid = head.eid
        lowest_rating = head.rating
        for emp in head.get_all_subordinates():
            if emp.rating < lowest_rating:
                lowest_rating = emp.rating
                eid = emp.eid
            elif emp.rating == lowest_rating:
                if emp.eid < eid:
                    lowest_rating = emp.rating
                    eid = emp.eid
        self.fire_employee(eid)

    def fire_under_rating(self, rating: int) -> None:
        """ Docstring """
        head = self.get_head()
        lst = head.get_all_subordinates() + [head]
        r = 0
        while r != rating:
            for emp in lst:
                if emp.rating < r:
                    self.fire_employee(emp.eid)
            r += 1

    def promote_employee(self, eid: int) -> None:
        """ Docstring """
        emp = self.get_employee(eid)
        pos = emp.position
        salary = emp.salary
        if emp.get_superior() is None:
            return
        while emp.get_superior() is not None:
            sup = emp.get_superior()
            while sup.rating <= emp.rating:
                emp.position = sup.position
                emp.salary = sup.salary
                sup.position = pos
                sup.salary = salary
                emp.swap_up()


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
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    # Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    #       There may also be Employee methods that you'll need to override.

    def get_department_employees(self) -> [Employee]:
        """ Docstring """

        # tested

        # not really recursive, could be made better
        ans = [self]
        for sub in self._subordinates:
            if not isinstance(sub, Leader):
                ans = merge(ans, [sub])
                subs = sub.get_all_subordinates()
                sub_subs = []
                for sub2 in subs:
                    if isinstance(sub2, Leader):
                        sub_subs.append(sub2)
                ans = merge(ans, sub_subs)
        return ans

    # === TASK 3 ===
    # Go through client_code.py for the methods you need to implement in
    #       Task 3. If there are no methods there, consider if you need to
    #       override any of the Task 3 Employee methods.

    def become_employee(self) -> Employee:
        """ Docstring """
        e = Employee(self.eid, self.name, self.position, self.salary,
                     self.rating)
        sup = self.get_superior()
        sup.remove_subordinate_id(self.eid)
        e.become_subordinate(sup)
        e._add_subs(self.get_direct_subordinates())
        return e

    def become_leader(self, department_name: str) -> Leader:
        """ Docstring """
        self._department_name = department_name
        return self


# === TASK 4 ===
# Go through client_code.py for the methods you need to implement in
#       Task 4. If there are no methods there, consider if you need to
#       override any of the Task 4 Employee methods.


# === TASK 5 ===
# Complete the create_department_salary_tree() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

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
        return None
    if head.get_department_name() == '':
        return None
    return _get_department(head)


def _get_department(e: Employee) -> DepartmentSalaryTree:
    """ Docstring """
    if _get_sub_leaders(e) == []:
        return DepartmentSalaryTree(e.get_department_name(), _get_dept_avg(e),
                                    [])
    lst = []
    for sub in _get_sub_leaders(e):
        lst.append(_get_department(sub))
    return DepartmentSalaryTree(e.get_department_name(), _get_dept_avg(e), lst)


def _get_dept_avg(e: Employee) -> None:
    """ Docstring """
    lst = e.get_department_employees()
    capital = 0
    for emp in lst:
        capital += emp.salary
    return capital / len(lst)


def _get_sub_leaders(e: Employee) -> List[Leader]:
    """ Docstring """
    ans = []
    subs = e.get_all_subordinates()
    for i in subs:
        if isinstance(i, Leader):
            ans.append(i)
    return ans


# === TASK 6 ===
# Complete the create_organization_from_file() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.


def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    org = Organization()
    for line in file.readlines():
        data = line.split(",")
        if data[5] == '':
            if len(data) == 7:
                org.set_head(Leader(data[0], data[1], data[2], data[3],
                                    data[4], data[6]))
            else:
                org.set_head(Employee(data[0], data[1], data[2], data[3],
                                      data[4]))
        else:
            if len(data) == 7:
                org.add_employee(Leader(data[0], data[1], data[2], data[3],
                                        data[4], data[6]), data[5])
            else:
                org.add_employee(Employee(data[0], data[1], data[2], data[3],
                                          data[4]), data[5])
    return org

    # Task 6: Complete the create_organization_from_file function.


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
