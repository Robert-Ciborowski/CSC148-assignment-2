from organization_hierarchy import merge, Employee, Leader


def test_merge() -> None:
    assert merge([], []) == []
    assert merge([], [1]) == [1]
    assert merge([1, 3], [2]) == [1, 2, 3]
    assert merge([1, 2, 3], [4]) == [1, 2, 3, 4]
    assert merge([2, 6, 7, 9, 13], [1, 3, 5, 8, 10, 11, 14]) == [1, 2, 3, 5, 6,
                                                                 7, 8, 9, 10,
                                                                 11, 13, 14]


def test_init() -> None:
    e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    assert e.eid == 1
    assert e.name == "Emma Ployee"
    assert e.position == "Worker"
    assert e.salary == 10000
    assert e.rating == 50
    assert e.get_direct_subordinates() == []
    assert e.get_superior() is None


def test_lt() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(1, "Evil Clone", "Worker", 10000, 50)
    assert e1 < e2
    assert not e2 < e1
    assert not e3 < e1


def test_direct_subs() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(3, "Cowor Ker", "Worker", 10000, 50)
    assert e2.get_direct_subordinates() == []
    e3.become_subordinate(e2)
    e1.become_subordinate(e2)
    lst = e2.get_direct_subordinates()
    assert len(lst) == 2
    assert lst[0].eid == 1
    assert lst[1].eid == 3


def test_get_all_subs() -> None:
    e1 = Employee(5, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(7, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(8, "Cowor Ker", "Worker", 10000, 50)
    assert (e2.get_all_subordinates() == [])
    e3.become_subordinate(e2)
    e1.become_subordinate(e2)
    e4 = Employee(2, "First Last", "Worker", 5, 50)
    e4.become_subordinate(e3)
    lst = e2.get_all_subordinates()
    assert len(lst) == 3
    assert lst[0].eid == 2
    assert lst[1].eid == 5
    assert lst[2].eid == 8


def test_get_org_head() -> None:
    e1 = Employee(1, "Boss", "CEO", 50000, 50)
    assert e1.get_organization_head().eid == 1
    e2 = Employee(2, "Sue", "Manager", 20000, 50)
    e2.become_subordinate(e1)
    assert e2.get_organization_head().eid == 1
    e3 = Employee(3, "Emma", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    assert e3.get_organization_head().eid == 1


def test_get_sup() -> None:
    e1 = Employee(1, "Boss", "CEO", 50000, 50)
    assert e1.get_superior() is None
    e2 = Employee(2, "Sue", "Manager", 20000, 50)
    e2.become_subordinate(e1)
    assert e2.get_superior().eid == 1
    e3 = Employee(3, "Emma", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    assert e3.get_superior().eid == 2


def test_become_sub() -> None:
    e1 = Employee(1, "Boss", "CEO", 50000, 50)
    assert e1.get_superior() is None
    e2 = Employee(2, "Sue", "Manager", 20000, 50)
    e2.become_subordinate(e1)
    assert e2.get_superior().eid == 1
    assert len(e1.get_direct_subordinates()) == 1
    e3 = Employee(3, "Emma", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    assert e3.get_superior().eid == 2
    assert len(e1.get_direct_subordinates()) == 1
    assert len(e1.get_all_subordinates()) == 2


def test_remove_sub() -> None:
    e1 = Employee(5, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(7, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(8, "Cowor Ker", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    e1.become_subordinate(e2)
    assert len(e2.get_direct_subordinates()) == 2
    e2.remove_subordinate_id(5)
    assert e1.get_superior() == e2
    assert len(e2.get_direct_subordinates()) == 1
    e1.become_subordinate(e3)
    assert len(e2.get_all_subordinates()) == 2
    e2.remove_subordinate_id(5)
    assert len(e2.get_direct_subordinates()) == 1
    assert e1.get_superior() == e3
    e1.become_subordinate(e3)
    assert len(e2.get_all_subordinates()) == 2
    e2.remove_subordinate_id(8)
    assert len(e2.get_all_subordinates()) == 0
    assert e1.get_superior() == e3


def test_add_sub() -> None:
    e1 = Employee(5, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(7, "Sue Perior", "Manager", 20000, 30)
    assert len(e1.get_all_subordinates()) == 0
    e1.add_subordinate(e2)
    assert len(e1.get_all_subordinates()) == 1
    assert e2.get_superior() is None


def test_get_emp() -> None:
    e1 = Employee(1, "Boss", "CEO", 50000, 50)
    assert e1.get_employee(0) is None
    e2 = Employee(2, "Sue", "Manager", 20000, 50)
    e2.become_subordinate(e1)
    assert e1.get_employee(2).name == "Sue"
    e3 = Employee(3, "Emma", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    assert e1.get_employee(3).name == "Emma"


def test_get_emp_paid_more_than() -> None:
    e1 = Employee(1, "Boss", "CEO", 50000, 50)
    e2 = Employee(4, "Sue", "Manager", 20000, 50)
    e2.become_subordinate(e1)
    e3 = Employee(2, "Emma", "Worker", 10000, 50)
    e3.become_subordinate(e2)
    e4 = Employee(3, "Sue2", "Manager", 20000, 50)
    e4.become_subordinate(e1)
    assert len(e1.get_employees_paid_more_than(50000)) == 0
    assert len(e1.get_employees_paid_more_than(40000)) == 1
    k = e1.get_employees_paid_more_than(5000)
    assert len(k) == 4
    assert k[0].eid == 1
    assert k[1].eid == 2
    assert k[2].eid == 3
    assert k[3].eid == 4


def test_get_closest_common_superior() -> None:
    e = Employee(1, 'Name1', 'Pos1', 10, 10)
    e1 = Employee(2, 'Name2', 'Pos2', 10, 10)
    e3 = Employee(3, 'Name3', 'Pos3', 10, 10)
    e1.become_subordinate(e)
    e3.become_subordinate(e)
    assert e1.get_closest_common_superior(3).name == e.name
    e4 = Employee(4, 'Name4', 'Pos4', 10, 10)
    e4.become_subordinate(e1)
    assert e4.get_closest_common_superior(3).name == e.name
    e5 = Employee(5, 'Name5', 'Pos5', 10, 10)
    e5.become_subordinate(e1)
    e6 = Employee(6, 'Name6', 'Pos6', 10, 10)
    e6.become_subordinate(e5)
    assert e5.get_closest_common_superior(4).name == 'Name2'
    assert e1.get_closest_common_superior(1) == e


def test_get_department_name() -> None:
    e2 = Employee(3, 'Joe', 'Worker', 10000, 50)
    assert e2.get_department_name() == ''
    l = Leader(1, 'Lena', 'LEADER', 100000, 100, 'Department')
    assert l.get_department_name() == 'Department'
    e1 = Employee(2, 'Mama', 'Anna', 50000, 100)
    e1.become_subordinate(l)
    assert e1.get_department_name() == 'Department'
    e2.become_subordinate(e1)
    assert e2.get_department_name() == 'Department'


def test_get_position_in_hierarchy() -> None:
    assert True


def test_get_dept_lead() -> None:
    assert True


def test_change_dept_lead() -> None:
    pass


def test_get_dept_emp() -> None:
    e = Leader(1, 'Name1', 'Pos1', 10000, 50, 'BigDept')
    e1 = Employee(2, 'Name2', 'Pos2', 1000, 50)
    e2 = Employee(3, 'Name3', 'Pos2', 1000, 50)
    e1.become_subordinate(e)
    e2.become_subordinate(e)
    e3 = Employee(4, 'Name4', 'Pos2', 1000, 50)
    e3.become_subordinate(e1)
    e4 = Leader(5, 'Name5', 'Pos3', 10000, 50, 'SmallDept1')
    e4.become_subordinate(e)
    e5 = Leader(6, 'Name6', 'Pos4', 10000, 50, 'SmallDept2')
    e5.become_subordinate(e2)
    assert len(e.get_department_employees()) == 6

# stolen tests


def test_get_higher_paid_employees_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    more_than = e2.get_higher_paid_employees()
    assert len(more_than) == 1
    assert more_than[0].name == 'Bigg Boss'

if __name__ == '__main__':
    import pytest

    pytest.main(['test_employee_2.py'])
