from organization_hierarchy import Organization, Employee


def test_init() -> None:
    org = Organization(None)
    assert org._head is None
    e = Employee(1, 'Boss', 'CEO', 50000, 50)
    org2 = Organization(e)
    assert org2._head.name == 'Boss'


def test_get_emp() -> None:
    org2 = Organization(None)
    assert org2.get_employee(1) is None
    e = Employee(1, 'Boss', 'CEO', 50000, 50)
    org = Organization(e)
    assert org.get_employee(1).name == 'Boss'
    e1 = Employee(2, 'Man', 'Manager', 20000, 50)
    e.add_subordinate(e1)
    assert org.get_employee(2).name == 'Man'
    assert org.get_employee(3) is None


def test_add_emp() -> None:
    org = Organization()
    e = Employee(1, 'Boss', 'CEO', 50000, 50)
    assert org.get_employee(1) is None
    org.add_employee(e)
    assert org.get_employee(1).name == 'Boss'
    e1 = Employee(2, 'Sarah', 'Keyboardist', 1000000, 100)
    org.add_employee(e1, 1)
    assert org.get_employee(2).name == 'Sarah'
    assert e1.get_superior() == e
    assert len(e.get_all_subordinates()) == 1
    e2 = Employee(3, 'John', 'Doe', 10, 10)
    org.add_employee(e2, 2)
    assert org.get_employee(3).name == 'John'
    assert e2.get_superior() == e1


def test_avg_sal() -> None:
    org = Organization()
    assert org.get_average_salary() == 0.0
    e = Employee(1, 'Boss', 'CEO', 50000, 50)
    org.add_employee(e)
    e1 = Employee(2, 'Sarah', 'Keyboardist', 100000, 100)
    org.add_employee(e1, 1)
    assert org.get_average_salary() == 75000
    assert org.get_average_salary('Keyboardist') == 100000


def test_get_head() -> None:
    assert True


def test_get_free_id() -> None:
    assert True


def test_get_emps_pos() -> None:
    assert True


if __name__ == '__main__':
    import pytest

    pytest.main(['test_organization_2.py'])
