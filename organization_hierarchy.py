"""Assignment 2: Organization Hierarchy

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

Author: Anshul Agrawal
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    merged_list = []
    i, j = 0, 0
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            merged_list.append(lst1[i])
            i += 1
        else:
            merged_list.append(lst2[j])
            j += 1
    merged_list += lst1[i:] + lst2[j:]
    return merged_list


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

    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        >>> e.name
        'Emma Ployee'
        >>> e.salary
        10000
        >>> e.position
        'Worker'
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
        >>> e2 < e1
        False
        """
        return isinstance(other, Employee) and self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        return self._subordinates

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
        if not self._subordinates:
            return []
        else:
            subs = []
            for subordinate in self._subordinates:
                subs = merge(subs, [subordinate])
                subs = merge(subs, subordinate.get_all_subordinates())
            return subs

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
        else:
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
        if superior is not None:
            superior.add_subordinate(self)
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
        self._superior = superior

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
        for subordinate in self._subordinates:
            if subordinate.eid == eid:
                self._subordinates.remove(subordinate)
                return None
        return None

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
        self._subordinates = merge(self._subordinates, [subordinate])

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
        all_subordinates = self.get_all_subordinates()
        for subordinate in all_subordinates:
            if subordinate.eid == eid:
                return subordinate
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
        result = []
        if self.salary > amount:
            result.append(self)
        all_subordinates = self.get_all_subordinates()
        for subordinate in all_subordinates:
            if subordinate.salary > amount:
                result = merge(result, [subordinate])
        return result

    def _get_all_superiors(self) -> List[Employee]:
        """ Returns the list of all superiors starting with the closest
            upto the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> s = e1._get_all_superiors()
        >>> s[0].name
        'Sue Perior'
        >>> s[1].name
        'Bigg Boss'
        >>> e3._get_all_superiors()
        []
        """
        superiors = []
        if self.get_superior() is None:
            return superiors
        else:
            superiors.append(self.get_superior())
            superiors.extend(self.get_superior()._get_all_superiors())
            return superiors

    def get_higher_paid_employees(self) -> List[Employee]:
        """Return a list of all employees in the Organization that are paid more
        than self.current_employee.

        Employees must be returned with IDs in increasing order.
        """
        head = self.get_organization_head()
        return head.get_employees_paid_more_than(self.salary)

    def get_closest_common_superior(self, eid: int) -> Employee:
        """Return the closest common superior in the organization between
        self.current_employee and the employee with ID <eid>.

        Precondition: <eid> exists in the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e2)
        >>> e1.get_closest_common_superior(5).name
        'Sue Perior'
        >>> e1.get_closest_common_superior(4).name
        'Bigg Boss'
        >>> e1.get_closest_common_superior(2).name
        'Sue Perior'
        >>> e3.get_closest_common_superior(2).name
        'Bigg Boss'
        """
        employee_eid = self.get_organization_head().get_employee(eid)
        superiors1 = [self] + self._get_all_superiors()
        superiors2 = [employee_eid] + employee_eid._get_all_superiors()
        for sup in superiors1:
            if sup in superiors2:
                return sup
        return self.get_organization_head()

    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e3.become_subordinate(e1)
        >>> e3.get_department_name()
        'Department'
        """
        if self.get_superior() is None:
            return ''
        else:
            return self.get_superior().get_department_name()

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
        result = self.position
        departments = self._get_position_in_hierarchy_helper()
        if not departments:
            return result
        else:
            for department in departments:
                result = result + ', ' + department
            return result

    def _get_position_in_hierarchy_helper(self) -> List[str]:
        """ Returns a list containing the departments in hierarchy of the
            Employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1._get_position_in_hierarchy_helper()
        []
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1._get_position_in_hierarchy_helper()
        ['Department', 'Company']
        >>> e2._get_position_in_hierarchy_helper()
        ['Department', 'Company']
        >>> e3._get_position_in_hierarchy_helper()
        ['Company']
        """
        if self._superior is None:
            if isinstance(self, Leader):
                return [self.get_department_name()]
            else:
                return []
        else:
            result = []
            if isinstance(self, Leader):
                result.append(self.get_department_name())
            result.extend(self._superior._get_position_in_hierarchy_helper())
            return result

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
        if isinstance(self, Leader):
            return self
        else:
            if self.get_superior() is not None:
                return self.get_superior().get_department_leader()
            else:
                return None

    def change_department_leader(self) -> Employee:
        """
        Makes the employee the leader of their current department,
        becoming the superior of the current department leader.
        The employee keeps all of their subordinates, in addition
        to gaining the leader as a subordinate.

        If the employee is already a leader or does not belong to a
        department, nothing happens.

        Returns the head the organization.

        >>> e1 = Leader(1, "Emma Ployee", "Worker", 10000, 50, 'Marketing')
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e3)
        >>> e2.become_subordinate(e1)
        >>> e3.become_subordinate(e1)
        >>> e3.change_department_leader().name
        'Bigg Boss'
        >>> isinstance(e4.get_superior(), Leader)
        True
        >>> len(e4.get_superior().get_direct_subordinates())
        3
        >>> isinstance(e4.get_superior().get_direct_subordinates()[0], Employee)
        True
        >>> e2.get_superior().name
        'Emma Ployee'
        >>> e2.get_superior().get_superior().name
        'Bigg Boss'
        >>> e5.get_department_name()
        'Marketing'
        >>> e5.get_department_leader().name
        'Bigg Boss'
        >>> e5.get_organization_head().eid
        3
        >>> len(e5.get_organization_head().get_all_subordinates())
        4
        >>> len(e5.get_organization_head().get_direct_subordinates())
        3
        """
        if self.get_department_leader() is None:
            return self.get_organization_head()
        else:
            department_name = self.get_department_name()
            new_employee = self.get_department_leader().become_employee()
            new_leader = self.become_leader(department_name)
            new_leader.become_subordinate(new_employee.get_superior())
            new_employee.become_subordinate(new_leader)
            return new_leader.get_organization_head()

    def become_leader(self, department_name: str) -> Leader:
        """ Makes the Employee a leader with department <department_name>.
        If Employee is already a leader, its changes the department to
        <department_name>.
        Returns the new leader created.

        >>> e0 = Employee(10, "The Rock", "Star", 15000, 60)
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e0.become_subordinate(e2)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> len(e2.get_direct_subordinates())
        2
        >>> e2.become_leader('Marketing').get_department_name()
        'Marketing'
        >>> isinstance(e1.get_superior(), Leader)
        True
        >>> e1.get_superior().get_superior().name
        'Bigg Boss'
        >>> k = e1.get_superior().get_direct_subordinates()
        >>> len(k)
        2
        >>> k[0].eid
        1
        >>> k[1].eid
        10
        """
        leader = Leader(self.eid, self.name, self.position, self.salary,
                        self.rating, department_name)
        if self.get_superior() is not None:
            self.get_superior().remove_subordinate_id(self.eid)
        leader.become_subordinate(self.get_superior())
        subs = self.get_direct_subordinates()
        for _ in range(len(subs)):
            subs[0].become_subordinate(leader)
        self._superior = None
        return leader

    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        In case of a tie, the employee with the lowest eid is returned.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, 'department')
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, 'company')
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e1.become_subordinate(e5)
        >>> e2.become_subordinate(e5)
        >>> e4.become_subordinate(e5)
        >>> e5.get_highest_rated_subordinate().name
        'Emma Ployee'
        >>> e3.become_subordinate(e5)
        >>> e5.get_highest_rated_subordinate().name
        'Bigg Boss'
        """
        subs = self.get_direct_subordinates()
        highest = -1
        sample = Employee(1, 'a', 'a', 1, 1)
        highest_employee = sample
        for sub in subs:
            if sub.rating > highest:
                highest = sub.rating
                highest_employee = sub
            elif sub.rating == highest:
                if highest_employee.eid > sub.eid:
                    highest_employee = sub
            else:
                continue
        if highest_employee == sample:
            return None
        else:
            return highest_employee

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
        >>> new_e1.salary
        20000
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> new_e2.eid
        2
        >>> new_e2.position
        'Worker'
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        sup = self.get_superior()

        self.name, sup.name = sup.name, self.name
        self.eid, sup.eid = sup.eid, self.eid
        self.rating, sup.rating = sup.rating, self.rating

        return self.get_superior()

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """ Set the employees with IDs in ids as subordinates of this
        employee.

        If those employees have subordinates, the superior of those subordinates
        becomes the employee's original superior.

        Pre-condition: This employee's id is not in ids.

        >>> e1 = Leader(1, "Emma Ployee", "Worker", 10000, 50, 'Marketing')
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e3)
        >>> e2.become_subordinate(e1)
        >>> e3.become_subordinate(e1)
        >>> head = e2.obtain_subordinates([3, 5])
        >>> head.get_direct_subordinates()[1].name
        'Emma Watson'
        >>> head.get_direct_subordinates()[0].get_direct_subordinates()[0].name
        'Bigg Boss'
        >>> head.get_direct_subordinates()[0].get_direct_subordinates()[1].name
        'The Rock'
        """
        head = self.get_organization_head()
        for id_ in ids:
            employee = head.get_employee(id_)
            subs = employee.get_direct_subordinates()
            if employee == head:
                new_head = employee.get_highest_rated_subordinate()
                subs.remove(new_head)
                for _ in range(len(subs)):
                    subs[0].become_subordinate(new_head)
                new_head.become_subordinate(None)
                employee.become_subordinate(self)
                head = new_head
            else:
                for _ in range(len(subs)):
                    subs[0].become_subordinate(employee.get_superior())
                employee.become_subordinate(self)
        return head


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

    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o = Organization(e1)
        >>> o.get_head() is e1
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
        if self._head is None:
            return None
        else:
            return self._head.get_employee(eid)

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
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> o.add_employee(e3)
        >>> o.get_head() is e3
        True
        >>> len(o.get_head().get_direct_subordinates())
        1
        >>> o.get_head().get_direct_subordinates()[0].name
        'Sue Perior'
        >>> o.get_head().get_direct_subordinates()[0].get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        if self._head is None:
            self._head = employee
            return None
        elif superior_id is None or superior_id == 0:
            self.get_head().become_subordinate(employee)
            self.set_head(employee)
            return None
        else:
            all_subs = merge(self._head.get_all_subordinates(), [self._head])
            for superior in all_subs:
                if superior.eid == superior_id:
                    employee.become_subordinate(superior)
                    return None
            return None

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
        if self._head is None:
            return 0.0
        else:
            total = 0
            count = 0
            if self._head.position == position or position is None:
                total = self._head.salary
                count += 1
            all_subordinates = self._head.get_all_subordinates()
            for subordinate in all_subordinates:
                if position is None or subordinate.position == position:
                    total += subordinate.salary
                    count += 1
            if count == 0:
                return 0.0
            else:
                return total/count

    def get_head(self) -> None:
        """Return the employee who is the head of the organization.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        >>> e = Employee(1, 'Anshul', 'Programmer', 100000, 100)
        >>> o = Organization(e)
        >>> o.get_head() is e
        True
        """
        return self._head

    def get_next_free_id(self) -> int:
        """ Returns the next free id.
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(4, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> o = Organization(e3)
        >>> o.get_next_free_id()
        3
        """
        i = 1
        all_employees = merge([self._head], self._head.get_all_subordinates())
        while i <= len(all_employees) and all_employees[i-1].eid == i:
            i += 1
        return i

    def get_employees_with_position(self, position: str) -> List[Employee]:
        """Return a list of employees in the organization with the
        position named <position> in order of increasing eids.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e2)
        >>> o = Organization(e3)
        >>> l = o.get_employees_with_position('Manager')
        >>> len(l)
        2
        >>> l[0].name
        'Sue Perior'
        >>> l[1].name
        'Emma Watson'
        >>> m = o.get_employees_with_position('Worker')
        >>> len(m)
        2
        >>> m[0].name
        'Emma Ployee'
        >>> m[1].name
        'The Rock'
        """
        if self._head is None:
            return []
        else:
            result = []
            all_subs = merge(self._head.get_all_subordinates(), [self._head])
            for employee in all_subs:
                if employee.position == position:
                    result.append(employee)
            return result

    def set_head(self, organization_head: Optional[Employee]) -> None:
        """ Changes the organization head t0 <organization_head>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> o = Organization(e2)
        >>> o.get_head().eid
        2
        >>> o.set_head(e1)
        >>> o.get_head().eid
        1
        """
        self._head = organization_head

    def fire_employee(self, eid: int) -> None:
        """ Fire the employee with ID eid from this organisation.

        Pre-condition: there is an employee with the eid <eid> in
        this organisation.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e4.become_subordinate(e3)
        >>> e5.become_subordinate(e3)
        >>> e2.become_subordinate(e1)
        >>> e3.become_subordinate(e1)
        >>> o = Organization(e1)
        >>> o.fire_employee(3)
        >>> len(e1.get_direct_subordinates())
        3
        >>> o.fire_employee(1)
        >>> o.get_head() is e4
        True
        >>> len(o.get_head().get_direct_subordinates())
        2
        """
        employee_to_be_fired = self.get_employee(eid)
        if employee_to_be_fired is not self._head:
            subs = employee_to_be_fired.get_direct_subordinates()
            for _ in range(len(subs)):
                subs[0].become_subordinate(employee_to_be_fired.get_superior())
            employee_to_be_fired.get_superior().remove_subordinate_id(eid)
        else:
            new_head = self._head.get_highest_rated_subordinate()
            if new_head is None:
                self.set_head(new_head)
            else:
                subs = self._head.get_direct_subordinates()
                subs.remove(new_head)
                for _ in range(len(subs)):
                    subs[0].become_subordinate(new_head)
                new_head.become_subordinate(None)
                self.set_head(new_head)

    def fire_lowest_rated_employee(self) -> None:
        """ Fire the lowest rated employee in this organisation.

        If two employees have the same rating, the one with the lowest id
        is fired.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
        >>> e1.become_subordinate(e5)
        >>> e2.become_subordinate(e5)
        >>> e3.become_subordinate(e5)
        >>> e4.become_subordinate(e5)
        >>> o = Organization(e5)
        >>> o.fire_lowest_rated_employee()
        >>> o.get_head() is e3
        True
        >>> len(o.get_head().get_direct_subordinates())
        3
        >>> o.fire_lowest_rated_employee()
        >>> len(o.get_head().get_direct_subordinates())
        2
        >>> o.get_head().get_direct_subordinates()[0].name
        'Emma Ployee'
        >>> o.get_head().get_direct_subordinates()[1].name
        'Emma Watson'
        """
        if self.get_head() is None:
            return None
        subs = merge([self.get_head()], self.get_head().get_all_subordinates())
        lowest = 101
        lowest_employee = 0
        for sub in subs:
            if sub.rating < lowest:
                lowest = sub.rating
                lowest_employee = sub
        self.fire_employee(lowest_employee.eid)

    def fire_under_rating(self, rating: int) -> None:
        """ Fire all employees with a rating below rating.

        Employees should be fired in order of increasing rating: the lowest
        rated employees are to be removed first. Break ties in order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 60)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 20)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 10)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 50)
        >>> e5.become_subordinate(e3)
        >>> e4.become_subordinate(e3)
        >>> e3.become_subordinate(e2)
        >>> e2.become_subordinate(e1)
        >>> o = Organization(e1)
        >>> o.fire_under_rating(40)
        >>> len(o.get_head().get_all_subordinates())
        1
        >>> o.get_head().get_all_subordinates()[0].name
        'The Rock'
        """
        subs = merge([self.get_head()], self.get_head().get_all_subordinates())
        under = []
        for sub in subs:
            if sub.rating < rating:
                under.append(sub)

        n = len(under)
        for i in range(n):
            for j in range(n - i - 1):
                if under[j].rating > under[j+1].rating:
                    under[j], under[j+1] = under[j+1], under[j]

        for sub in under:
            self.fire_employee(sub.eid)

    def promote_employee(self, eid: int) -> None:
        """Promote the employee with the eid <eid> in organisation
        until they have a superior with a higher rating than them or until they
        are the head of the organization.

        Precondition: There is an employee in the organisation with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 60)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 20)
        >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 10)
        >>> e5 = Employee(5, "The Rock", "Worker", 15000, 50)
        >>> e5.become_subordinate(e4)
        >>> e4.become_subordinate(e3)
        >>> e3.become_subordinate(e2)
        >>> e2.become_subordinate(e1)
        >>> o = Organization(e1)
        >>> o.promote_employee(5)
        >>> o.get_head() is e1
        True
        >>> o.get_head().get_direct_subordinates()[0].name
        'The Rock'
        """
        employee = self.get_employee(eid)
        if employee.get_superior() is None:
            return None
        elif employee.rating < employee.get_superior().rating or \
           employee == self.get_head():
            return None
        else:
            employee.swap_up()
            return self.promote_employee(eid)


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

    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Sales")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Sales'
        """
        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    def get_department_name(self) -> str:
        """Returns the name of the department of this Leader.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.get_department_name()
        'Department'
        """
        return self._department_name

    def get_department_employees(self) -> List[Employee]:
        """ Returns a list of employees in this Leader's department
            (including the leader).

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> l = e3.get_department_employees()
        >>> len(l)
        3
        >>> l[0].name
        'Emma Ployee'
        >>> l[1].name
        'Sue Perior'
        >>> l[2].name
        'Bigg Boss'
        >>> m = e2.get_department_employees()
        >>> len(m)
        2
        >>> m[0].name
        'Emma Ployee'
        >>> m[1].name
        'Sue Perior'
        """
        return merge([self], self.get_all_subordinates())

    def become_employee(self) -> Employee:
        """ Makes the Leader an Employee.

        Returns the new Employee created.

        >>> e0 = Employee(10, "The Rock", "Star", 15000, 60)
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, 'Marketing')
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e0.become_subordinate(e2)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e2.become_employee().name
        'Sue Perior'
        >>> isinstance(e1.get_superior(), Employee)
        True
        >>> e1.get_superior().get_superior().name
        'Bigg Boss'
        >>> k = e1.get_superior().get_direct_subordinates()
        >>> len(k)
        2
        >>> k[0].eid
        1
        >>> k[1].eid
        10
        """
        employee = Employee(self.eid, self.name, self.position, self.salary, \
                            self.rating)
        if self.get_superior() is not None:
            self.get_superior().remove_subordinate_id(self.eid)
        employee.become_subordinate(self.get_superior())
        subs = self.get_direct_subordinates()
        for _ in range(len(subs)):
            subs[0].become_subordinate(employee)
        self._superior = None
        return employee

    def become_leader(self, department_name: str) -> Leader:
        """ Makes the Employee a leader with department <department_name>.
        If Employee is already a leader, its changes the department to
        <department_name>.
        Returns the new leader created.

        >>> l = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> l.become_leader('Marketing').name
        'Bigg Boss'
        >>> l.get_department_name()
        'Marketing'
        """
        self._department_name = department_name
        return self

    def change_department_leader(self) -> Employee:
        """
        Makes the employee the leader of their current department,
        becoming the superior of the current department leader.
        The employee keeps all of their subordinates, in addition
        to gaining the leader as a subordinate.

        If the employee is already a leader or does not belong to a
        department, nothing happens.

        Returns the head the organization.

        >>> a = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> l = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> l.become_subordinate(a)
        >>> o = Organization(a)
        >>> l.change_department_leader().name
        'Sue Perior'
        """
        return self.get_organization_head()


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
    >>> len(dst.subdepartments)
    1
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    head = organization.get_head()
    if head is None:
        return None
    flag = False
    for sub in merge(head.get_all_subordinates(), [head]):
        if isinstance(sub, Leader):
            flag = True
            break
    if flag:
        department_name = head.get_department_name()
        total, count = head.salary, 1
        for employee in _get_non_leader_employees(head):
            total += employee.salary
            count += 1
        average_salary = total / count
        dsts = []
        for employee in head.get_all_subordinates():
            if isinstance(employee, Leader):
                temp_o = Organization(employee)
                dsts.append(create_department_salary_tree(temp_o))
        return DepartmentSalaryTree(department_name, average_salary, dsts)
    else:
        return None


def _get_non_leader_employees(employee: Employee) -> List[Employee]:
    """ Return all the subordinates of this leader that are in the same
    department (not sub department employees).

    >>> e1 = Leader(1, "Emma Ployee", "Worker", 10000, 50, 'Marketing')
    >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, 'Sales')
    >>> e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
    >>> e5 = Employee(5, "The Rock", "Worker", 15000, 15)
    >>> e2.become_subordinate(e1)
    >>> e3.become_subordinate(e1)
    >>> e4.become_subordinate(e3)
    >>> e5.become_subordinate(e3)
    >>> len(_get_non_leader_employees(e1))
    1
    >>> _get_non_leader_employees(e1)[0].name
    'Sue Perior'
    >>> len(_get_non_leader_employees(e2))
    0
    >>> len(_get_non_leader_employees(e3))
    2
    >>> _get_non_leader_employees(e3)[0].name
    'Emma Watson'
    >>> _get_non_leader_employees(e3)[1].name
    'The Rock'
    """
    subs = employee.get_direct_subordinates()
    if not subs:
        return []
    else:
        employees = []
        for sub in subs:
            if not isinstance(sub, Leader):
                employees.append(sub)
                employees.extend(_get_non_leader_employees(sub))
        return employees


def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.
    # Use doctest if you have 'employees.txt'
    # >>> o = create_organization_from_file(open('employees.txt'))
    # >>> o.get_head().name
    # 'Alice'
    """
    o = Organization()
    all_lines = [details.strip('\n').split(',') for details in file]
    for line in all_lines:
        if line[5] == '':
            if len(line) == 6:
                e = Employee(int(line[0]),
                             line[1],
                             line[2],
                             int(line[3]),
                             int(line[4]))
            else:
                e = Leader(int(line[0]),
                           line[1],
                           line[2],
                           int(line[3]),
                           int(line[4]),
                           line[6])
            o.set_head(e)
            all_lines.remove(line)
            break

    for line in all_lines:
        if o.get_employee(int(line[5])) is None:
            all_lines.append(line)
        else:
            if len(line) == 6:
                e = Employee(int(line[0]),
                             line[1],
                             line[2],
                             int(line[3]),
                             int(line[4]))
            else:
                e = Leader(int(line[0]),
                           line[1],
                           line[2],
                           int(line[3]),
                           int(line[4]),
                           line[6])
            o.add_employee(e, int(line[5]))
    return o


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['python_ta', 'doctest', 'typing',
    #                                '__future__'],
    #     'max-args': 7})
