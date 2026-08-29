from views.tables_view import TablesView


def test_next_table_number_after_existing_tables():
    assert TablesView._next_table_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 11


def test_next_table_number_when_no_tables_exist():
    assert TablesView._next_table_number([]) == 1
