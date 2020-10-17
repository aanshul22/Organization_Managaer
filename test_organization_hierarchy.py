from organization_hierarchy import Employee, Leader, Organization, DepartmentSalaryTree, create_department_salary_tree


def test_become_subordinate() -> None:
    a = Employee(1, 'Alpha', 'Slave', 80, 80)
    b = Employee(2, 'Beta', 'Worker', 90, 90)
    c = Employee(3, 'Charlie', 'God', 100, 100)
    a._subordinates = [b]
    b._superior = a
    c.become_subordinate(a)
    assert c._superior == a
    assert c._subordinates == []
    assert a._subordinates[1] == c
    b.become_subordinate(None)
    assert b._superior == None
    assert b._subordinates == []
    assert len(a._subordinates) == 1
    assert a._subordinates[0] == c


def test_create_department_salary_tree() -> None:
    e1 = Leader(1, "Emma Ployee", "Worker", 15000, 50, 'Marketing')
    e2 = Employee(2, "Sue Perior", "Manager", 25000, 30)
    e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
    e4 = Leader(4, "Emma Watson", "Manager", 30000, 50, 'Sales')
    e5 = Leader(5, "The Rock", "Worker", 15000, 15, 'Management')
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    o = Organization(e1)
    dst = create_department_salary_tree(o)
    assert dst.department_name == 'Marketing'
    assert dst.salary == 30000.0
    assert len(dst.subdepartments) == 2
    assert dst.subdepartments[0].department_name == 'Sales'
    assert dst.subdepartments[0].salary == 30000.0
    assert dst.subdepartments[1].department_name == 'Management'
    assert dst.subdepartments[1].salary == 15000.0


def test_create_department_salary_tree_no_leaders() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 15000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 25000, 30)
    e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
    e4 = Employee(4, "Emma Watson", "Manager", 30000, 50)
    e5 = Employee(5, "The Rock", "Worker", 15000, 15)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    o = Organization(e1)
    result = create_department_salary_tree(o)
    assert result is None


def test_obtain_subordinates_2_1() -> None:
    e1 = Employee(1, "1", "CEO", 15000, 1)
    e2 = Employee(2, "2", "Sub", 25000, 2)
    e3 = Employee(3, "3", "Sub", 50000, 3)
    e5 = Employee(5, "5", "Sub", 15000, 5)
    e6 = Employee(6, "6", "Sub", 30000, 6)
    e40 = Employee(40, "40", "Sub", 30000, 40)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e6.become_subordinate(e3)
    e40.become_subordinate(e2)
    e5.become_subordinate(e2)
    head = e6.obtain_subordinates([2, 1])
    assert head.name == '40'
    assert head.get_superior() is None
    assert len(head.get_direct_subordinates()) == 2
    assert head.get_direct_subordinates()[0].eid == 3
    assert head.get_direct_subordinates()[1].eid == 5


def test_obtain_subordinates_1_2() -> None:
    e1 = Employee(1, "1", "CEO", 15000, 1)
    e2 = Employee(2, "2", "Sub", 25000, 2)
    e3 = Employee(3, "3", "Sub", 50000, 3)
    e5 = Employee(5, "5", "Sub", 15000, 5)
    e6 = Employee(6, "6", "Sub", 30000, 6)
    e40 = Employee(40, "40", "Sub", 30000, 40)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e6.become_subordinate(e3)
    e40.become_subordinate(e2)
    e5.become_subordinate(e2)
    head = e6.obtain_subordinates([1, 2])
    assert head.name == '3'
    assert len(head.get_direct_subordinates()) == 3
    assert head.get_direct_subordinates()[0].eid == 5
    assert head.get_direct_subordinates()[1].eid == 6
    assert head.get_direct_subordinates()[2].eid == 40


if __name__ == "__main__":
    import pytest

    pytest.main(['test_organization_hierarchy.py'])
