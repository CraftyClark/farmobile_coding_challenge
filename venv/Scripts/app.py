from flask import Flask, jsonify
import logging
import csv
import time
from datetime import datetime, timedelta
from collections import Counter

filename = '../Include/gps_can_data.csv'
app = Flask(__name__)


@app.route('/total-gps')
def returnGpsCount():
    return jsonify(
        total_gps = str(gps_messages_count)
    )


@app.route('/total-can')
def returnCanCount():
    return jsonify(
        total_can = str(can_messages_count)
    )


@app.route('/total-unique-can')
def returnUniqueCanCount():
    return jsonify(
        total_unique_can = str(unique_can_messages_count)
    )


@app.route('/total-runtime')
def returnTotalRuntime():
    return jsonify(
        total_runtime = str(total_runtime)
    )


@app.route('/average-can-messages')
def returnAvgCanMessages():
    # find average CAN messages per second of runtime
    avg_can_per_second_runtime = can_messages_count / total_runtime
    # find average CAN messages per GPS message
    avg_can_per_gps_message = can_messages_count / gps_messages_count
    # return both values
    return jsonify(
        average_can_per_second_runtime = avg_can_per_second_runtime,
        avg_can_per_gps_message = avg_can_per_gps_message
    )


@app.route('/most-can-messages')
def returnMostCanMessages():
    return jsonify(
        most_can_messages = ts_most_can_messages
    )


@app.route('/least-can-messages')
def returnLeastCanMessages():
    return jsonify(
        least_can_messages = ts_least_can_messages
    )


def totalUniqueCanMessages(id, unique_can_messages_count, can_messages_dict):
    """Determines if given message id is unique and returns the current count of unique CAN messages."""
    if id in can_messages_dict:
        can_messages_dict[id] += 1
    else:
        # if key doesn't exist, it's unique, add to count
        unique_can_messages_count += 1
        can_messages_dict[id] = 1

    return unique_can_messages_count


def convertDateToDateObject(date_string):
    """Converts date string into date object."""
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return current_row_date


def calculateRunTime(latest_timestamp, earliest_timestamp):
    """Calculates the total runtime of the data using the earliest and latest timestamps."""
    total_runtime_object = latest_timestamp - earliest_timestamp
    total_runtime = total_runtime_object.days * 24 * 3600 + total_runtime_object.seconds
    return total_runtime


def findFirstKeyUsingValue(sorted_counter, ts_value):
    """Finds the first key in the dictionary where the key's value matches the given timestamp count value."""
    for key, value in sorted_counter:
        if value == ts_value:
            return key


def lookAtData():
    """Calculates for the requested data using the input data CSV file."""

    # declare global variables
    global gps_messages_count, can_messages_count, unique_can_messages_count, earliest_timestamp, latest_timestamp
    global total_runtime, counter_dictionary, ts_most_can_messages, ts_least_can_messages, can_messages_dict

    # initialize variables
    gps_messages_count = can_messages_count = unique_can_messages_count = 0
    total_runtime = ts_most_can_messages = ts_least_can_messages = 0
    current_row_count = 1 # initialize to 1 to account for row of column names
    
    # initialize timestamp variables using datetime max and min
    # max date is used for the earliest timestamp variable to give ourselves a value to compare to in the future when 
    # ... trying to find the earliest timestamp in the file; the same strategy is used for the latest timestamp variable
    earliest_timestamp = datetime.max
    latest_timestamp = datetime.min

    # declare a new empty Counter
    counter_dictionary = Counter()
    # initalize dictionary for CAN messages
    can_messages_dict = {}

    # open input CSV file
    try:
        with open(filename) as csvfile:  
            data = csv.DictReader(csvfile)
            for row in data:
                # increment row count for empty row logging purposes
                current_row_count += 1
                # handle total runtime of data in file
                # get date object using date string from column 'ts'
                try:
                    current_row_date = convertDateToDateObject(row['ts'])
                except:
                    logging.warning('row {} has no timestamp value'.format(current_row_count)) 

                # check if current date is the earliest or latest 
                if current_row_date < earliest_timestamp:
                    earliest_timestamp = current_row_date
                elif current_row_date > latest_timestamp:
                    latest_timestamp = current_row_date

                # create variables to store string data for current row in data file
                current_gps_id = row['gps_id']
                current_message_id = row['message_id']

                # determine if current row is a GPS or CAN message
                # keep a running count for both message types
                if current_gps_id:
                    # current row is a GPS message
                    gps_messages_count += 1

                elif current_message_id:
                    # current row is a CAN message
                    can_messages_count += 1
                    # find total unique CAN messages
                    unique_can_messages_count = totalUniqueCanMessages(current_message_id, unique_can_messages_count, can_messages_dict)

                    # tally timestamp occurrence in Counter
                    counter_dictionary[row['ts']] += 1
                else:
                    # if both message_id and gps_id are empty; log warning
                    logging.warning('row {} has no values for message_id or gps_id'.format(current_row_count))
    except:
        logging.critical('Unable to open CSV file. Please check that the correct filename is being used on line 8 of app.py')
        exit(0)

    # find total runtime of the data in the the file
    total_runtime = calculateRunTime(latest_timestamp, earliest_timestamp)

    # find integer value representing the largest number of CAN message occurrences for any timestamp
    ts_most_value = counter_dictionary.most_common()[0][1]

    # find integer value representing the smallest number of CAN message occurrences for any timestamp
    ts_least_can_messages = counter_dictionary.most_common()[:-2:-1]
    ts_least_value = ts_least_can_messages[0][1]

    # use the sorted method to use the counter dictionary to create a list of sorted tuples
    # this list of sorted tuples will be sorted by 
    sorted_counter = sorted(counter_dictionary.items())

    # find the first timestamps for which contain the corresponding most and least CAN messages
    ts_most_can_messages =  findFirstKeyUsingValue(sorted_counter, ts_most_value)
    ts_least_can_messages =  findFirstKeyUsingValue(sorted_counter, ts_least_value)


if __name__ == '__main__':
    # start time to track program execution speed
    starttime = time.time()
    logging.info('reading in input CSV data file: {}'.format(filename))
    # call function to begin program
    lookAtData()
    # log the program's run time
    logging.info("Program run time = {} seconds".format(time.time() - starttime))
    # run flask application
    app.run()
