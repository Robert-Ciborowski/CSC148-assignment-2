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


def test_line_obtain_subs() -> None:
    o = Organization()
    e1 = Employee(1, '', '', 1, 1)
    o.add_employee(e1)
    e2 = Employee(2, '', '', 1, 1)
    o.add_employee(e2, 1)
    e3 = Employee(3, '', '', 1, 1)
    o.add_employee(e3, 1)
    e4 = Employee(4, '', '', 1, 1)
    o.add_employee(e4, 3)
    e5 = Employee(5, '', '', 1, 1)
    o.add_employee(e5, 4)
    assert e2 in e1.get_direct_subordinates()
    assert e3 in e1.get_direct_subordinates()
    assert not e5 in e1.get_direct_subordinates()
    assert e5 in e1.get_all_subordinates()
    assert len(e2.get_all_subordinates()) == 0
    e2.obtain_subordinates([3, 4])
    assert not e3 in e1.get_direct_subordinates()
    assert e2 in e1.get_direct_subordinates()
    assert e3 in e2.get_direct_subordinates()
    assert e4 in e2.get_direct_subordinates()
    assert e5 in e1.get_direct_subordinates()
    assert e3 in e2.get_direct_subordinates()
    assert e4 in e2.get_direct_subordinates()


if __name__ == '__main__':
    import pytest

    pytest.main(['test_3.py'])
