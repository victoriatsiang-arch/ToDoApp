from datetime import datetime
from todo import add, update, next 


def test_add_t1():
    add(("Math 135 HW", "Schoolwork", datetime(2025, 9, 20), datetime(2025, 9, datetime.now().day+3), datetime(2025, 9, 20)))
    add(("se101 HW", "Schoolwork", datetime(2025, 9, 20), datetime(2025, 9, datetime.now().day), datetime(2025, 9, 20)))
    assert add(("Math 135 HW", "Schoolwork", datetime(2025, 9, 20), datetime(2025, 9, datetime.now().day+3), datetime(2025, 9, 20))) == "Task already there!"

def test_update_t1():
    assert update(("Math 135 HW", "Schoolwork", datetime(2025, 9, 20), datetime(2025, 9, datetime.now().day+1), datetime(2025, 9, 20))) == "update successful"

def test_next_t1():
    assert next() == ('se101 HW', 'Schoolwork', datetime(2025, 9, 20, 0, 0), datetime(2025, 9, 27, 0, 0), datetime(2025, 9, 20, 0, 0), 27)

def test_next_t2():
    assert update(('invalid', 'Schoolwork', datetime(2025, 9, 20, 0, 0), datetime(2025, 9, 27, 0, 0), datetime(2025, 9, 20, 0, 0), 27)) == "update unsuccessful"
    

