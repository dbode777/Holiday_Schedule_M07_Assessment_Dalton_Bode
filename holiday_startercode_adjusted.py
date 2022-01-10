import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass, field


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday():
    """
    DOCSTRING: ...
    """
    # name: str
    # date: date (YYYY-MM-DD)
    # type: str 
    # details: str, defaults to ''     
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
    
@dataclass
class HolidayList():
    """
    DOCSTRING:
    """
    # innerHolidays: list = []

    def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays (use pop() method)
        # inform user you deleted the holiday (use print() method)

    def read_json(filelocation):
        # Read in things from json file location (json.loads)
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(filelocation):
        # Write out json file to selected file. (json.dump)
        
    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2 years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # save the results as a list of dictionaries
        # Check to see if name and date of holiday is in innerHolidays array (if ... not in innerHolidays: then ...)
        # Add non-duplicates to innerHolidays
        # Handle any exceptions. (try/except statements)

    def numHolidays():
        # Return the total number of holidays in innerHolidays (use len() method)
    
    def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        ## holidays = lambda ...
        ## holidayList = list(filter(holidays, innerholidays))
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return holidayList

    def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # use https://rapidapi.com/community/api/open-weather-map
        # Sign-up for auth-key
        # Format weather information and return weather string.

    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

def add_Holiday(holidayList):
    # Asks user for Holiday and saves to a variable.
    # tries to see if the date is valid
        # if it is, skips except clause.
    # if not, exception prints error message and doesn't return anything.
    # next tries to see if holiday is in Holidaylist object:
        # if not, add holiday to HolidayList object, returns nothing.
    # if it is, exception prints error that the holiday is in the list. Returns nothing

def remove_Holiday(holidayList):
    # Similar to add_Holiday, but last try/except statement checks to see if the holiday is NOT in the list, instead.

def save_file(holidayList):
    # Asks user if they want to save
    # if yes, ask user what filename they want to save the file as
    # calls holidayList's save_to_json method with the filename as a parameter
    
def view_Holidays(holidayList):
    # Asks user what year they would like to view.
    # Asks user what week they would like to view.
        # Tries using the user_inputs to gather the information
        # If it works, it prints out each of the holidays and their dates.
        # If it doesn't work, prints out error message telling the user their inputs were not numbers or which number was outside their respective ranges.
    # Asks user if they want to see the current week's weather
        # If they do, print out the current week's holidays, dates, and weather reports
        # If they don't, continue to the next lines of code.
        # Raise exception if they enter something unintended.

def exit_program(filename,holidayList):
    # reads in most recent saved holidayList JSON file by filename
    # If that doesn't match current holidayList, ask them if they want to save changes before exiting
        # if they do, run the save_file function
        # if they don't, print out Goodbye! and return False to while loop condition
    # Otherwise, they did save their info and want to exit, so print Goodbye! and return False to the while loop condtion.
    # returns boolean to while loop condition. If they do want 

def menu_selection(user_input):
    # try:
        # If statements for each number of the menu select screen 
        # last statement checks if number is in list of all menu number options.
        # Any statement thats not a integer or not in the list will return the except clause 
    # except:
        # print out error message
        # return True to while loop condition to continue asking user

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display start-up screen (prints f-string with number of holidays stored in the system)
    # 5. Display User Menu (Print the menu)
    # Main Menu
        # ====================
        # 1. Add a Holiday
        # 2. Remove a Holiday
        # 3. Save Holiday List
        # 4. View Holidays
        # 5. Exit
        # ====================
    # 6. Take user input for their action based on Menu and check the user input for errors
        # Run menu_selection function() to execute selected menu option
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
        # If yes, while loop condition stays True.
        # If no, while loop condition stays False.

if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





