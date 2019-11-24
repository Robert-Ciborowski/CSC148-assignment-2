from organization_hierarchy import Employee, Organization, Leader


def test_get_employee_simple() -> None:
    o = Organization()
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    o.add_employee(e1)
    assert o.get_employee(1) is e1
    assert o.get_employee(2) is None


def test_get_employee_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 22000, 30)
    o = Organization()
    o.add_employee(e4)
    o.add_employee(e7, 4)
    o.add_employee(e6, 4)
    o.add_employee(e2, 4)
    o.add_employee(e1, 2)
    o.add_employee(e3, 2)
    o.add_employee(e5, 2)
    assert o.get_employee(1) is e1
    assert o.get_employee(4) is e4
    assert o.get_employee(12) is None


# Note: add_employee already gets tested by get_employee
def test_add_employee_simple() -> None:
    o = Organization()
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    o.add_employee(e2)
    assert o.get_head() is e2
    o.add_employee(e1, 2)
    assert o.get_employee(1) is e1
    assert e1.get_superior() is e2


def test_get_average_salary_simple() -> None:
    o = Organization()
    assert o.get_average_salary() == 0
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    o.add_employee(e2)
    o.add_employee(e1, 2)
    assert o.get_average_salary() == 15000.0


def test_get_average_salary_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 50000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 50000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 50000, 30)
    o = Organization()
    o.add_employee(e4)
    o.add_employee(e2, 4)
    o.add_employee(e1, 2)
    o.add_employee(e3, 2)
    o.add_employee(e5, 2)
    assert round(o.get_average_salary()) == 140000


def test_get_average_salary_position_filter() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 20000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 30000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 20000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 20000, 30)
    e8 = Employee(8, "Sparrow", "Contract Worker", 60000, 30)
    e9 = Employee(9, "Nick", "Contract Worker", 70000, 30)
    e10 = Employee(10, "Theseus", "Contract Worker", 80000, 30)
    o = Organization()
    o.add_employee(e4)
    o.add_employee(e2, 4)
    o.add_employee(e1, 2)
    o.add_employee(e3, 2)
    o.add_employee(e5, 2)
    o.add_employee(e6, 4)
    o.add_employee(e7, 4)
    o.add_employee(e8, 1)
    o.add_employee(e9, 1)
    o.add_employee(e10, 1)
    assert round(o.get_average_salary("Worker")) == 20000


def test_get_employees_with_position() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 22000, 30)
    o = Organization()
    o.add_employee(e4)
    o.add_employee(e7, 4)
    o.add_employee(e6, 4)
    o.add_employee(e2, 4)
    o.add_employee(e1, 2)
    o.add_employee(e3, 2)
    o.add_employee(e5, 2)
    assert o.get_employees_with_position("Worker") == [e1, e3, e5, e6, e7]
    assert o.get_employees_with_position("Manager") == [e2]
    assert o.get_employees_with_position("CEO") == [e4]


def test_fire_employee_simple() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Employee(3, "Sofia", "Manager", 25000, 40)
    e4 = Employee(4, "Senya", "Grunt", 5000, 30)
    e5 = Employee(5, "Sylvia", "Grunt", 5000, 40)
    o = Organization()
    o.add_employee(e1)
    o.add_employee(e2, 1)
    o.add_employee(e3, 1)
    o.add_employee(e4, 3)
    o.add_employee(e5, 3)
    o.fire_employee(3)
    assert e1.get_direct_subordinates() == [e2, e4, e5]
    assert e4.get_superior() == e1
    assert e5.get_superior() == e1


def test_fire_employee_new_head() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Employee(3, "Sofia", "Manager", 25000, 40)
    e4 = Employee(4, "Senya", "Grunt", 5000, 30)
    e5 = Employee(5, "Sylvia", "Grunt", 5000, 40)
    o = Organization()
    o.add_employee(e1)
    o.add_employee(e2, 1)
    o.add_employee(e3, 1)
    o.add_employee(e4, 3)
    o.add_employee(e5, 3)
    o.fire_employee(1)
    head = o.get_head()
    assert head.eid == 3
    assert head.get_direct_subordinates() == [e2, e4, e5]
    assert e2.get_superior() == head
    assert e4.get_superior() == head
    assert e5.get_superior() == head


if __name__ == '__main__':
    import pytest

    pytest.main(['test_organization.py'])

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['__future__', 'typing', 'json',
    #                                'python_ta', 'doctest', 'io',
    #                                'store', 'pytest'],
    #     'disable': ['W0613', 'W0212']})
