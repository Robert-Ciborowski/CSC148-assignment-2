from organization_hierarchy import Employee, Organization, Leader,\
    DepartmentSalaryTree, create_department_salary_tree


def test_department_salary_tree_simple() -> None:
    e1 = Leader(1, "Sarah", "CEO", 300000, 89, "Some Corp.")
    e2 = Leader(2, "Sandra", "Secretary", 20000, 89, "Finance")
    e3 = Employee(3, "Sofia", "Manager", 300000, 89)
    e4 = Leader(4, "Senya", "HR Head", 5000, 89, "Human Resources")
    e5 = Employee(5, "Sylvia", "Secretary", 300000, 99)
    e6 = Employee(6, "Selena", "Grunt", 5000, 99)
    e7 = Employee(7, "Sophie", "Grunt", 5000, 99)
    o = Organization()
    o.add_employee(e1)
    o.add_employee(e2, 1)
    o.add_employee(e3, 1)
    o.add_employee(e4, 1)
    o.add_employee(e5, 1)
    o.add_employee(e6, 4)
    o.add_employee(e7, 4)
    tree = create_department_salary_tree(o)
    assert int(tree.salary) == 300000
    assert tree.department_name == "Some Corp."
    assert len(tree.subdepartments) == 2
    assert int(tree.subdepartments[0].salary) == 20000
    assert tree.subdepartments[0].department_name == "Finance"
    assert len(tree.subdepartments[0].subdepartments) == 0
    assert int(tree.subdepartments[1].salary) == 5000
    assert tree.subdepartments[1].department_name == "Human Resources"
    assert len(tree.subdepartments[1].subdepartments) == 0

if __name__ == '__main__':
    import pytest

    pytest.main(['test_department_salary_tree.py'])

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['__future__', 'typing', 'json',
    #                                'python_ta', 'doctest', 'io',
    #                                'store', 'pytest'],
    #     'disable': ['W0613', 'W0212']})
