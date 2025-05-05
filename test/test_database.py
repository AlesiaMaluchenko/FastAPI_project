import sqlite3

def test_db_create(test_database_file, cmd):
    connection = sqlite3.connect(test_database_file)
    cursor = connection.cursor()

    cursor.executescript(cmd)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    test_database_file = 'test_database.sqlite3'
    create_file = 'test_database.sql'

    test_cmd = None
    with open(create_file, 'r') as cmdf:
        test_cmd = cmdf.read()


    test_db_create(test_database_file, test_cmd)
