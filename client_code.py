"""Assignment 2: Client Code
You should NOT modify this code.

Read through the client code to identify the methods that you need to write.

You may assume any pre-conditions listed in the client code are also applicable
to the methods you must write in organization_hierarchy.py.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains client code that calls upon the classes specified in
organization_hierarchy.py.

Author: Anshul Agrawal
"""
from typing import Optional, Tuple, List
from organization_hierarchy import Employee, Leader, Organization, \
     DepartmentSalaryTree, create_department_salary_tree, \
     create_organization_from_file


class OrganizationSimulator:
    """OrganizationSimulator: a class that stores information about the current
    state of a simulated organization.

    === Public Attributes ===
    current_employee:
        The Employee currently beieng displayed in the simulation.
    current_subordinates:
        The list of subordinates currently being displayed in the simulation.
    displaying_direct:
        Whether the current_subordinates being displayed are only the direct
        subordinates of current_employee or not.
    current_organization:
        The Organization currently being displayed in the simulation.
    """
    current_employee: Optional[Employee]
    current_subordinates: List[Employee]
    displaying_direct: bool
    current_organization: Organization

    def __init__(self) -> None:
        """Initialize this OrganizationSimulator with an empty Organization.
        """
        self.current_organization = Organization()
        self.current_employee = None
        self.current_subordinates = []
        self.displaying_direct = True

    def display_employee(self, eid: int) -> None:
        """Update self.current_employee to be the employee with the ID <eid>.
        If no such employee exist, self.current_employee should be None.
        """
        self.current_employee = self.current_organization.get_employee(eid)

    def get_current_employee_details(self) -> Tuple[str, float, int, str, str]:
        """Return the self.current_employee's name, salary, position, and
        department.
        """
        if self.current_employee:
            return (self.current_employee.name, self.current_employee.salary,
                    self.current_employee.rating,
                    self.current_employee.position,
                    self.get_current_employee_department())

        return "", 0.0, 0, "", ""

    def get_current_superior(self) -> Optional[Employee]:
        """Return the superior of self.current_employee.

        Pre-condition: self.current_employee has a superior (i.e. they are not
        the head of the organization.)
        """
        if self.current_employee:
            return self.current_employee.get_superior()

        return None

    def create_employee(self, name: str, eid: int, salary: float, rating: int,
                        position: str, superior_id: int) -> None:
        """Create the Employee with the name <name>, ID <eid>, salary <salary>,
        position <position>, rating <rating>, and set their superior to be the
        employee with ID <superior_id>.

        If <superior_id> == 0, this employee is the new head of the
        organization.

        If <eid> is already in use or < 0, then pick the next free ID number as
        the ID.

        Pre-condition: <superior_id> == 0 or is an ID that appears in the
        organization.
        """
        # Find the next free id if eid is already taken or is < 1
        if eid < 1 or self.current_organization.get_employee(eid) is not None:
            eid = self.current_organization.get_next_free_id()

        # Create the employee
        new_employee = Employee(eid, name, position, salary, rating)

        # Add the employee to the organization
        if superior_id <= 0:
            self.current_organization.add_employee(new_employee)
        else:
            self.current_organization.add_employee(new_employee, superior_id)

        self.display_employee(eid)

    def find_employees_with_position(self, position: str) -> List[Employee]:
        """Return a list of employees in self.current_organization with the
        position named <position> in order of increasing eids.
        """
        return self.current_organization.get_employees_with_position(position)

    def get_average_salary(self) -> float:
        """Return the average salary of all employees in
        self.current_organization.

        If there are no employees in self.current_organization, return 0.0
        """
        return self.current_organization.get_average_salary()

    def get_average_salary_for_position(self, position: str) -> float:
        """Return self.current_organization's average salary for all employees
        with the position <position>. Return 0.0 if no such employees exist.
        """
        return self.current_organization.get_average_salary(position)

    def display_direct_subordinates(self) -> None:
        """Update the list of subordinates to display self.current_employee's
        direct subordinates.

        Subordinates must be in order of increasing eids.
        """
        self.displaying_direct = True

        if self.current_employee:
            self.current_subordinates = \
                self.current_employee.get_direct_subordinates()

    def display_all_subordinates(self) -> None:
        """Update the list of subordinates to display all of
        self.current_employee's subordinates.

        Subordinates must be in order of increasing eids.
        """
        self.displaying_direct = False

        if self.current_employee:
            self.current_subordinates = \
                self.current_employee.get_all_subordinates()

    def get_higher_paid_employees(self) -> List[Employee]:
        """Return a list of all employees in the Organization that are paid more
        than self.current_employee.

        Employees must be returned with IDs in increasing order.
        """
        return self.current_employee.get_higher_paid_employees()

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        The head of the organization is defined as the employee that does not
        have any superiors.
        """
        return self.current_employee.get_organization_head()

    def get_common_superior(self, eid: int) -> Employee:
        """Return the closest common superior in the organization between
        self.current_employee and the employee with ID <eid>.

        Precondition: <eid> exists in the organization.
        """
        return self.current_employee.get_closest_common_superior(eid)

    def is_leader(self) -> bool:
        """Return True if self.current_employee is a Leader.
        """
        return isinstance(self.current_employee, Leader)

    def get_current_employee_department(self) -> str:
        """Return the department that self.current_employee belongs to.

        If self.current_employee is not part of any department, return "".
        """
        if self.current_employee:
            return self.current_employee.get_department_name()

        return ""

    def get_position_in_hierarchy(self) -> str:
        """Return the full position of self.current_employee.
        The full position takes the form:
        <self.current_employee's position>

        Followed by a comma separating any departments they're a part of (from
        their immediate department, to the department that one belongs to, and
        so on.)
        """
        return self.current_employee.get_position_in_hierarchy()

    def find_department_employees(self) -> List[Employee]:
        """Return a list of employees in self.current_employee's department.

        Pre-condition: self.current_employee is a Leader.
        """
        return self.current_employee.get_department_employees()

    def take_over_department(self) -> None:
        """Makes self.current_employee the leader of their current department,
        becoming the superior of the current department leader.
        self.current_employee keeps all of their subordinates, in addition
        to gaining the leader as a subordinate.

        If self.current_employee is already a leader or does not belong to a
        department, nothing happens.
        """

        # Keep the employee's ID number so we can update self.current_employee
        # to the leader version afterwards.
        eid = self.current_employee.eid

        organization_head = self.current_employee.change_department_leader()
        self.current_organization.set_head(organization_head)

        # Update the current employee being displayed
        self.current_employee = self.current_organization.get_employee(eid)

    def become_leader(self, department_name: str) -> None:
        """Make self.current_employee the leader of a new department with the
        name <department_name>.

        If self.current_employee is already a leader, changes the name of their
        department to department_name.
        """
        # Keep the employee's ID number so we can update self.current_employee
        # to the leader version afterwards.
        eid = self.current_employee.eid

        leader = self.current_employee.become_leader(department_name)
        self.current_organization.set_head(leader.get_organization_head())

        # Update the current employee being displayed
        self.current_employee = self.current_organization.get_employee(eid)

    def become_employee(self) -> None:
        """Make self.current_employee an employee instead of a leader.

        Pre-condition: self.current_employee is a Leader.
        """
        # Keep the employee's ID number so we can update self.current_employee
        # to the employee version afterwards.
        eid = self.current_employee.eid

        employee = self.current_employee.become_employee()
        self.current_organization.set_head(employee.get_organization_head())

        # Update the current employee being displayed
        self.current_employee = self.current_organization.get_employee(eid)

    def obtain_subordinates(self, ids: List[int]) -> None:
        """Set the employees with IDs in ids as subordinates of
        self.current_employee.

        If those employees have subordinates, the superior of those subordinates
        becomes the employee's original superior.

        Pre-condition: self.current_employee's id is not in ids.
        """
        organization_head = self.current_employee.obtain_subordinates(ids)
        self.current_organization.set_head(organization_head)

    def fire_employee(self, eid: int) -> None:
        """Fire the employee with ID eid from self.current_organization.

        Pre-condition: there is an employee with the eid <eid> in
        self.current_organization.
        """
        previous_id = self.current_employee.eid

        self.current_organization.fire_employee(eid)

        if previous_id == eid:
            self.current_employee = self.current_organization.get_head()

    def fire_lowest_rated_employee(self) -> None:
        """Fire the lowest rated employee in self.current_organization.

        If two employees have the same rating, the one with the lowest id
        is fired.
        """
        self.current_organization.fire_lowest_rated_employee()

        # Update the display if the previous self.current_employee is no longer
        # in the organization
        eid = self.current_employee.eid
        if not self.current_organization.get_employee(eid):
            self.current_employee = self.current_organization.get_head()

    def fire_under_rating(self, rating: int) -> None:
        """Fire all employees with a rating below rating.

        Employees should be fired in order of increasing rating: the lowest
        rated employees are to be removed first. Break ties in order of eid.
        """
        self.current_organization.fire_under_rating(rating)

        # Update the display if the previous self.current_employee is no longer
        # in the organization
        eid = self.current_employee.eid
        if not self.current_organization.get_employee(eid):
            self.current_employee = self.current_organization.get_head()

    def promote_employee(self, eid: int) -> None:
        """Promote the employee with the eid <eid> in self.current_organization
        until they have a superior with a higher rating than them or until they
        are the head of the organization.

        Precondition: There is an employee in self.current_organization with
        eid <eid>.
        """
        self.current_organization.promote_employee(eid)

        self.current_employee = \
            self.current_organization.get_employee(self.current_employee.eid)

    def get_department_salary_tree(self) -> DepartmentSalaryTree:
        """Return the DepartmentSalaryTree that corresponds to
        self.current_organization.
        """
        return create_department_salary_tree(self.current_organization)

    def file_to_organization(self, filename: str) -> None:
        """Read the organization data in the file named filename, creating an
        organization from it and setting it as self.current_organization.
        Set the current employee to the head of the organization.
        """
        f = open(filename)
        self.current_organization = create_organization_from_file(f)
        self.current_employee = self.current_organization.get_head()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['organization_hierarchy', 'doctest',
    #                                'typing', 'python_ta'],
    #     'disable': ['E9998'],
    #     'max-args': 7
    # })
