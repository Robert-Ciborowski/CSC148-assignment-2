from organization_hierarchy import Employee, Leader


def test__lt__() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    assert e1 < e2


def test_get_direct_subordinates_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e1.become_subordinate(e2)
    assert e2.get_direct_subordinates()[0].name == 'Emma Ployee'


def test_get_direct_subordinates_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 20000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 20000, 30)
    e6 = Employee(6, "Terry", "Worker", 20000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 20000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    assert e2.get_direct_subordinates() == [e1, e3, e5]
    assert e4.get_direct_subordinates() == [e2, e6, e7]
    assert e1.get_direct_subordinates() == []


def test_get_all_subordinates_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    assert e3.get_all_subordinates()[0].name == 'Emma Ployee'
    assert e3.get_all_subordinates()[1].name == 'Sue Perior'


def test_get_all_subordinates_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 20000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 20000, 30)
    e6 = Employee(6, "Terry", "Worker", 20000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 20000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    assert e2.get_all_subordinates() == [e1, e3, e5]
    assert e4.get_all_subordinates() == [e1, e2, e3, e5, e6, e7]
    assert e1.get_all_subordinates() == []


def test_get_organization_head_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    assert e1.get_organization_head().name == 'Bigg Boss'


def test_get_organization_head_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 20000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 20000, 30)
    e6 = Employee(6, "Terry", "Worker", 20000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 20000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    assert e1.get_organization_head() == e4


def test_get_superior_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    assert e1.get_superior() is None
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e1.become_subordinate(e2)
    assert e1.get_superior().name == 'Sue Perior'


def test_become_subordinate() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e1.become_subordinate(e2)
    assert e1.get_superior().eid == 2
    assert e2.get_direct_subordinates()[0].eid == 1
    e1.become_subordinate(None)
    assert e1.get_superior() is None
    assert e2.get_direct_subordinates() == []


def test_remove_subordinate_id() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e1.become_subordinate(e2)
    assert e2.get_direct_subordinates()[0].eid == 1
    e2.remove_subordinate_id(1)
    assert e2.get_direct_subordinates() == []
    assert e1.get_superior() is e2


def test_add_subordinate() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e2.add_subordinate(e1)
    assert e2.get_direct_subordinates()[0].eid == 1
    assert e1.get_superior() is None


def test_get_employee() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    assert e3.get_employee(1) is e1
    assert e1.get_employee(1) is e1
    assert e2.get_employee(3) is None


def test_get_employees_paid_more_than_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    more_than_10000 = e3.get_employees_paid_more_than(10000)
    assert len(more_than_10000) == 2
    assert more_than_10000[0].name == 'Sue Perior'
    assert more_than_10000[1].name == 'Bigg Boss'


def test_get_employees_paid_more_than_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 22000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    more_than_20000 = e4.get_employees_paid_more_than(20000)
    assert more_than_20000 == [e2, e4, e7]


def test_get_higher_paid_employees_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    more_than = e2.get_higher_paid_employees()
    assert len(more_than) == 1
    assert more_than[0].name == 'Bigg Boss'


def test_get_higher_paid_employees_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 52000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 62000, 30)
    e8 = Employee(8, "Sparrow", "Contract Worker", 60000, 30)
    e9 = Employee(9, "Nick", "Contract Worker", 70000, 30)
    e10 = Employee(10, "Theseus", "Contract Worker", 80000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    e8.become_subordinate(e1)
    e9.become_subordinate(e1)
    e10.become_subordinate(e1)
    assert e2.get_higher_paid_employees() == [e1, e4, e7, e8, e9, e10]


def test_get_closest_common_superior_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Some Corp.")
    e1.become_subordinate(e3)
    e2.become_subordinate(e3)
    superior = e1.get_closest_common_superior(3)
    assert superior.eid == 3


def test_get_closest_common_superior_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 52000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 62000, 30)
    e8 = Employee(8, "Sparrow", "Contract Worker", 60000, 30)
    e9 = Employee(9, "Nick", "Contract Worker", 70000, 30)
    e10 = Employee(10, "Theseus", "Contract Worker", 80000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    e8.become_subordinate(e1)
    e9.become_subordinate(e1)
    e10.become_subordinate(e1)
    assert e10.get_closest_common_superior(7) == e4


def test_get_closest_common_superior_self_is_superior() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 22000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    assert e4.get_closest_common_superior(1) == e4


def test_get_closest_common_superior_other_is_superior() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 30)
    e4 = Leader(4, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 30)
    e6 = Employee(6, "Terry", "Worker", 5000, 30)
    e7 = Employee(7, "Odysseus", "Worker", 22000, 30)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    assert e1.get_closest_common_superior(4) == e4


def test_get_position_in_hierarchy() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Dept E")
    e3 = Leader(3, "Robocop", "Worker", 20000, 30, "Dept D")
    e4 = Leader(4, "Sarah", "Worker", 20000, 30, "Dept C")
    e5 = Leader(5, "Sofia", "Secretary", 20000, 30, "Dept B")
    e6 = Employee(6, "Terry", "COO", 20000, 30)
    e7 = Leader(7, "Sarah", "CEO", 20000, 30, "Dept A")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    e3.become_subordinate(e4)
    e4.become_subordinate(e5)
    e5.become_subordinate(e6)
    e6.become_subordinate(e7)
    assert e1.get_position_in_hierarchy() == "Worker, Dept E, Dept D, Dept C," \
                                             " Dept B, Dept A"
    assert e5.get_position_in_hierarchy() == "Secretary, Dept B, Dept A"
    assert e7.get_position_in_hierarchy() == "CEO, Dept A"


def test_get_department_name() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    assert e1.get_department_name() == ''
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    e1.become_subordinate(e2)
    assert e1.get_department_name() == 'Department'


def test_get_department_leader() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    assert e1.get_department_leader() is None
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    assert e1.get_department_leader().name == 'Sue Perior'
    assert e2.get_department_leader().name == 'Sue Perior'


# see revised test in test_employee_1.py
def test_change_department_leader_simple() -> None:
    assert False


#     e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
#     e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
#     e3 = Employee(3, "Sofia", "Manager", 25000, 30)
#     e4 = Employee(4, "Senya", "Grunt", 5000, 30)
#     e5 = Employee(5, "Sylvia", "Grunt", 5000, 30)
#     e2.become_subordinate(e1)
#     e3.become_subordinate(e1)
#     e4.become_subordinate(e3)
#     e5.become_subordinate(e3)
#     new_head = e3.change_department_leader()
#     assert new_head.name == "Sofia"
#     assert new_head.get_department_name() == "Some Corp."
#     assert new_head.get_superior() is None
#     subordinates = new_head.get_direct_subordinates()
#     assert subordinates == [e1, e4, e5]
#     assert e1.get_superior() == new_head
#     assert e4.get_superior() == new_head
#     assert e5.get_superior() == new_head
#     subordinates = e1.get_direct_subordinates()
#     assert subordinates == [e2]
#     assert e2.get_superior() == e1


def test_change_department_leader_advanced() -> None:
    # see revised test in test_employee_1.py
    assert False


#     e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
#     e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
#     e3 = Leader(3, "Sofia", "Manager", 25000, 30, "Grunts Department")
#     e4 = Employee(4, "Senya", "Grunt Alpha", 15000, 30)
#     e5 = Employee(5, "Sylvia", "Grunt Beta", 10000, 30)
#     e6 = Employee(6, "Scarlett", "Grunt Gamma", 5000, 30)
#     e7 = Employee(7, "Samantha", "Grunt Epsilon", 2500, 30)
#     e2.become_subordinate(e1)
#     e3.become_subordinate(e1)
#     e4.become_subordinate(e3)
#     e5.become_subordinate(e4)
#     e6.become_subordinate(e5)
#     e7.become_subordinate(e6)
#     new_head = e6.change_department_leader()
#     assert new_head.name == "Scarlett"
#     assert new_head.get_department_name() == "Grunts Department"
#     assert new_head.get_superior() == e1
#     subordinates = new_head.get_direct_subordinates()
#     assert subordinates == [e3, e7]
#     assert e3.get_superior() == new_head
#     assert e7.get_superior() == new_head
#     subordinates = e3.get_direct_subordinates()
#     assert subordinates == [e4]
#     assert e4.get_superior() == e3


def test_get_highest_rated_subordinate_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    assert e1.get_position_in_hierarchy() == 'Worker'
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    assert e3.get_highest_rated_subordinate().name == 'Sue Perior'
    e1.become_subordinate(e3)
    assert e3.get_highest_rated_subordinate().name == 'Emma Ployee'


def test_get_highest_rated_subordinate_advanced() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 52000, 50)
    e2 = Employee(2, "Sue Perior", "Manager", 50000, 30)
    e3 = Employee(3, "Robocop", "Worker", 20000, 80)
    e4 = Leader(4, "Sarah", "CEO", 500000, 99, "Some Corp.")
    e5 = Employee(5, "Sofia", "Worker", 10000, 69)
    e6 = Employee(6, "Terry", "Worker", 5000, 79)
    e7 = Employee(7, "Odysseus", "Worker", 62000, 88)
    e8 = Employee(8, "Sparrow", "Contract Worker", 60000, 12)
    e9 = Employee(9, "Nick", "Contract Worker", 70000, 25)
    e10 = Employee(10, "Theseus", "Contract Worker", 80000, 87)
    e1.become_subordinate(e2)
    e3.become_subordinate(e2)
    e2.become_subordinate(e4)
    e5.become_subordinate(e2)
    e6.become_subordinate(e4)
    e7.become_subordinate(e4)
    e8.become_subordinate(e1)
    e9.become_subordinate(e1)
    e10.become_subordinate(e1)
    assert e2.get_highest_rated_subordinate() == e3
    assert e4.get_highest_rated_subordinate() == e7
    assert e1.get_highest_rated_subordinate() == e10


def test_swap_up_simple() -> None:
    e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    e1.become_subordinate(e2)
    e2.become_subordinate(e3)
    new_e1 = e1.swap_up()
    assert isinstance(new_e1, Leader)
    new_e2 = new_e1.get_direct_subordinates()[0]
    assert isinstance(new_e2, Employee)
    assert new_e1.position == 'Manager'
    assert new_e1.eid == 1
    assert e3.get_direct_subordinates()[0] is new_e1


def test_swap_up_repeated() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Leader(3, "Sofia", "Manager", 25000, 30, "Grunts Department")
    e4 = Employee(4, "Senya", "Grunt Alpha", 15000, 30)
    e5 = Employee(5, "Sylvia", "Grunt Beta", 10000, 30)
    e6 = Employee(6, "Scarlett", "Grunt Gamma", 5000, 30)
    e7 = Employee(7, "Samantha", "Grunt Epsilon", 2500, 100)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e4)
    e6.become_subordinate(e5)
    e7.become_subordinate(e6)

    new_e7 = e7.swap_up()
    assert new_e7.get_superior() == e5
    assert new_e7.salary == 5000
    assert new_e7.position == "Grunt Gamma"

    for i in range(4):
        new_e7 = new_e7.swap_up()

    assert isinstance(new_e7, Leader)
    assert new_e7.get_superior() is None
    assert new_e7.salary == 500000
    assert new_e7.position == "CEO"
    assert new_e7.get_department_name() == "Some Corp."
    new_subs = new_e7.get_direct_subordinates()
    assert new_subs[0].name == "Sarah"
    assert new_subs[1].name == "Sandra"


def test_obtain_subordinates_simple() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Employee(3, "Sofia", "Manager", 25000, 40)
    e4 = Employee(4, "Senya", "Grunt", 5000, 30)
    e5 = Employee(5, "Sylvia", "Grunt", 5000, 40)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    new_head = e2.obtain_subordinates([3, 5])
    assert new_head == e1
    assert e2.get_direct_subordinates() == [e3, e5]
    assert e1.get_direct_subordinates() == [e2, e4]
    assert e3.get_superior() == e2
    assert e5.get_superior() == e2
    assert e2.get_superior() == e1
    assert e4.get_superior() == e1


def test_obtain_subordinates_different_head() -> None:
    e1 = Leader(1, "Sarah", "CEO", 500000, 30, "Some Corp.")
    e2 = Employee(2, "Sandra", "Secretary", 20000, 30)
    e3 = Employee(3, "Sofia", "Manager", 25000, 40)
    e4 = Employee(4, "Senya", "Grunt", 5000, 30)
    e5 = Employee(5, "Sylvia", "Grunt", 5000, 40)
    e2.become_subordinate(e1)
    e3.become_subordinate(e1)
    e4.become_subordinate(e3)
    e5.become_subordinate(e3)
    new_head = e2.obtain_subordinates([1, 3])
    assert new_head.eid == 5
    # assert isinstance(new_head, Leader)
    new_subs = e2.get_direct_subordinates()
    assert new_subs[0].eid == 1
    assert new_subs[1].eid == 3
    assert new_head.get_direct_subordinates() == [e2, e4]
    assert new_subs[0].get_superior() == e2
    assert new_subs[1].get_superior() == e2
    assert e4.get_superior() == new_head
    assert e2.get_superior() == new_head


if __name__ == '__main__':
    import pytest

    pytest.main(['test_employee.py'])

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['__future__', 'typing', 'json',
    #                                'python_ta', 'doctest', 'io',
    #                                'store', 'pytest'],
    #     'disable': ['W0613', 'W0212']})
