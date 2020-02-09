from flask import Flask
import csv
from collections import Counter

filename = '../Include/gps_small_can_dataset.csv'

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


def totalUniqueCanMessages(id, unique_can_messages_count):
    if id in can_messages_dict:
        can_messages_dict[id] += 1
    else:
        # if key doesn't exist, it's unique, add to count
        unique_can_messages_count += 1
        can_messages_dict[id] = 1

    return unique_can_messages_count


def lookAtData():

    global gps_messages_count 
    gps_messages_count = 0
    global can_messages_count 
    can_messages_count = 0
    global unique_can_messages_count
    unique_can_messages_count = 0


    with open(filename) as csvfile:  
        data = csv.DictReader(csvfile)
        for row in data:
            
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
