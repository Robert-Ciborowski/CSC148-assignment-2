from organization_hierarchy import Employee, Leader, \
    create_organization_from_file, create_department_salary_tree, \
    Organization, DepartmentSalaryTree


def test_short_create() -> None:
    o = Organization()
    lin = Leader(1, 'Linda', 'Sewed', 10, 10, 'MyNew')
    o.add_employee(lin)
    assert o.get_head() == lin
    t = create_department_salary_tree(o)
    assert t.department_name == 'MyNew'
    assert size(t) == 1


def test_empty_create() -> None:
    o = Organization()
    assert create_department_salary_tree(o) is None
    lin = Employee(1, 'Linda', 'Tailor', 10, 10)
    o.add_employee(lin)
    assert create_department_salary_tree(o) is None


def test_medium_create() -> None:
    o = Organization()
    l1 = create_lead(1)
    l2 = create_lead(2)
    l3 = create_lead(3)
    o.add_employee(l1)
    o.add_employee(l2, 1)
    o.add_employee(l3, 1)
    e4 = create_emp(4)
    e5 = create_emp(5)
    e6 = create_emp(6)
    e7 = create_emp(7)
    o.add_employee(e4, 2)
    o.add_employee(e5, 2)
    o.add_employee(e6, 3)
    o.add_employee(e7, 3)
    dept_hier = create_department_salary_tree(o)
    assert dept_hier.department_name == 'Dept1'
    subdepts = dept_hier.subdepartments
    assert len(subdepts) == 2
    salaries = [subdepts[0].salary, subdepts[1].salary]
    assert 2900.0 / 3 in salaries
    assert 4300.0 / 3 in salaries
    assert size(dept_hier) == 3


def test_med_2_create() -> None:
    leads = create_leaders(4)
    emps = create_emps(5)
    o = Organization()
    e = leads[0]
    o.add_employee(e)
    o.add_employee(leads[1], 1)
    o.add_employee(leads[2], 1)
    o.add_employee(leads[3], 2)
    o.add_employee(emps[0], 4)
    o.add_employee(emps[1], 4)
    o.add_employee(emps[2], 2)
    o.add_employee(emps[3], 3)
    o.add_employee(emps[4], 104)
    d = create_department_salary_tree(o)
    assert size(d) == 4


# ignore these below, I thought they make it easier to write tests,
# but they make it harder to find where test failed
# nvm don't ignore them completely, I made some useful ones


def size(d: DepartmentSalaryTree) -> int:
    if d.department_name == '':
        return 0
    else:
        ans = 1
        for subdept in d.subdepartments:
            ans += size(subdept)
        return ans


def create_emp(n: int) -> Leader:
    return Employee(n, 'Name' + str(n), 'Job' + str(n), n * 100, 50)


def create_lead(n: int) -> Leader:
    return Leader(n, 'Name' + str(n), 'Job' + str(n), n * 1000, 50,
                  'Dept' + str(n))


def become_subs(subs: [Employee], e: Employee) -> None:
    for sub in subs:
        sub.become_subordinate(e)


def add_emps(org: Organization, emps: [Employee]) -> None:
    for emp in emps:
        org.add_employee(emp)


def create_emps(n: int) -> [Employee]:
    ans = []
    for i in range(1, n + 1):
        ans.append(Employee(100 + i, 'Name' + str(i), 'Job' + str(i),
                            i * 1000, 50))
    return ans


def test_create_emps() -> None:
    assert create_emps(5)[2].name == 'Name3'


def create_leaders(n: int) -> [Leader]:
    ans = []
    for i in range(1, n + 1):
        ans.append(Leader(i, 'Name' + str(i), 'Job' + str(i), i * 1000, 50,
                          'Department' + str(i)))
    return ans


if __name__ == '__main__':
    import pytest

    pytest.main(['test_5_and_6.py'])
