# farmobile_coding_challenge
 software developer coding challenge for farmobile

Instructions for this coding challenge are described in the pdf file, 'Farmobile Coding Challenge_Software', located in the same directory as this README.md file

Where to locate app.py?
1. I followed installation instructions for Flask and virtualenv linked here -> https://flask.palletsprojects.com/en/1.1.x/installation/
2. Since I used virtualenv, you will not find app.py in the root directory but instead you will find it in farmobile_coding_challenge/venv/Scripts


How to run program:
1. Unzip and extract using 7zip
2. Copy desired source CSV data input file into directory farmobile_coding_challenge/Include/
    or use the source data that is already in the directory ('gps_can_data.csv')
    2a. If you are copying over your own data input csv file. Alter the text on line 8 of app.py from 'gps_can_data.csv' to the name of your source file. 
3. No arguments are needed to run the program. Simply run the program by opening a terminal, navigating to the directory containing app.py 
    (farmobile_coding_challenge/venv/Scripts), and type into terminal 'python app.py', press enter


What does program do / how to test program?
1. The program will use the input CSV data file to calculate for appropriate values and then host them at http://127.0.0.1:5000/*insert routing location  here*
2. In order to quickly test program, you can use the text file 'farmobile_coding_challenge/routing_documentation_for_requested_data.txt' in order to quickly 
    navigate to each URL by control clicking on the link from your favorite text editor. You may also copy paste or just manually type in the urls into your browser.


Program results:
1. The program's results are pretty straight forward. All the requested data is returned to the screen in JSON form. 
    Also you can view the results I got by referring to program_results_screenshot.PNG
2. I added some useful logging messages throughout the program. 
    2a. Including a critical program ending message (also ends program) if the filename for the data input file is incorrect and cannot be opened.
    2b. Also I created log warning messages (logging msg is printed to terminal but program continues on as usual) for if a given row has no timestamp value 
        and/or if a given row has neither message_id or gps_id


Other files included in this folder, and what they are:
1. sources.txt: this file sites the docs/sources that helped me build this project
2. routing_documentation_for_requested_data.txt: list of routing urls for testing the program
3. README.md: this document you're reading, which provides clarity and instructions on how to run program
4. program_results_screenshot.PNG: screenshots of all the program's output put into one image file
5. Farmobile Coding Challenge_Software.pdf: complete instructions for this coding challenge


Thank you for taking the time to look over my project. 
-Andrew 