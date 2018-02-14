import sqlite3

# create database
conn = sqlite3.connect('schedule.db')

# define cursor
c = conn.cursor()


# create tables
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS pill_module1('
              'id REAL,'
              'user_id REAL,'
              'pill_name TEXT,'
              'module_num INTEGER)'
              )
    c.execute('CREATE TABLE IF NOT EXISTS pill_module2('
              'id REAL,'
              'user_id REAL,'
              'pill_name TEXT,'
              'module_num INTEGER)'
              )
    c.execute('CREATE TABLE IF NOT EXISTS pill_module3('
              'id REAL,'
              'user_id REAL,'
              'pill_name TEXT,'
              'module_num INTEGER)'
              )
    c.execute('CREATE TABLE IF NOT EXISTS schedulerPM1('
              'id REAL,'
              'category TEXT,'
              'day TEXT,'
              'time TEXT,'
              'counter INTEGER,'
              'module_nums ARRAY OF INTEGERS,'
              'user_id REAL)'
              )
    c.execute('CREATE TABLE IF NOT EXISTS schedulerPM2('
              'id REAL,'
              'category TEXT,'
              'day TEXT,'
              'time TEXT,'
              'counter INTEGER,'
              'module_nums ARRAY OF INTEGERS,'
              'user_id REAL)'
              )
    c.execute('CREATE TABLE IF NOT EXISTS schedulerPM3('
              'id REAL,'
              'category TEXT,'
              'day TEXT,'
              'time TEXT,'
              'counter INTEGER,'
              'module_nums ARRAY OF INTEGERS,'
              'user_id REAL)'
              )


# test input data into database
def data_entry():
    c.execute("INSERT INTO pill_module VALUES(123, 456, 'Sunshine', 1)")
    c.execute("INSERT INTO pill_module2 VALUES(789, 876, 'Coffee', 2)")
    c.execute("INSERT INTO pill_module3 VALUES(543, 210, 'Happiness', 3)")
    c.execute("INSERT INTO TABLE schedulerPM1 VALUES(000, 'day', 'Monday', '10:30', 0, [1,2,3], 123)")
    c.execute("INSERT INTO TABLE schedulerPM2 VALUES(000, 'minute', 'Tuesday', '10:30', 0, [1,2,3], 123)")
    c.execute("INSERT INTO TABLE schedulerPM3 VALUES(000, 'hour', 'Wednesday', '10:30', 0, [1,2,3], 123)")
    conn.commit()
    c.close()
    conn.close()


# actual input data
# def data_entry():
#    c.execute('INSERT INTO pill_module1 VALUES()')
#    c.execute('INSERT INTO pill_module2 VALUES()')
#    c.execute('INSERT INTO pill_module3 VALUES()')
#    c.execute('INSERT INTO TABLE schedulerPM1 VALUES()')
#    c.execute('INSERT INTO TABLE schedulerPM2 VALUES()')
#    c.execute('INSERT INTO TABLE schedulerPM3 VALUES()')
#    conn.commit()
#    c.close()
#    conn.close()

create_table()
data_entry()

