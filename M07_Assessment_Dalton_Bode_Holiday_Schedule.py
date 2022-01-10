# Imports
import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

# Data Classes
@dataclass
class Holiday():
    """
    DOCSTRING: Helps with generating Holiday objects. Requires a name and date.
    A string consisting of the object's name and date are printed when the object is called with the str() method.
    
    PARAMETERS: 
    name: str defaults to string of a space
    date: datetime.date object defaults to the beginning of 2020

    RETURNS: 
    - __str__ method returns modified string version of how the parameters should be displayed.
    """
    name: str = ' '
    date: datetime.date = datetime.date(2020,1,1)  
    
    def __str__ (self):
        return f"{self.name} ({self.date})"
    
@dataclass
class HolidayList():
    """
    DOCSTRING: Creates a holiday list object from holiday objects. Initialize with the read_json method to populate an originating list of holidays from a JSON file
    
    PARAMETERS: innerHolidays: list defaults to an empty list
    
    RETURNS: 
    - numHolidays method returns the length of the innerHolidays list for the initial start-up screen.
    - getWeather method returns the list of weather information for the next 7 days for whichever city, country combo the user input.
    If the user has too many failed attempts (more than 10 requests), they will be returned back to the main menu with the return value 'max_response'.
    - Every other method either prints out a string for the user or makes adjustments to the list with no output displayed to the user. 
    These methods are used inside functions of higher scope.
    """
    innerHolidays = []

    def addHoliday(self, holidayName, date):
        
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(Holiday(holidayName, date)) == type(Holiday()):
            self.innerHolidays.append({"name": f"{Holiday(holidayName, date).__dict__['name']}", "date": f"{str(Holiday(holidayName, date).__dict__['date'])}"})

    def removeHoliday(self, holidayName, date):
        # Removes the holiday object from the list
        if type(Holiday(holidayName, date)) == type(Holiday()):
            self.innerHolidays.pop(self.innerHolidays.index({"name": f"{Holiday(holidayName, date).__dict__['name']}", "date": f"{str(Holiday(holidayName, date).__dict__['date'])}"}))

    def read_json(self, fileName):
        # Read in things from json file location (json.loads)
        with open(fileName, "rt",encoding = "utf-8") as holidayList:
            # Updates list with pre-saved list
            self.innerHolidays = json.load(holidayList)["holidays"]
            
    def save_to_json(self, fileName):
        # Write out json file to selected file. (json.dump)
        with open(fileName, "wt", encoding = 'utf-8') as holidayList:
            json.dump({"holidays": self.innerHolidays}, holidayList)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/calendar/print.html?year=2023&country=1&cols=3&hol=33554809&df=1
        past = datetime.datetime.today().year - 2
        thisYear = datetime.datetime.today().year
        future = datetime.datetime.today().year +2
        yearList = [past, thisYear, future]
        months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
        
        # Adds to the holiday list if the holiday's aren't already in the holiday list for previous 2 years, current year and next 2 years.
        for year in yearList:
            url = f"https://www.timeanddate.com/calendar/print.html?year={year}&country=1&cols=3&hol=33554809&df=1"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            
            try:
                for row in soup.find('table', attrs = {'class':"cht lpad"}).find_all('tr'):
                    # Converts month into integer for date object
                    for month in list(months.keys()):
                        if month != row.find_all('td')[0].text[0:3]:
                            continue
                        else:
                            holidayMonth = int(months[row.find_all('td')[0].text[0:3]])
                            break
                    
                    # Converts day into integer for date object       
                    day = int(row.find_all('td')[0].text.split(' ')[1])
                    
                    # Adds non-duplicates to the holiday list
                    if {"name": row.find_all('td')[1].text, "date": str(datetime.date(year,holidayMonth,day))} not in self.innerHolidays:
                        self.addHoliday(row.find_all('td')[1].text, datetime.date(year,holidayMonth,day))
                    
                    else:
                        continue

            except:
                print("Something went wrong.")

    def numHolidays(self):
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year, weekNumber):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
    
        # Used as a function to filter each element of the list to retrieve desired holiday information
        def holidayWeeks(holiday):
            dateobj = datetime.date(int(str(holiday['date'])[0:4]),int(str(holiday['date'])[5:7]),int(str(holiday['date'])[8:10]))
            if str(year) == str(dateobj)[0:4] and str(weekNumber) == str(dateobj.isocalendar()[1]):
                return True
        
        # Creates a list of strings for all holidays from the inputed week number and year
        holidayWeekList = list(filter(lambda x: holidayWeeks(x), self.innerHolidays))
        return holidayWeekList

    def displayHolidaysInWeek(self, holidayWeekList):
        # Print out each holiday
        for i in holidayWeekList:
            print(f"{i['name']} {str(i['date'])}\n")
        
        print(f"Number of holidays in the week: {len(holidayWeekList)}")
            
    def getWeather(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        
        num_requests=0
        # Only allows for 10 requests per visit to the submenu that calls this function
        while num_requests<11:
            city = str(input("\nWhat city's forecast would you like to see? : ")).title()
            country = str(input("\nWhat's the country abbrevation for this city? : ")).upper()

            # Retrieves daily weather forecast for next 7 days
            querystring = {"q":f"{city}, {country}","cnt":"7","mode":"xml"}

            headers = {
                'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
                'x-rapidapi-key': "100d55a295mshe1ccfe736e38503p1c8bffjsn3804385600b3"
            }

            response = requests.request("GET", url, headers=headers, params=querystring).text
            soup = BeautifulSoup(response,'lxml-xml')
            try:
                weatherList = []
                # If the response can't find the city or country, this code won't work
                for row in soup.find_all('time'):
                    weatherList.append({'date':row.attrs['day'], 'conditions': row.find('symbol').attrs['name']})
                return weatherList
            except:
                print(soup.text)
                num_requests+=1
                if num_requests == 11:
                    print("You made the maximum amount of requests. You will be returned back to the main menu")
                    return ['max_response']

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up rest of the current week and year
        next7Days = []
        for x in range(0,7):
            # Adds number of days in ordinal format and then reconverts that number back into a datetime object
            next7Days.append(datetime.date.fromordinal(datetime.date.today().toordinal()+datetime.date(1,1,x+1).toordinal()))    
            
        currentYear = datetime.datetime.today().year
        # Use your filter_holidays_by_week function to get the list of holidays for the current week/year
        currentWeeksHolidaysList = []
        next7DaysWeekNum = list(map(lambda x: x.isocalendar()[1], next7Days))
        calledWeekNums = []
        for x in next7DaysWeekNum:
            if x not in calledWeekNums:
                calledWeekNums.append(x)
                # Adds two weeks worth of holidays 6/7ths of the time
                currentWeeksHolidaysList.append(self.filter_holidays_by_week(currentYear,x))
        
        def next7DayDates(holiday):
             if str(holiday['date'])[-10:] in list(map(lambda date: str(date),next7Days)):
                return True
            
        # Filters out holidays whose dates don't match any dates in the next 7 days
        # -10 is used since every date will comprise the last 10 digits of any string from a holiday object
        if type(currentWeeksHolidaysList) != None:
            if type(currentWeeksHolidaysList[0]) != None:
                next7DayHolidays = list(filter(lambda x: next7DayDates(x), currentWeeksHolidaysList[0]))
            try:
                if type(currentWeeksHolidaysList[1]) != None:
                    if type(currentWeeksHolidaysList[0]) == None:
                        next7DayHolidays = list(filter(lambda x: next7DayDates(x), currentWeeksHolidaysList[1]))
                    elif type(currentWeeksHolidaysList[0]) != None:
                        next7DayHolidays.extend(list(filter(lambda x: next7DayDates(x), currentWeeksHolidaysList[1])))
            except:
                pass

        # Use your displayHolidaysInWeek function to display the holidays in the week
        while True: 
            try:
                weatherCheck = input("Would you like to see the weather? Enter y for yes or n for no: ").lower()
                if weatherCheck == 'y' or weatherCheck == 'yes':
                    forecast = self.getWeather()
                    try:
                        if forecast[0] == 'max_response':
                            break
                        else:
                            for holiday in next7DayHolidays:
                                for weather in forecast:
                                    # [-10:] retrieves date from the string
                                    if str(holiday['date'])[-10:] == str(weather['date']):
                                        print(f"{holiday['name']} ({holiday['date']}) - {weather['conditions']}")
                            break
                    except:
                        print('\nNo holidays for the next 7 days.')
                        break
                elif weatherCheck == 'n' or weathercheck == 'no':
                    try:
                        displayHolidaysInWeek(next7DayHolidays)
                        break
                    except:
                        print("\nNo holidays for the next 7 days.")
                else:
                    print("\nYou typed in a string but not what was expected. Please try again.")
                    continue
            except:
                print("\nYour response was not a string. Please try again.")

# Functions
def add_Holiday(holidayList):
    print(f"\nAdd a Holiday\n{'='* len('Add a Holiday')}")
    # holidayList needs to be HolidayList object
    while True:
        # Ask user for holiday and date to add
        addHol = str(input("\nWhat holiday would you like to add? Enter the name of the holiday: ")).title()          
        addNewDate = str(input("\nWhat is the date for this holiday? Enter a date with the following format [YYYY-MM-DD]: "))
        
        print(f"\nHoliday: {addHol}\nDate: {addNewDate}")
        # Tries to see if valid date is inputed, raises exception if not.
        try:
            # Checks to see if holiday and date is already in holiday list
            if Holiday(addHol,addNewDate).__dict__ not in holidayList.innerHolidays:
                holidayList.addHoliday(addHol,addNewDate)
                print(f"\nSuccess:\n{str(Holiday(addHol,addNewDate))} has been added to the holiday list.")
                break
            else:
                print(f"\nError:\n{str(Holiday(addHol,addNewDate))} is already in the holiday list")
                break
        except:
            print("\nError:\nInvalid date. Please Try again.")
                     
def remove_Holiday(holidayList):
    print(f"\nRemove a Holiday\n{'='*len('Remove a Holiday')}")
    while True:
        # Ask user for holiday and date to remove
        remHol = str(input("\nWhat holiday would you like to remove? Enter the name of the holiday: ")).title()
        remDate = str(input("\nWhat is the date for this holiday? Enter a date with the following format: YYYY-MM-DD: "))
        
        print(f"\nHoliday: {remHol}\nDate: {remDate}")
        # Tries to see if valid date is inputed, raises exception if not.
        try:
            # Checks to see if holiday and date is in holiday list
            if Holiday(remHol,remDate).__dict__ in holidayList.innerHolidays:
                holidayList.removeHoliday(remHol,remDate)
                print(f"\nSuccess:\n{str(Holiday(remHol,remDate))} has been removed to the holiday list.")
                break
            else:
                print(f"\nError:\n{str(Holiday(remHol,remDate))} is not in the holiday list")
                break
        except:
            print("\nError:\nInvalid date. Please Try again.")
                     
def save_file(holidayList,fileName='holidays.json'):
    print(f"\nSaving Holiday List\n{'='*len('Saving Holiday List')}")
    # Asks user if they want to save
    while True:
        saveChanges = str(input("\nAre you sure you want to save your changes? Enter y for yes or n for n: ")).lower()
        try:
            if saveChanges == 'y' or saveChanges == 'yes':
                holidayList.save_to_json(fileName)
                print('\nSuccess:\nYour changes have been saved.')
                break
            elif saveChanges == 'n' or saveChanges == 'no':
                print("\nCanceled:\nHoliday list file save canceled.")
                break
            else:
                print("\Response given was not an expected result. Please try again.")
        except:
            print("\nError:\nInvalid response. Please try again.")
    
def view_Holidays(holidayList):
    print(f"\nView Holidays\n{'='*len('View Holidays')}")
    while True: 
        # Asks user what year they would like to view.
        try:
            year = int(input("\nWhat year would you like to view? [YYYY]: "))
        except:
            print("\nError:\nInvalid year. Please try again.")
            continue
            
        # Asks user what week they would like to view.
        try: 
            weekNum = int(input("\nWhat week would you like to view? Enter a number from 1-53: "))     
        except:
            print('\nError:\nInvalid week entered. Please enter a number within the range 1 and 53.')
            continue
            
        if year == datetime.datetime.today().year and weekNum == datetime.datetime.today().isocalendar()[1]:
            while True:
                try:
                    currentVsForecastCheck = int(input("\nWould you like to view holidays for the \n\t1. current week \nor \n\t2. next 7 days?\nEnter 1 for current week or 2 for the next 7 days: "))
                    if currentVsForecastCheck == 1:
                        viewableList = holidayList.filter_holidays_by_week(year,weekNum)
                        holidayList.displayHolidaysInWeek(viewableList)
                        break

                    elif currentVsForecastCheck == 2:
                        holidayList.viewCurrentWeek()
                        break
                    else:
                        print("\nError:\nThe number entered is not valid. Please try again.")
                except:
                    print("\nError:\nInvalid response. Please try again.")
                    continue
            break
        # Looks at any week that isn't the current week
        else:     
            viewableList = holidayList.filter_holidays_by_week(year,weekNum)
            holidayList.displayHolidaysInWeek(viewableList)
            break


def exit_program(holidayList,fileName='holidays.json'):
    print(f"\nExit\n{'='*len('Exit')}")
    
    # reads in most recent saved holidayList from JSON file by fileName
    with open(fileName, "rt", encoding = 'utf-8') as savedholidays:
        savedHolidaysList = json.load(savedholidays)['holidays']
    
    # Checks to see if the current list matches the most recently saved list.
    while True:
        try:
            exit = str(input("\nAre you sure you want to exit? Enter y for yes or n for no: ")).lower()
            if exit == 'y' or exit == 'yes':
                if holidayList.innerHolidays != savedHolidaysList:
                    # Ask user if they want to save changes before exiting
                    saveChanges = str(input("\nYou have not saved your changes. Would you like to save before exiting?\nEnter y for yes or n for no: ")).lower()
                    # if they do, run the save_file function
                    try:
                        if saveChanges == 'y' or saveChanges == 'yes':
                            holidayList.save_to_json(fileName)
                            print('\nSuccess:\nYour changes have been saved.')
                            print("\nGoodbye!")
                            return False
                        elif saveChanges == 'n' or saveChanges == 'no':
                            print("\nGoodbye!")
                            return False
                    except:
                        print("\nError:\nInvalid response. Please try again.")
                else:
                    print('Goodbye!')
                    return False
            elif exit == 'no' or exit == 'n':
                print('\nReturning to Main Menu.')
                return True
            else:
                print("\nResponse not one that was expected: Please try again.")
                continue
        except:
            print("\nResponse was not a string. Please try again.")

def menu_selection(holidayList,userInput):
    if userInput == '1':
        add_Holiday(holidayList)
    elif userInput == '2':
        remove_Holiday(holidayList)
    elif userInput == '3':
        save_file(holidayList,'holidays.json')
    elif userInput == '4':
        view_Holidays(holidayList)
    elif userInput == '5':
        return exit_program(holidayList,'holidays.json')

def main():
    
    # 1. Initialize HolidayList Object
    holidayList = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    holidayList.read_json('holidays.json')
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    holidayList.scrapeHolidays()
    # 3. Create while loop for user to keep adding or working with the Calender
    working = True
    while working:
        # 4. Display start-up screen (prints f-string with number of holidays stored in the system)
        print(f"\nHoliday Management\n{'='*len('Holiday Management')}\nThere are {holidayList.numHolidays()} holidays stored in the system.")
        # 5. Display User Menu (Print the menu)
        print("\nMain Menu")
        print("====================")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        print("====================")
        userInput = str(input("\nEnter the number corresponding to the part of the menu you'd like to select: "))
        if userInput in ['1','2','3','4']:
            menu_selection(holidayList, userInput)
            continue
        elif userInput == '5':
            working = menu_selection(holidayList, userInput)
            continue
        else:
            print(f"{userInput} does not correspond to a valid menu option. Please choose again.")
            continue

# Run Program
if __name__ == "__main__":
    main();