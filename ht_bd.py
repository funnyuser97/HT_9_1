import psycopg2

# connection to DB

try:
    connection = psycopg2.connect("dbname='postgres'"
                                  " user='postgres' "
                                  "password='54705b' "
                                  "host='localhost' "
                                  "port='5432'")
    connection.autocommit = True
    cursor = connection.cursor()
    print(type(cursor))
except:
    print("Dosen`t connect to DB!!!")


# create_table= ('''CREATE TABLE  (
#                     id INTEGER,
#                     name VARCHAR,
#                     make VARCHAR,
#                     model VARCHAR,
#                     year DATE,
#                     primary key (id)
#                     );''')
drop_table_name = ("DROP TABLE job")
add_record_table = ('''INSERT INTO table_name 
VALUES (2, 'Marly', 'Ford', 'Explorer', '2000-01-01'); ''')
update_record_table = ('''UPDATE table_name
SET name='Chevrolet'
WHERE id=1;''')
select_table = ('''SELECT by_record, id, id_site 
FROM jobstories;''')
delete_records_table = ('''DELETE FROM table_name
WHERE name='Ford';''')
add_record = ('''INSERT INTO {catalog_name} (id, by_record, descendants,
id_site, kids, score, time_record, text_record, title, parts, type_record, url) 
VALUES ({id}, '{by_record}', '{descendants}',
'{id_site}', '{kids}', '{score}', '{time_record}', '{text_record}', '{title}', '{parts}',
'{type_record}', '{url}'); ''')

# print (add_record.format(catalog_name=self.my_catalog, id=i, by_record=data_dict['by'],
#                           descendants=data_dict['descendants'], id_site=data_dict['id_site'], kids=data_dict['kids'],
#                           score=data_dict['score'], time_record=data_dict['time'], text_record=data_dict['text'],
#                           title=data_dict['title'], type_record=data_dict['type'], parts=data_dict['parts'],
#                           url=data_dict['url']))
# myline = str(add_record.format (catalog_name='jobstories', id=2, by_record='2',
#                           descendants='descendants', id_site='id_site', kids='kids',
#                           score='score', time_record='time', text_record='text',
#                           title='title', type_record='type', parts='parts', url='url'))
# print(myline)
cursor.execute (select_table)
rows = cursor.fetchall()
for row in rows:
    print(row[2])



cursor.close()
connection.close()

#
# class DbConnection(object):(id serial PRIMARY KEY, name varchar(100))
#
#     def __init__(self):
#         try:
#             self.connection = psycopg2.connect("dbname='postgres'"
#                         " user='postgres' "
#                         "password='54705b' "
#                         "host='localhost' "
#                         "port='5432'")
#             self.connection.autocommit = True
#             self.cursor = self.connection.cursor()
#         except:
#             print("Dosen`t connect to DB!!!")
#
#     def create_table(self):
#         create_table_name = ("DROP TABLE job")
#         self.cursor.execute(create_table_name)
#
#
# if __name__ == '__main__':
#     database_connection = DbConnection()
#     database_connection.create_table()
#
