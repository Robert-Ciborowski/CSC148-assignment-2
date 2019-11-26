from organization_hierarchy import Employee, Leader, Organization


def test_employee_general() -> None:
    e1 = Employee(1, "e1", "a", 1, 50)
    e2 = Employee(2, "e2", "a", 1, 50)
    e3 = Employee(3, "e3", "a", 1, 50)
    e4 = Employee(4, "e4", "a", 1, 50)
    e5 = Employee(5, "e5", "a", 1, 50)
    e6 = Employee(6, "e6", "a", 1, 50)
    e7 = Employee(7, "e7", "a", 1, 50)
    e7.become_subordinate(e5)
    e5.become_subordinate(e2)
    e4.become_subordinate(e2)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e6.become_subordinate(e3)
    assert e6.get_all_subordinates() == []
    assert e2.get_all_subordinates() == [e4, e5, e7]
    assert e2.get_direct_subordinates() == [e4, e5]
    assert e7.get_organization_head() == e1
    assert e1.get_organization_head() == e1
    assert e7.get_closest_common_superior(4) == e2
    assert e2.get_closest_common_superior(4) == e2
    assert e2.get_closest_common_superior(7) == e2

    # assert e7.become_leader("seven") == e1
    assert len(e5.get_direct_subordinates()) == 1

    e7 = e5.get_direct_subordinates()[0]
    # assert isinstance(e7, Leader)
    assert e1.get_highest_rated_subordinate() == e2
    assert e5.get_highest_rated_subordinate().eid == 7
    # assert e7.get_department_leader() == e7

    # assert e2.become_leader('two') == e1
    e2 = e1.get_direct_subordinates()[0]
    assert e2.eid == 2

    assert e1.become_leader('one').eid == 1
    e1 = e2.become_leader(3)
    # assert e1.obtain_subordinates([2]) == e1
    # assert e1.get_direct_subordinates() == [e2, e3, e4, e5]


def test_obtain_sub_already_sub() -> None:
    e1 = Employee(1, "e1", "a", 1, 50)
    e2 = Employee(2, "e2", "a", 1, 50)
    e3 = Employee(3, "e3", "a", 1, 50)
    e4 = Employee(4, "e4", "a", 1, 50)
    e5 = Employee(5, "e5", "a", 1, 50)
    e6 = Employee(6, "e6", "a", 1, 50)
    e7 = Employee(7, "e7", "a", 1, 50)
    e2.become_subordinate(e1)
    e3.become_subordinate(e2)
    e4.become_subordinate(e2)
    e5.become_subordinate(e4)
    e6.become_subordinate(e4)
    e7.become_subordinate(e5)
    assert e3.obtain_subordinates([4, 5]) == e1
    assert e2.get_direct_subordinates() == [e3, e6, e7]


def test_obtain_sub_already_sub_anotha_one() -> None: #dj khaled
    e1 = Employee(1, "e1", "a", 1, 50)
    e2 = Employee(2, "e2", "a", 1, 50)
    e3 = Employee(3, "e3", "a", 1, 50)
    e4 = Employee(4, "e4", "a", 1, 50)
    e5 = Employee(5, "e5", "a", 1, 50)
    e6 = Employee(6, "e6", "a", 1, 50)
    e7 = Employee(7, "e7", "a", 1, 50)
    e2.become_subordinate(e1)
    e3.become_subordinate(e2)
    e4.become_subordinate(e2)
    e5.become_subordinate(e4)
    e6.become_subordinate(e4)
    e7.become_subordinate(e5)
    assert e2.obtain_subordinates([4, 6]) == e1
    assert e2.get_direct_subordinates() == [e3, e4, e5, e6]


def test_obtain_sub_head_being_obtained() -> None:
    e1 = Employee(1, "e1", "a", 1, 1)
    e2 = Employee(2, "e2", "a", 1, 2)
    e3 = Employee(3, "e3", "a", 1, 3)
    e4 = Employee(4, "e4", "a", 1, 4)
    e5 = Employee(5, "e5", "a", 1, 5)
    e6 = Employee(6, "e6", "a", 1, 6)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    e6.become_subordinate(e5)
    assert e5.obtain_subordinates([1, 3]) == e5
    assert e5.get_direct_subordinates() == [e1, e2, e3, e4, e6]


def test_fire_head() -> None:
    o = Organization()
    e1 = Employee(1, "e1", "a", 1, 1)
    e2 = Employee(2, "e2", "a", 1, 2)
    e3 = Employee(3, "e3", "a", 1, 3)
    e4 = Employee(4, "e4", "a", 1, 4)
    e5 = Employee(5, "e5", "a", 1, 5)
    e6 = Employee(6, "e6", "a", 1, 6)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    e6.become_subordinate(e5)
    o.add_employee(e1)
    assert o.get_head() == e1
    o.fire_employee(1)
    assert o.get_head() == e3
    o.fire_employee(3)
    assert o.get_head() == e5
    o.fire_employee(4)
    assert o.get_head() == e5
    o.fire_employee(5)
    assert o.get_head() == e6


def test_fire_lowest_rated() -> None:
    o = Organization()
    e1 = Employee(1, "e1", "a", 1, 1)
    e2 = Employee(2, "e2", "a", 1, 2)
    e3 = Employee(3, "e3", "a", 1, 3)
    e4 = Employee(4, "e4", "a", 1, 4)
    e5 = Employee(5, "e5", "a", 1, 5)
    e6 = Employee(6, "e6", "a", 1, 6)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    e6.become_subordinate(e5)
    o.add_employee(e1)
    assert o.get_head() == e1
    o.fire_lowest_rated_employee()
    assert o.get_head() == e3
    o.fire_lowest_rated_employee()
    assert o.get_head() == e3
    o.fire_lowest_rated_employee()
    o.fire_lowest_rated_employee()
    o.fire_lowest_rated_employee()
    assert o.get_head() == e6


def test_become_each_other() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Employee(3, "Sofia", "Manager", 25000, 40)
    e2.become_subordinate(e1)
    e3.become_subordinate(e2)
    assert e3.get_department_name() == 'Some Corp.'
    lol = e2.become_leader('chloeisamazingandneedschicken')
    assert isinstance(lol.get_employee(2), Leader)
    assert e3.get_department_name() == 'chloeisamazingandneedschicken'
    lol = e1.become_employee()
    assert isinstance(lol.get_employee(1), Employee)
    assert isinstance(lol.get_employee(1), Leader) == False
    assert lol.get_employee(1).get_department_name() == ''
    assert len(lol.get_employee(1).get_all_subordinates()) == 2
    assert lol.get_employee(2).get_department_name() == \
           'chloeisamazingandneedschicken'


if __name__ == '__main__':
    import pytest

    pytest.main(['test.py'])

