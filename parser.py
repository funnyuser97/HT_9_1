# program by Stupka Bogdan

###

import datetime
import argparse
import psycopg2
import logging
import config
import pickle
import json
import os
import csv
import re
from urllib import request

# for del tag in text area
pattern = r"<.+>.*<.+>"
pattern_show = r"(.|\n)*my_show.+>"
pattern_ask = r"(.|\n)*my_ask.+>"
pattern_job = r"(.|\n)*my_job.+>"
pattern_new = r"(.|\n)*my_new.+>"
new_row = '<tr>\n' + '<th>' + 'by' + '</th>\n' + '<th>' + 'descendants'
new_row += '</th>\n' + '<th>' + 'id' + '</th>\n' + '<th>' + 'kids'
new_row += '</th>\n' + '<th>' + 'score' + '</th>\n' + '<th>' + 'time'
new_row += '</th>\n' + '<th>' + 'text' + '</th>\n' + '<th>' + 'title'
new_row += '</th>\n' + '<th>' + 'parts' + '</th>\n' + '<th>' + 'type'
new_row += '</th>\n' + '<th>' + 'url' + '</th>' + '\n' + '</tr>\n'
create_table = ('''CREATE TABLE {catalog_name} (
                    id INTEGER,
                    by_record VARCHAR,
                    descendants VARCHAR,
                    id_site VARCHAR,
                    kids VARCHAR,
                    score VARCHAR,
                    time_record VARCHAR,
                    text_record VARCHAR,
                    title VARCHAR,
                    parts VARCHAR,
                    type_record VARCHAR,
                    url VARCHAR,                    
                    primary key (id)
                    );''')
add_record = ('''INSERT INTO {catalog_name} (id, by_record, descendants,
id_site, kids, score, time_record, text_record, title, parts, type_record, url) 
VALUES ({index}, '{by_record}', '{descendants}',
'{id_site}', '{kids}', '{score}', '{time_record}', '{text_record}', '{title}', '{parts}',
'{type_record}', '{url}'); ''')
select_table = ('''SELECT id, by_record, descendants,
id_site, kids, score, time_record, text_record, title, parts, type_record, url
FROM {};''')


class Parametrs(object):

    name_catalog = ''

    def __init__(self):
        log_format = "('%(asctime)s - %(name)s - %(levelname)s - %(message)s')"
        logging.basicConfig(filename=config.log_file_name, level=logging.INFO, format=log_format)
        logging.info('Program was started!')

        # This is copying html template from test.html, if file.html hasn`t
        # -----------------------------------------------------------
        count_file = 0
        for filename in os.listdir("."):
            if filename.endswith("html"):
                count_file += 1

        if count_file == 0:
            logging.info('Html has NOT in currently directory')
            read_file = open(config.template_file, 'r')
            template = read_file.read()
            read_file.close()

            write_file = open(config.genereta_html, 'w')
            write_file.write(template)
            write_file.close()
        else:
            logging.info('Html already has in currently directory')
        # -----------------------------------------------------------

        # UNcomment for clear log file
        # -----------------------------------------------------------
        # with open(config.log_file_name, 'w') as f:
        #     pass
        # -----------------------------------------------------------

    @staticmethod
    def received_parametrs():

        arg_parser = argparse.ArgumentParser(description='Great Description'
                                                         ' To Be Here')
        try:
            arg_parser.add_argument("-c", "--catalog", type=str,
                                    choices=config.choose_categoty,
                                    default=config.default_parametr,
                                    help="category for parsing")
        except Exception as i:
            logging.error("Error :", i)

        options = arg_parser.parse_args()
        logging.info('Parameters console received!')
        print("Parameters  console received!")

        Parametrs.name_catalog = options.catalog


class Catalog(object):

    def __init__(self, my_catalog):
        self.my_catalog = my_catalog

    def request_catalog(self):

        data = []

        print('Receive data of catalog...')
        my_catalog = self.my_catalog
        exp_url = config.url_category[:38] + my_catalog
        exp_url += config.url_category[38:]
        try:
            response = request.urlopen(exp_url)
            data = json.loads(response.read())
            print('ALL OK! All id category {} received!'.format(my_catalog))
            logging.info('OK!All id category {} received!'.format(my_catalog))
        except Exception as my_error:
            logging.error('This is an error message :', my_error)
            print('error :', my_error)
        return data

    def request_items(self, data):

        try:
            cursor.execute(create_table.format(catalog_name=self.my_catalog))
            print('Table was created!')
        except Exception as error3:
            print(error3)
            print('Table wasn`t created!')

        data_items = []

        print('Receive and add data for every id...')
        for i, item in enumerate(data):
            exp_url = config.url_id[:43] + str(item) + config.url_id[43:]
            try:
                response = request.urlopen(exp_url)
                data_dict = json.loads(response.read())

            except Exception as my_error:
                logging.error('This is an error message: {}'.format(my_error))
            else:
                # check keys in dictionary and insert empty string
                for key in config.columns:

                    try:
                        print(data_dict[key])
                    except Exception as error1:
                        print(str(error1) + "Doesn`t have this, key: {}".format(key))
                        data_dict[key] = ''

                try:
                    print(data_dict)
                    myline = str(
                        add_record.format(catalog_name=self.my_catalog, index=str(i), by_record=str(data_dict['by']),
                                          descendants=data_dict['descendants'], id_site=str(data_dict['id']),
                                          kids=str(data_dict['kids']), score=str(data_dict['score']),
                                          time_record=str(data_dict['time']), text_record=data_dict['text'],
                                          title=data_dict['title'], type_record=data_dict['type'],
                                          parts=data_dict['parts'], url=data_dict['url']))
                    print(myline)
                    cursor.execute(
                        add_record.format(catalog_name=self.my_catalog, index=str(i), by_record=str(data_dict['by']),
                                          descendants=data_dict['descendants'], id_site=str(data_dict['id']),
                                          kids=str(data_dict['kids']), score=str(data_dict['score']),
                                          time_record=str(data_dict['time']), text_record=data_dict['text'],
                                          title=data_dict['title'], type_record=data_dict['type'],
                                          parts=data_dict['parts'], url=data_dict['url']))

                    print('record add to DB')
                except Exception as error1:
                    print(error1)
                    print('record doesn`t add to DB')

                data_items.append(data_dict.copy())
                logging.info('Data of {}-th element received(add)'.format(i))

        return data_items

    @staticmethod
    def filter(data_items):
        print('Filtering data...')

        new_list_data = []

        for item in data_items:
            if config.score <= int(item['score']) and \
                            config.from_date <= int(item['time']):
                # clear tag in area "text"
                if 'text' in item.keys():
                    my_search = re.findall(pattern, item['text'])
                    if len(my_search) >= 1:
                        for dupl in my_search:
                            item['text'] = item['text'].replace(dupl, '')
                new_list_data.append(item.copy())

        print('Data is filtered out!')
        logging.info('Data is filtered out')

        return new_list_data

    @staticmethod
    def file_write(new_list_data):
        try:
            os.makedirs(config.name_dir)
            print('dir created')
        except OSError:
            print('dir already created')
        with open(config.file_report, "w", newline="") as file:
            logging.info('File report.csv created!')
            columns = ['by', 'descendants', 'id', 'kids', 'score', 'time',
                       'text', 'title', 'parts', 'type', 'url']
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            logging.info('Header write to file report.csv !')
            writer.writerows(new_list_data)
            logging.info('Data write to file report.csv !')

    def to_html(self):

        list_row = []
        list_id = []
        old_id = []
        id_header = 999999
        name_file = ''

        # This part for first start
        # ----------------------------------------------------------
        try:
            pickle_file = open('my_id.pickle', 'rb')
        except IOError as e:
            print(e, 'error open file: my_id.pickle')
            logging.info('has not file: my_id.pickle ')
        else:
            logging.info('Opening file and copy id: my_id.pickle ')
            print('Opening file and copy id')
            old_id = pickle.load(pickle_file)
            pickle_file.close()
            list_id = old_id.copy()
        # ----------------------------------------------------------
        # Next check and write record
        # ----------------------------------------------------------
        logging.info ('Reading DB')
        if id_header not in old_id:
            new_rowh = '<tr>\n' + '<th>' + 'by' + '</th>\n' + '<th>' + 'descendants'
            new_rowh += '</th>\n' + '<th>' + 'id' + '</th>\n' + '<th>' + 'kids'
            new_rowh += '</th>\n' + '<th>' + 'score' + '</th>\n' + '<th>' + 'time'
            new_rowh += '</th>\n' + '<th>' + 'text' + '</th>\n' + '<th>' + 'title'
            new_rowh += '</th>\n' + '<th>' + 'parts' + '</th>\n' + '<th>' + 'type'
            new_rowh += '</th>\n' + '<th>' + 'url' + '</th>' + '\n' + '</tr>\n'
            list_row.append (new_rowh)
            # this is saving id_header
            list_id.append (id_header)
        print(old_id)

        cursor.execute(select_table.format(self.my_catalog))
        rows = cursor.fetchall()

        count_add_records = 0
        logging.info ('Add record to html ')
        for row in rows:
            if row[3] not in old_id:
                new_row1 = '<tr>\n' + '<td>' + row[1] + '</td>\n' + '<td>'
                new_row1 += row[2] + '</td>\n' + '<td>'
                new_row1 += row[3] + '</td>\n' + '<td>' + row[4]
                new_row1 += '</td>\n' + '<td>' + row[5] + '</td>\n'
                new_row1 += '<td>' + row[6] + '</td>\n' + '<td>'
                new_row1 += row[7] + '</td>\n' + '<td>' + row[8]
                new_row1 += '</td>\n' + '<td>' + row[9] + '</td>\n'
                new_row1 += '<td>' + row[10] + '</td>\n' + '<td>'
                new_row1 += row[11] + '</td>' + '\n' + '</tr>\n'
                list_row.append (new_row1)
                count_add_records += 1
                list_id.append (row[3])
                logging.info ('Add record to html {}-th'.format (count_add_records))
        print (list_id)
        logging.info ('Adding records completed')

        # with open(config.file_report) as csvfile:
        #     logging.info('Reading csv file')
        #     reader = csv.DictReader(csvfile)
        #     if id_header not in old_id:
        #         new_rowh = '<tr>\n'+'<th>'+'by'+'</th>\n'+'<th>'+'descendants'
        #         new_rowh += '</th>\n'+'<th>'+'id'+'</th>\n'+'<th>'+'kids'
        #         new_rowh += '</th>\n'+'<th>'+'score'+'</th>\n'+'<th>'+'time'
        #         new_rowh += '</th>\n'+'<th>'+'text'+'</th>\n'+'<th>'+'title'
        #         new_rowh += '</th>\n'+'<th>'+'parts'+'</th>\n'+'<th>'+'type'
        #         new_rowh += '</th>\n'+'<th>'+'url'+'</th>'+'\n'+'</tr>\n'
        #         list_row.append(new_rowh)
        #         # this is saving id_header
        #         list_id.append(id_header)
        #     print(old_id)
        #
        #     count_add_records = 0
        #     logging.info('Add record to html ')
        #     for row in reader:
        #         if row[3] not in old_id:
        #             new_row1 = '<tr>\n'+'<td>'+row[1]+'</td>\n'+'<td>'
        #             new_row1 += row[2]+'</td>\n'+'<td>'
        #             new_row1 += row[3]+'</td>\n'+'<td>'+row[4]
        #             new_row1 += '</td>\n'+'<td>'+row[5]+'</td>\n'
        #             new_row1 += '<td>'+row[6]+'</td>\n'+'<td>'
        #             new_row1 += row[7]+'</td>\n'+'<td>'+row[8]
        #             new_row1 += '</td>\n'+'<td>'+row[9]+'</td>\n'
        #             new_row1 += '<td>'+row[10]+'</td>\n'+'<td>'
        #             new_row1 += row[11]+'</td>' + '\n'+'</tr>\n'
        #             list_row.append(new_row1)
        #             count_add_records += 1
        #             list_id.append(row[3])
        #             logging.info('Add record to html {}-th'.format(count_add_records))
        #     print(list_id)
        #     logging.info('Adding records completed')
        # ----------------------------------------------------------
        # saving id
        logging.info('Saving used is')
        with open('my_id.pickle', 'wb') as f:
            pickle.dump(list_id, f)

        # insert table with help regex
        print('Start generate html file ')
        logging.info('Start generate html file')
        template = ''

        logging.info('Search html files in current directory')
        for filename in os.listdir("."):
            if filename.endswith("html"):
                read_file = open(filename, 'r')
                template = read_file.read()
                read_file.close()
                name_file = filename

        logging.info('Find place insert')
        if self.my_catalog == 'jobstories':
            last_index = len(re.match(pattern_job, template).group())
        elif self.my_catalog == 'showstories':
            last_index = len(re.match(pattern_show, template).group())
        elif self.my_catalog == 'askstories':
            last_index = len(re.match(pattern_ask, template).group())
        elif self.my_catalog == 'newstories':
            last_index = len(re.match(pattern_new, template).group())
        else:
            last_index = 0

        new_table = ''

        logging.info('Start generate new html file')
        for item in list_row:
            new_table += item
        new_html = template[:last_index] + new_table + template[last_index:]

        logging.info('Saving html file')
        write_file = open(name_file, 'w')
        write_file.write(new_html)
        write_file.close()

        # just rename file html
        print('Start generate html file ')
        logging.info('Rename html file')
        str_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for filename in os.listdir("."):
            if filename.endswith("html"):
                os.rename(filename, 'file_'+str_time+'.html')


if __name__ == "__main__":

    # receiving parameters for parsing
    catalogs = Parametrs()
    catalogs.received_parametrs()
    str_catalog = catalogs.name_catalog

    try:
        connection = psycopg2.connect("dbname='postgres'"
                                      " user='postgres' "
                                      "password='54705b' "
                                      "host='localhost' "
                                      "port='5432'")
        connection.autocommit = True
        cursor = connection.cursor()
        print('Connect TRUE')
    except Exception as error:
        print("Doesn`t connect to DB!!!\n" + str(error))
        cursor = None
        connection = None

    # parsing for every catalog
    if str_catalog == 'all':
        for catalog_name in config.choose_categoty[:-1]:
            first = Catalog(catalog_name)
            data_m = first.request_catalog()
            data_list_m = first.request_items(data_m)
            logging.info('Data of every id {} received!'.format(first.my_catalog))
            print('Data of every id the category {}'
                  ' received!'.format(first.my_catalog))
            new_list_data_m = first.filter(data_list_m)
            print('Write data to file...')
            first.file_write(new_list_data_m)
            print('ALL OK! Data recorded')
            first.to_html()
    else:
        first = Catalog(str_catalog)
        data_m = first.request_catalog()
        data_list_m = first.request_items(data_m)
        logging.info('Data of every id {} received!'.format(first.my_catalog))
        print('Data of every id the category {}'
              ' received!'.format(first.my_catalog))
        new_list_data_m = first.filter(data_list_m)
        print('Write data to file...')
        first.file_write(new_list_data_m)
        print('ALL OK! Data recorded')
        first.to_html()

    try:
        cursor.close()
        connection.close()
    except Exception as error2:
        print(error2)
