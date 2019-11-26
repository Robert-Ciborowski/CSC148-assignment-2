from organization_hierarchy import Employee, Leader, Organization


def test_obtain_employees() -> None:
    o = Organization()
    e1 = Leader(1, 'Holly', '', 1, 1, 'Department')
    o.add_employee(e1)
    e2 = Employee(2, 'Ivan', '', 1, 1)
    o.add_employee(e2, 1)
    e3 = Employee(3, 'Kevin', '', 1, 1)
    o.add_employee(e3, 2)
    e4 = Employee(4, 'Joe', 'Mama', 1, 100)
    o.add_employee(e4, 2)
    e5 = Employee(5, 'Linda', '', 1, 1)
    o.add_employee(e5, 4)
    assert e1.get_direct_subordinates() == [e2]
    assert e2.get_superior() == e1
    assert e2.get_direct_subordinates() == [e3, e4]
    assert e3.get_superior() == e2
    assert e4.get_superior() == e2
    assert e3.get_direct_subordinates() == []
    assert e4.get_direct_subordinates() == [e5]
    assert e5.get_superior() == e4
    e4.obtain_subordinates([2])
    assert o.get_head() == e1
    assert e1.get_direct_subordinates() == [e3, e4]
    assert e3.get_superior() == e1
    assert e4.get_superior() == e1
    assert e3.get_direct_subordinates() == []
    assert e4.get_direct_subordinates() == [e2, e5]
    assert e2.get_superior() == e4
    assert e5.get_superior() == e4

if __name__ == '__main__':
    import pytest

    pytest.main(['test_3.py'])
