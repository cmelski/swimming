import datetime

import matplotlib
from flask import (Flask, abort, render_template, redirect, url_for, flash,
                   request, jsonify)
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import json
import os

matplotlib.use('agg')

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dsfds'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


def format_apostrophe(data):
    if "'" in data:
        data = data.replace("'", "''")

    return data


def format_time(data):
    formatted_time = data.split(':')
    time_data = (float(formatted_time[0]) * 60) + float(formatted_time[1])
    return time_data


def format_time_colon(data):
    first_number = float(str(data).split('.')[0]) / 60
    first_number = str(first_number)[0]
    second_number = str(int(float(str(data).split('.')[0]) - (float(first_number) * 60)))
    third_number = str(data).split(".")[1]
    if len(third_number) == 1:
        third_number = third_number + '0'

    if float(second_number) < 10:
        second_number = '0' + second_number

    third_number = '0' + '.' + third_number

    third_number = f'{float(third_number):.2f}'

    sec_third = str(second_number) + '.' + str(third_number).split('.')[1]

    formatted_time = first_number + ':' + str(sec_third)

    return formatted_time


def format_chart(dates, results, ax):
    for i, j in zip(dates, results):
        # print(i)
        formatted_j = str(j).split('.')
        print(formatted_j)
        first_number = int(formatted_j[0]) / 60
        # print(first_number)
        second_number = str(first_number).split('.')[1]
        print(second_number)
        second_number = '0.' + second_number
        print(second_number)
        second_number = float(second_number) * 60
        second_number = round(second_number, 0)
        print(second_number)
        first_number = str(first_number)[0]
        print(first_number)

        if '.0' in str(second_number):
            second_number = str(second_number).replace('.0', '')
        if len(str(second_number)) == 1:
            second_number = '0' + str(second_number)
        if len(str(second_number)) > 2:
            print(second_number)
            second_number = second_number[0:2]
        print(second_number)
        third_number = formatted_j[1]
        if len(third_number) == 1:
            third_number = third_number + '0'
        print(third_number)
        if int(formatted_j[0]) >= 60:
            j_label = first_number + ':' + str(second_number) + '.' + third_number
            ax.annotate(str(j_label), xy=(i, j))
        else:
            ax.annotate(str(j), xy=(i, j))


def get_50_chart(mylist):
    result_list = []
    dates = []
    for data in mylist:
        if data[3] == 50:
            if ':' in data[4]:
                formatted_time = data[4].split(':')
                # print(formatted_time)
                time_data = (float(formatted_time[0]) * 60) + float(formatted_time[1])
                # print(time_data)
                result_list.append(float(time_data))
                # print(result_list)
            else:
                result_list.append(float(data[4]))
            date_object = dt.datetime.strptime(data[10], "%Y")
            date = date_object.year
            dates.append(date)

    s = pd.Series(result_list, dates)
    fig, ax = plt.subplots()
    plt.xlabel("Year")
    plt.ylabel("Times")
    plt.title("50m Results")
    plt.legend()
    if len(result_list) > 0:
        s.plot.line()
        for i, j in zip(dates, result_list):
            # print(i)
            formatted_j = str(j).split('.')
            # print(formatted_j)
            if len(formatted_j[0]) > 2:
                formatted_j[0] = formatted_j[0].replace(formatted_j[0],
                                                        str((int(formatted_j[0][0]) + int('00')) / 60) + ':' +
                                                        formatted_j[0][1:3])
                # print(formatted_j)
            ax.annotate(str(j), xy=(i, j))
        fig.savefig('static/images/50_chart.png')


def get_100_chart(mylist):
    result_list = []
    dates = []
    for data in mylist:
        if data[3] == 100:
            if ':' in data[4]:
                formatted_time = data[4].split(':')
                # print(formatted_time)
                time_data = (float(formatted_time[0]) * 60) + float(formatted_time[1])
                # print(time_data)
                result_list.append(float(time_data))
                # print(result_list)
            else:
                result_list.append(float(data[4]))
            date_object = dt.datetime.strptime(data[10], "%Y")
            date = date_object.year
            dates.append(date)

    s = pd.Series(result_list, dates)
    fig, ax = plt.subplots()
    plt.xlabel("Year")
    plt.ylabel("Times")
    plt.title("100m Results")
    if len(result_list) > 0:
        s.plot.line()
        for i, j in zip(dates, result_list):
            # print(i)
            formatted_j = str(j).split('.')
            # print(formatted_j)
            if len(formatted_j[0]) > 2:
                formatted_j[0] = formatted_j[0].replace(formatted_j[0],
                                                        str((int(formatted_j[0][0]) + int('00')) / 60) + ':' +
                                                        formatted_j[0][1:3])
                # print(formatted_j)
            ax.annotate(str(j), xy=(i, j))
        fig.savefig('static/images/100_chart.png')


def get_combined_chart(mylist):
    result_list_25 = []
    result_list_50 = []
    result_list_100 = []
    result_list_200 = []
    result_list_400 = []
    dates_25 = []
    dates_50 = []
    dates_100 = []
    dates_200 = []
    dates_400 = []
    print(mylist)

    for data in mylist:
        if data[3] == 25:
            if ':' in data[4]:
                time_data = format_time(data[4])
                result_list_25.append(float(time_data))
            else:
                result_list_25.append(float(data[4]))

            date_object = dt.datetime.strptime(data[10], "%Y-%m-%d")
            dates_25.append(date_object)

        if data[3] == 50:
            if ':' in data[4]:

                time_data = format_time(data[4])
                result_list_50.append(float(time_data))
            else:
                result_list_50.append(float(data[4]))

            date_object = dt.datetime.strptime(data[10], "%Y-%m-%d")
            dates_50.append(date_object)

        if data[3] == 100:
            if ':' in data[4]:
                time_data = format_time(data[4])
                result_list_100.append(float(time_data))
            else:
                result_list_100.append(float(data[4]))

            date_object = dt.datetime.strptime(data[10], "%Y-%m-%d")
            dates_100.append(date_object)

        if data[3] == 200:
            if ':' in data[4]:
                time_data = format_time(data[4])
                result_list_200.append(float(time_data))
            else:
                result_list_200.append(float(data[4]))

            date_object = dt.datetime.strptime(data[10], "%Y-%m-%d")
            dates_200.append(date_object)

        if data[3] == 400:
            if ':' in data[4]:
                time_data = format_time(data[4])
                result_list_400.append(float(time_data))
            else:
                result_list_400.append(float(data[4]))

            date_object = dt.datetime.strptime(data[10], "%Y-%m-%d")
            dates_400.append(date_object)

    s = pd.Series(result_list_25, dates_25)
    t = pd.Series(result_list_50, dates_50)
    u = pd.Series(result_list_100, dates_100)
    v = pd.Series(result_list_200, dates_200)
    w = pd.Series(result_list_400, dates_400)
    fig, ax = plt.subplots()
    ax.legend()
    plt.xlabel("Date")
    plt.ylabel("Times(seconds)")
    plt.title(f"{mylist[0][2]} Results")

    if len(result_list_25) > 1:
        diff = max(result_list_25) - min(result_list_25)
        diff = f'{diff:.2f}'
        s.plot.line(label=f'25m: -{diff}')
        ax.legend()
        for i, j in zip(dates_25, result_list_25):
            formatted_j = str(j).split('.')
            if len(formatted_j[0]) > 2:
                formatted_j[0] = formatted_j[0].replace(formatted_j[0],
                                                        str((int(formatted_j[0][0]) + int('00')) / 60) + ':' +
                                                        formatted_j[0][1:3])

            ax.annotate(str(j), xy=(i, j))

    if len(result_list_50) > 1:
        diff = max(result_list_50) - min(result_list_50)
        diff = f'{diff:.2f}'
        t.plot.line(label=f'50m: -{diff}')
        ax.legend()
        for i, j in zip(dates_50, result_list_50):
            formatted_j = str(j).split('.')
            if len(formatted_j[0]) > 2:
                formatted_j[0] = formatted_j[0].replace(formatted_j[0],
                                                        str((int(formatted_j[0][0]) + int('00')) / 60) + ':' +
                                                        formatted_j[0][1:3])

            ax.annotate(str(j), xy=(i, j))

    if len(result_list_100) > 1:
        diff = max(result_list_100) - min(result_list_100)
        diff = f'{diff:.2f}'
        u.plot.line(label=f'100m: -{diff}')
        ax.legend()
        format_chart(dates_100, result_list_100, ax)

    if len(result_list_200) > 1:
        diff = max(result_list_200) - min(result_list_200)
        diff = f'{diff:.2f}'
        v.plot.line(label=f'200m: -{diff}')
        ax.legend()
        format_chart(dates_200, result_list_200, ax)

    if len(result_list_400) > 1:
        diff = max(result_list_400) - min(result_list_400)
        diff = f'{diff:.2f}'
        w.plot.line(label=f'400m: -{diff}')
        ax.legend()
        format_chart(dates_400, result_list_400, ax)

    fig.savefig('static/images/combined_chart.png')


class DBConnect:
    def __init__(self):
        # self.connection = psycopg2.connect(database="swimming", user="postgres", password="password",
        # host="localhost", port=5433)

        # self.cursor = self.connection.cursor()

        self.connection = psycopg2.connect(database="swimming2", user=os.environ.get('DB_USER'),
                                           password=os.environ.get('DB_PASSWORD'),
                                           host="localhost", port=5433)

        self.cursor = self.connection.cursor()


def create_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",  # Connect to the default 'postgres' database first
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=5433
        )
        conn.autocommit = True  # Set autocommit to True
        cur = conn.cursor()

        cur.execute("CREATE DATABASE swimming2;")
        print("Database created successfully!")

        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Duplicate DB: {e}")


create_db()


def create_table():
    conn = psycopg2.connect(database="swimming2", user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASSWORD'),
                            host="localhost", port=5433)
    print('connected')
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("""
        CREATE TABLE competition (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            team VARCHAR(50) NOT NULL,
            location VARCHAR(50) NOT NULL,
            year VARCHAR(50) NOT NULL
        )
        """)
    cur.execute("""
            CREATE TABLE event (
                id SERIAL PRIMARY KEY,
                stroke VARCHAR(50) NOT NULL
            )
            """)

    cur.execute("""
            CREATE TABLE swimmer (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL
            )
            """)

    cur.execute("""
            CREATE TABLE results (
                swimmer_id BIGINT NOT NULL,
                competition_id BIGINT NOT NULL,
                event_id BIGINT NOT NULL,
                distance BIGINT NOT NULL,
                age VARCHAR(50) NOT NULL,
                place VARCHAR(50) NOT NULL,
                time VARCHAR(50) NOT NULL
            )
            """)

    cur.close()
    conn.close()


create_table()


def get_swimmers():
    con = DBConnect()
    con.cursor.execute('SELECT * from swimmer')
    swimmer_data = con.cursor.fetchall()
    con.cursor.close()
    return swimmer_data


def get_competitions():
    con = DBConnect()
    con.cursor.execute('SELECT * from competition')
    competitions = con.cursor.fetchall()
    con.cursor.close()
    return competitions


def get_events():
    con = DBConnect()
    con.cursor.execute('SELECT * from event')
    events = con.cursor.fetchall()
    con.cursor.close()
    return events


def get_results():
    con = DBConnect()
    con.cursor.execute('SELECT * from results')
    results = con.cursor.fetchall()
    con.cursor.close()
    return results


def migrate_data():
    # swimmers = get_swimmers()
    # competitions = get_competitions()
    # events = get_events()
    # results = get_results()
    # print(swimmers)
    # # Sample data
    # swimmer_data = {
    #     'id': [item[0] for item in swimmers],
    #     'first_name': [item[1] for item in swimmers],
    #     'last_name': [item[2] for item in swimmers]
    # }
    #
    #
    # # Create a DataFrame
    # df = pd.DataFrame(swimmer_data)
    #
    # # Specify the file path
    # file_path = 'swimmers.csv'
    #
    # # Write the DataFrame to a CSV file
    # df.to_csv(file_path, index=False)
    #
    # # use json
    # json_object = json.dumps(swimmer_data, indent=4)
    #
    # # Writing to sample.json
    # with open("swimmers.json", "w") as outfile:
    #     outfile.write(json_object)

    with open('swimmers.json', 'r') as openfile:
        json_object = json.load(openfile)

    conn = psycopg2.connect(database="swimming2", user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PASSWORD'),
                            host="localhost", port=5433)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM swimmer LIMIT 0')
    column_names = [desc[0] for desc in cur.description]

    for i in range(0, len(json_object['id'])):
        insert = f"INSERT INTO swimmer ({column_names[0]}, {column_names[1]}," \
                 f"{column_names[2]})" \
                 f" VALUES('{json_object['id'][i]}','{json_object['first_name'][i]}', '{json_object['last_name'][i]}');"

        cur.execute(insert)

    # for swimmer in swimmers:
    #     insert = f"INSERT INTO swimmer ({column_names[0]}, {column_names[1]}," \
    #              f"{column_names[2]})" \
    #              f" VALUES('{swimmer[0]}','{swimmer[1]}', '{swimmer[2]}');"
    #
    #     cur.execute(insert)
    #
    # cur.execute(f'SELECT * FROM competition LIMIT 0')
    # column_names = [desc[0] for desc in cur.description]
    # for comp in competitions:
    #     insert = f"INSERT INTO competition ({column_names[0]}, {column_names[1]}," \
    #              f"{column_names[2]}, {column_names[3]}, {column_names[4]})" \
    #              f" VALUES('{comp[0]}','{format_apostrophe(comp[1])}', '{comp[2]}', '{comp[3]}', '{comp[4]}');"
    #
    #     cur.execute(insert)
    #
    # cur.execute(f'SELECT * FROM event LIMIT 0')
    # column_names = [desc[0] for desc in cur.description]
    # for event in events:
    #     insert = f"INSERT INTO event ({column_names[0]}, {column_names[1]})" \
    #              f" VALUES('{event[0]}','{event[1]}');"
    #
    #     cur.execute(insert)
    #
    # cur.execute(f'SELECT * FROM results LIMIT 0')
    # column_names = [desc[0] for desc in cur.description]
    # for result in results:
    #     insert = f"INSERT INTO results ({column_names[0]}, {column_names[1]}," \
    #              f"{column_names[2]}, {column_names[3]}, {column_names[4]}, {column_names[5]}, {column_names[6]})" \
    #              f" VALUES('{result[0]}','{result[1]}', '{result[2]}', '{result[3]}', '{result[4]}', '{result[5]}', '{result[6]}');"
    #     cur.execute(insert)
    #
    cur.close()


# migrate_data()


def get_swimmers_by_event(event_id):
    con = DBConnect()
    con.cursor.execute(f'select distinct(a.id),a.first_name,a.last_name '
                       f'from swimmer a, results b '
                       f'where b.event_id = {event_id} '
                       f'and a.id = b.swimmer_id;')
    swimmer_data = con.cursor.fetchall()
    con.cursor.close()
    return swimmer_data


def get_results_by_event_by_swimmer(event_id, swimmer_id):
    con = DBConnect()
    con.cursor.execute(f'select d.first_name, d.last_name, c. stroke, a.distance, a.time, a.place, a.age, '
                       f'b.name, b. team, b.location, b.year '
                       f'from results a, competition b, event c, swimmer d '
                       f'where a.competition_id = b.id '
                       f'and a.event_id = c.id '
                       f'and a.swimmer_id = d.id '
                       f'and a.swimmer_id = {swimmer_id} '
                       f'and a.event_id = {event_id} '
                       f'order by a.distance, b.year desc;')
    results_data = con.cursor.fetchall()
    con.cursor.close()
    get_combined_chart(results_data)
    return results_data


def format_date(date_string):
    format_string = "%Y-%m-%d"
    datetime_object = dt.datetime.strptime(date_string, format_string)
    datetime_object = datetime_object.strftime("%b %Y")
    return datetime_object


def get_pbs_compare(swimmer1, swimmer2, swimmer1_id, swimmer2_id):
    con = DBConnect()
    compare_dict = dict()
    compare_dict['pbs'] = [{f'{swimmer1}': {'Freestyle': {25: ('', '', '', ''),
                                                          50: ('', '', '', ''),
                                                          100: ('', '', '', ''),
                                                          200: ('', '', '', ''),
                                                          400: ('', '', '', ''),
                                                          },
                                            'Fly': {25: ('', '', '', ''),
                                                    50: ('', '', '', ''),
                                                    100: ('', '', '', ''),
                                                    200: ('', '', '', ''),
                                                    400: ('', '', '', ''),
                                                    },
                                            'Breast': {25: ('', '', '', ''),
                                                       50: ('', '', '', ''),
                                                       100: ('', '', '', ''),
                                                       200: ('', '', '', ''),
                                                       400: ('', '', '', ''),
                                                       },
                                            'Back': {25: ('', '', '', ''),
                                                     50: ('', '', '', ''),
                                                     100: ('', '', '', ''),
                                                     200: ('', '', '', ''),
                                                     400: ('', '', '', ''),
                                                     }
                                            }
                            },
                           {f'{swimmer2}': {'Freestyle': {25: ('', '', '', ''),
                                                          50: ('', '', '', ''),
                                                          100: ('', '', '', ''),
                                                          200: ('', '', '', ''),
                                                          400: ('', '', '', ''),
                                                          },
                                            'Fly': {25: ('', '', '', ''),
                                                    50: ('', '', '', ''),
                                                    100: ('', '', '', ''),
                                                    200: ('', '', '', ''),
                                                    400: ('', '', '', ''),
                                                    },
                                            'Breast': {25: ('', '', '', ''),
                                                       50: ('', '', '', ''),
                                                       100: ('', '', '', ''),
                                                       200: ('', '', '', ''),
                                                       400: ('', '', '', ''),
                                                       },
                                            'Back': {25: ('', '', '', ''),
                                                     50: ('', '', '', ''),
                                                     100: ('', '', '', ''),
                                                     200: ('', '', '', ''),
                                                     400: ('', '', '', ''),
                                                     }
                                            }
                            }
                           ]
    events = get_events()
    for event in events:
        con.cursor.execute(f'select a.time, a.distance, b.name, b.year '
                           f'from results a '
                           f'JOIN competition b '
                           f'ON a.competition_id = b.id '
                           f'where a.time IN '
                           f'(select min(a.time) from results a '
                           f'where event_id = {event[0]} '
                           f'and swimmer_id = {swimmer1_id} '
                           f'Group by a.distance)'
                           f'Order by a.distance;')
        stroke = event[1]
        results_data_swimmer1 = con.cursor.fetchall()
        print(results_data_swimmer1)
        if len(results_data_swimmer1) > 0:
            for data in results_data_swimmer1:
                compare_dict['pbs'][0][swimmer1][stroke][data[1]] = data
        con.cursor.execute(f'select a.time, a.distance, b.name, b.year '
                           f'from results a '
                           f'JOIN competition b '
                           f'ON a.competition_id = b.id '
                           f'where a.time IN '
                           f'(select min(a.time) from results a '
                           f'where event_id = {event[0]} '
                           f'and swimmer_id = {swimmer2_id} '
                           f'Group by a.distance)'
                           f'Order by a.distance;')
        results_data_swimmer2 = con.cursor.fetchall()
        print(results_data_swimmer2)
        if len(results_data_swimmer2) > 0:
            for data in results_data_swimmer2:
                compare_dict['pbs'][1][swimmer2][stroke][data[1]] = data

    # print(compare_dict)
    return compare_dict


def get_pbs(swimmer_id):
    events = get_events()
    con = DBConnect()
    times = dict()

    for event in events:
        # con.cursor.execute(f'select time, distance '
        #                    f'from results  '
        #                    f'where event_id = {event[0]} '
        #                    f'and swimmer_id = {swimmer_id};')

        con.cursor.execute(f'select results.time, results.distance, competition.name, competition.year '
                           f'from results  '
                           f'JOIN competition '
                           f'ON competition.id = results.competition_id '
                           f'where results.event_id = {event[0]} '
                           f'and results.swimmer_id = {swimmer_id};')
        stroke = event[1]
        results_data = con.cursor.fetchall()
        print(results_data)
        for result in results_data:
            if len(result) > 0:

                times[f'{stroke} - 25m'] = [(float(result[0]), result[2], format_date(result[3])) for result in
                                            results_data if result[1] == 25]
                if len(times[f'{stroke} - 25m']) > 0:
                    times[f'{stroke} - 25m'] = min(times[f'{stroke} - 25m'])
                else:
                    times[f'{stroke} - 25m'] = ''

                times[f'{stroke} - 50m'] = [(float(result[0]), result[2], format_date(result[3])) for result in
                                            results_data if result[1] == 50]
                if len(times[f'{stroke} - 50m']) > 0:
                    times[f'{stroke} - 50m'] = min(times[f'{stroke} - 50m'])
                else:
                    times[f'{stroke} - 50m'] = ''

                times[f'{stroke} - 100m'] = [[result[0], result[2], format_date(result[3])] for result in results_data
                                             if result[1] == 100]

                if len(times[f'{stroke} - 100m']) > 0:
                    for i in range(0, len(times[f'{stroke} - 100m'])):
                        if ':' in times[f'{stroke} - 100m'][i][0]:
                            times[f'{stroke} - 100m'][i][0] = float(format_time(str(times[f'{stroke} - 100m'][i][0])))
                        else:
                            times[f'{stroke} - 100m'][i][0] = float(times[f'{stroke} - 100m'][i][0])

                    times[f'{stroke} - 100m'] = min(times[f'{stroke} - 100m'])

                    if times[f'{stroke} - 100m'][0] >= 60:
                        times[f'{stroke} - 100m'][0] = format_time_colon(times[f'{stroke} - 100m'][0])
                else:
                    times[f'{stroke} - 100m'] = ''

                times[f'{stroke} - 200m'] = [[result[0], result[2], format_date(result[3])] for result in results_data
                                             if result[1] == 200]
                if len(times[f'{stroke} - 200m']) > 0:
                    for i in range(0, len(times[f'{stroke} - 200m'])):
                        if ':' in times[f'{stroke} - 200m'][i][0]:
                            times[f'{stroke} - 200m'][i][0] = float(format_time(str(times[f'{stroke} - 200m'][i][0])))
                        else:
                            times[f'{stroke} - 200m'][i][0] = float(times[f'{stroke} - 200m'][i][0])
                    times[f'{stroke} - 200m'] = min(times[f'{stroke} - 200m'])
                    if times[f'{stroke} - 200m'][0] >= 60:
                        times[f'{stroke} - 200m'][0] = format_time_colon(times[f'{stroke} - 200m'][0])
                else:
                    times[f'{stroke} - 200m'] = ''

                times[f'{stroke} - 400m'] = [[result[0], result[2], format_date(result[3])] for result in results_data
                                             if result[1] == 400]
                if len(times[f'{stroke} - 400m']) > 0:
                    for i in range(0, len(times[f'{stroke} - 400m'])):
                        if ':' in times[f'{stroke} - 400m'][i][0]:
                            times[f'{stroke} - 400m'][i][0] = float(format_time(str(times[f'{stroke} - 400m'][i][0])))
                        else:
                            times[f'{stroke} - 400m'][i][0] = float(times[f'{stroke} - 400m'][i][0])
                    times[f'{stroke} - 400m'] = min(times[f'{stroke} - 400m'])
                    if times[f'{stroke} - 400m'][0] >= 60:
                        times[f'{stroke} - 400m'][0] = format_time_colon(times[f'{stroke} - 400m'][0])
                else:
                    times[f'{stroke} - 400m'] = ''

    con.cursor.close()
    freestyle = []
    back = []
    breast = []
    fly = []

    for k, v in times.items():
        if 'Freestyle' in k:
            freestyle.append(v)
        if 'Back' in k:
            back.append(v)
        if 'Breast' in k:
            breast.append(v)
        if 'Fly' in k:
            fly.append(v)

    times_dict = dict()
    times_dict['Freestyle'] = freestyle
    times_dict['Back'] = back
    times_dict['Breast'] = breast
    times_dict['Fly'] = fly

    for key in times_dict.keys():
        for k, v in times_dict.items():
            if k == key:
                print(v)

    return times_dict


class AddSwimmer(FlaskForm):
    first_name = StringField(validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    submit = SubmitField("Add Swimmer")


class AddCompetition(FlaskForm):
    competition_name = StringField(label='Competition Name:', validators=[DataRequired()],
                                   render_kw={"placeholder": "Competition Name"})
    team = SelectField(label='Team:', choices=[('GEMS', 'GEMS'), ('Nexus', 'Nexus'), ('Dorados', 'Dorados')],
                       render_kw={"placeholder": "Team"})
    location = StringField(label='Location:', validators=[DataRequired()], render_kw={"placeholder": "Location"})
    year = DateField(label='Year:', validators=[DataRequired()], render_kw={"placeholder": "Year"})
    submit = SubmitField("Add Competition")


class AddEvent(FlaskForm):
    stroke = StringField(label='Event Name:', validators=[DataRequired()],
                         render_kw={"placeholder": "Event Name"})

    submit = SubmitField("Add Event")


class AddResults(FlaskForm):
    swimmer_names = SelectField('Swimmer_Names', coerce=str)
    competition_names = SelectField(u'Comp_Names', coerce=str)
    event_names = SelectField(u'Event_Names', coerce=str)
    distance = SelectField(label='Distance:',
                           choices=[(25, 25), (50, 50), (100, 100), (200, 200), (400, 400), (800, 800)],
                           render_kw={"placeholder": "Distance"})

    time = StringField(label='Time:', validators=[DataRequired()], render_kw={"placeholder": "Time"})
    place = StringField(label='Place:', validators=[DataRequired()], render_kw={"placeholder": "Place"})
    age = StringField(label='Age:', validators=[DataRequired()], render_kw={"placeholder": "Age"})
    submit = SubmitField("Add Result")


@app.route('/')
def home():
    swimmers = get_swimmers()
    competitions = get_competitions()
    swimming_events = get_events()

    swimming_list = []
    for event in swimming_events:
        swimmers_by_event = get_swimmers_by_event(event[0])
        for i in range(0, len(swimmers_by_event)):
            item = list(swimmers_by_event[i])
            item.append(event[0])
            item = tuple(item)
            swimmers_by_event[i] = item
        swimming_dict = dict()
        swimming_dict[event[1]] = swimmers_by_event
        swimming_list.append(swimming_dict)

    return render_template('index.html', data=swimming_list, swimmers=swimmers,
                           competitions=competitions)


@app.route('/results/<event_id>/<swimmer_id>', methods=["GET", "POST"])
def get_results(event_id, swimmer_id):
    results = get_results_by_event_by_swimmer(event_id, swimmer_id)

    for i in range(1, len(results)):

        if results[i][3] == results[i - 1][3]:
            if ':' in results[i][4]:
                time_data_i = format_time(results[i][4])
            else:
                time_data_i = results[i][4]
            if ':' in results[i - 1][4]:
                time_data_i_1 = format_time(results[i - 1][4])
            else:
                time_data_i_1 = results[i - 1][4]

            time_diff = float(time_data_i_1) - float(time_data_i)
            print(time_diff)

            if time_diff <= 0:
                results[i - 1] = results[i - 1] + (f'{time_diff:.2f}',)
            else:
                results[i - 1] = results[i - 1] + (f'+{time_diff:.2f}',)
        else:
            results[i - 1] = results[i - 1] + (' ',)

    return render_template("results3.html", data=results)


@app.route('/add_swimmer', methods=["GET", "POST"])
def add_swimmer():
    add_swimmer_form = AddSwimmer()
    if add_swimmer_form.validate_on_submit():
        first_name = add_swimmer_form.first_name.data
        last_name = add_swimmer_form.last_name.data
        con = DBConnect()
        con.cursor.execute(f'SELECT * FROM swimmer LIMIT 0')
        column_names = [desc[0] for desc in con.cursor.description]
        insert = f"INSERT INTO swimmer ({column_names[1]}," \
                 f"{column_names[2]})" \
                 f" VALUES('{first_name}','{last_name}');"

        con.cursor.execute(insert)
        con.connection.commit()
        con.cursor.close()
        return redirect(url_for("home"))

    return render_template("add_swimmer.html", form=add_swimmer_form)


@app.route('/add_competition', methods=["GET", "POST"])
def add_competition():
    add_competition_form = AddCompetition()
    if add_competition_form.validate_on_submit():
        name = format_apostrophe(add_competition_form.competition_name.data)
        team = add_competition_form.team.data
        location = add_competition_form.location.data
        year = add_competition_form.year.data
        print(year)
        # year = str(year).split('-')[0]
        con = DBConnect()
        con.cursor.execute(f'SELECT * FROM competition LIMIT 0')
        column_names = [desc[0] for desc in con.cursor.description]
        insert = f"INSERT INTO competition ({column_names[1]}," \
                 f"{column_names[2]}, {column_names[3]}, {column_names[4]})" \
                 f" VALUES('{name}','{team}', '{location}', '{year}');"

        con.cursor.execute(insert)
        con.connection.commit()
        con.cursor.close()
        return redirect(url_for("home"))

    return render_template("add_competition.html", form=add_competition_form)


@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    add_event_form = AddEvent()
    if add_event_form.validate_on_submit():
        stroke = add_event_form.stroke.data
        con = DBConnect()
        con.cursor.execute(f'SELECT * FROM event LIMIT 0')
        column_names = [desc[0] for desc in con.cursor.description]
        insert = f"INSERT INTO event ({column_names[1]})" \
                 f" VALUES('{stroke}');"

        con.cursor.execute(insert)
        con.connection.commit()
        con.cursor.close()
        return redirect(url_for("home"))

    return render_template("add_event.html", form=add_event_form)


@app.route('/add_results', methods=["GET", "POST"])
def add_results():
    swimmers = get_swimmers()
    competitions = get_competitions()
    events = get_events()
    add_results_form = AddResults()
    add_results_form.swimmer_names.choices = [swimmer[1] + ' ' + swimmer[2] for swimmer in swimmers]
    add_results_form.competition_names.choices = [competition[1] for competition in competitions]
    add_results_form.event_names.choices = [event_name[1] for event_name in events]
    con = DBConnect()
    swimmer = add_results_form.swimmer_names.data
    competition = add_results_form.competition_names.data
    event = add_results_form.event_names.data
    distance = add_results_form.distance.data
    time = add_results_form.time.data
    age = add_results_form.age.data

    if add_results_form.validate_on_submit():
        swimmer = add_results_form.swimmer_names.data

        competition = format_apostrophe(add_results_form.competition_names.data)

        event = add_results_form.event_names.data

        distance = add_results_form.distance.data

        time = add_results_form.time.data

        place = add_results_form.place.data
        age = add_results_form.age.data

        con.cursor.execute(f"SELECT id from swimmer where swimmer.first_name = '{swimmer.split()[0]}';")
        swimmer_id = con.cursor.fetchall()[0][0]

        con.cursor.execute(f"SELECT id from competition where name = '{competition}';")
        competition_id = con.cursor.fetchall()[0][0]
        con.cursor.execute(f"SELECT id from event where stroke = '{event}';")
        event_id = con.cursor.fetchall()[0][0]

        con.cursor.execute(f'SELECT * FROM results LIMIT 0')
        column_names = [desc[0] for desc in con.cursor.description]
        insert = f"INSERT INTO results ({column_names[0]}," \
                 f"{column_names[1]}, {column_names[2]}, {column_names[3]}, {column_names[4]}, {column_names[5]}, {column_names[6]})" \
                 f" VALUES('{swimmer_id}','{competition_id}', '{event_id}', '{distance}', '{age}', '{place}', '{time}');"

        con.cursor.execute(insert)
        con.connection.commit()
        con.cursor.close()
        return redirect(url_for("home"))

    return render_template("add_results.html", form=add_results_form)


@app.route('/comp_results', methods=["GET", "POST"])
def get_comp_results():
    con = DBConnect()
    swimmer = request.form['swimmers']
    comp = format_apostrophe(request.form['competitions'])
    con.cursor.execute(f"SELECT id from swimmer where swimmer.first_name = '{swimmer.split()[0]}';")
    swimmer_id = con.cursor.fetchall()[0][0]
    con.cursor.execute(f"SELECT id from competition where competition.name = '{comp}';")
    comp_id = con.cursor.fetchall()[0][0]
    con.cursor.execute(f"SELECT * from results where results.swimmer_id = '{swimmer_id}' and "
                       f"results.competition_id = '{comp_id}' order by results.event_id, results.distance asc;")
    results_data = con.cursor.fetchall()

    for i in range(0, len(results_data)):
        con.cursor.execute(f"SELECT stroke from event where id = '{results_data[i][2]}';")
        stroke = con.cursor.fetchall()[0][0]
        results_data[i] = results_data[i] + (stroke,)
    con.cursor.close()
    return render_template("comp_results.html", data=results_data, swimmer=swimmer, comp=comp)


@app.route('/pbs', methods=["GET", "POST"])
def get_personal_bests():
    con = DBConnect()
    swimmer = request.form['swimmers_pb']
    con.cursor.execute(f"SELECT id from swimmer where swimmer.first_name = '{swimmer.split()[0]}';")
    swimmer_id = con.cursor.fetchall()[0][0]
    con.cursor.close()
    times = get_pbs(swimmer_id)
    return render_template('pbs.html', data=times, swimmer=swimmer)


@app.route('/pbs_compare', methods=["GET", "POST"])
def get_personal_bests_compare():
    con = DBConnect()
    swimmer1 = request.form['swimmers_pb_compare1']
    swimmer2 = request.form['swimmers_pb_compare2']
    con.cursor.execute(f"SELECT id from swimmer where swimmer.first_name = '{swimmer1.split()[0]}';")
    swimmer1_id = con.cursor.fetchall()[0][0]
    con.cursor.execute(f"SELECT id from swimmer where swimmer.first_name = '{swimmer2.split()[0]}';")
    swimmer2_id = con.cursor.fetchall()[0][0]
    con.cursor.close()
    times = get_pbs_compare(swimmer1, swimmer2, swimmer1_id, swimmer2_id)
    print(times)
    print(times.values())
    return render_template('pbs_compare.html', data=times,
                           swimmer1=swimmer1, swimmer2=swimmer2)


if __name__ == "__main__":
    app.run(debug=False, port=5002)
