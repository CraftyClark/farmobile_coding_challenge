from flask import Flask
import csv
import time
from datetime import datetime, timedelta

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
    total_runtime_object = latest_timestamp - earliest_timestamp
    total_runtime = total_runtime_object.days * 24 * 3600 + total_runtime_object.seconds
    return str(total_runtime)


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

            # if current row has message id, it's a CAN message
            if current_message_id:
                can_messages_count += 1
                unique_can_messages_count = totalUniqueCanMessages(current_message_id, unique_can_messages_count)







if __name__ == '__main__':
    lookAtData()
    app.run(debug=True)

    print("Program run time = {} seconds".format(time.time() - starttime))
