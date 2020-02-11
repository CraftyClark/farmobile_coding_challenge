from flask import Flask
import csv
import time
from datetime import datetime, timedelta
from collections import Counter

filename = '../Include/custom_data.csv'

starttime = time.time()

can_messages_dict = {}

app = Flask(__name__)

@app.route('/total-gps')
def returnGpsCount():
    return str(gps_messages_count)

@app.route('/total-can')
def returnCanCount():
    return str(can_messages_count)

@app.route('/total-unique-can')
def returnUniqueCanCount():
    return str(unique_can_messages_count)

@app.route('/total-runtime')
def returnTotalRuntime():
    return str(total_runtime)

@app.route('/average-can-messages')
def returnAvgCanMessages():
    # find average CAN messages per second of runtime
    avg_can_per_second_runtime = can_messages_count / total_runtime
    # find average CAN messages per GPS message
    avg_can_per_gps_message = can_messages_count / gps_messages_count
    # return both values
    return "{}, {}".format(avg_can_per_second_runtime, avg_can_per_gps_message)


@app.route('/most-can-messages')
def returnMostCanMessages():
    return ts_most_can_messages


@app.route('/least-can-messages')
def returnLeastCanMessages():
    return ts_least_can_messages


def totalUniqueCanMessages(id, unique_can_messages_count):
    if id in can_messages_dict:
        can_messages_dict[id] += 1
    else:
        # if key doesn't exist, it's unique, add to count
        unique_can_messages_count += 1
        can_messages_dict[id] = 1

    return unique_can_messages_count


def convertDateToDateObject(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return current_row_date


def calculateRunTime(latest_timestamp, earliest_timestamp):
    total_runtime_object = latest_timestamp - earliest_timestamp
    total_runtime = total_runtime_object.days * 24 * 3600 + total_runtime_object.seconds
    return total_runtime


def findFirstKeyUsingValue(sorted_counter, ts_value):
    for key, value in sorted_counter:
        if value == ts_value:
            return key


def lookAtData():

    global gps_messages_count 
    gps_messages_count = 0
    global can_messages_count 
    can_messages_count = 0
    global unique_can_messages_count
    unique_can_messages_count = 0
    # initialize earliest timestamp using a far future date
    global earliest_timestamp
    earliest_timestamp = datetime(3000, 1, 1)
    # initialize latest timestamp using a far past date
    global latest_timestamp
    latest_timestamp = datetime(1000, 1, 1)
    global total_runtime
    total_runtime = 0

    global cnt
    cnt = Counter()

    global ts_most_can_messages
    ts_most_can_messages = 0
    global ts_least_can_messages
    ts_least_can_messages = 0

    with open(filename) as csvfile:  
        data = csv.DictReader(csvfile)
        for row in data:
            
            # handle total runtime of data in file
            # get date object from date string
            current_row_date = convertDateToDateObject(row['ts'])

            # check if current date is the earliest or latest 
            if current_row_date < earliest_timestamp:
                earliest_timestamp = current_row_date
            elif current_row_date > latest_timestamp:
                latest_timestamp = current_row_date

            current_gps_id = row['gps_id']
            current_message_id = row['message_id']

            # if current row has gps id, it's a GPS message
            if current_gps_id:
                gps_messages_count += 1

            # else if current row has message id, it's a CAN message
            elif current_message_id:
                can_messages_count += 1
                # find total unique CAN messages
                unique_can_messages_count = totalUniqueCanMessages(current_message_id, unique_can_messages_count)

                # find first timestamp that contains the most CAN messages
                # use the current row date string
                # create a counter
                cnt[row['ts']] += 1



    # find total runtime of the data in the the file
    total_runtime = calculateRunTime(latest_timestamp, earliest_timestamp)

    # find first timestamp that contains the most CAN messages
    ts_most_value = cnt.most_common()[0][1]

    # find the first timestamp that contains the least CAN messages
    # cnt = sorted(cnt.items())


    ts_least_can_messages = cnt.most_common()[:-2:-1]
    ts_least_value = ts_least_can_messages[0][1]

    sorted_counter = sorted(cnt.items())

    ts_most_can_messages =  findFirstKeyUsingValue(sorted_counter, ts_most_value)
    ts_least_can_messages =  findFirstKeyUsingValue(sorted_counter, ts_least_value)



if __name__ == '__main__':
    lookAtData()
    print("Program run time = {} seconds".format(time.time() - starttime))
    app.run(debug=True)

    
