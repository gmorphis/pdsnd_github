import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Prompt the user for input

    cont = 'no'

    while cont.lower() == 'n' or cont.lower() == 'no':


        city = input("We currently have data for Chicago, New York, and Washington. \nPlease enter a city (Chicago, New York, or Washington): ")

        # Keep looping until valid input is provided
        while city.lower() not in ["chicago", "new york", "washington"]:
            print("Invalid city selection. Please try again.")
            city = input("We currently have data for Chicago, New York, and Washington. \nPlease enter a city (Chicago, New York, or Washington): ")


        # get user input for month (all, january, february, ... , june)
        month = input("Which month would you like data for? \nPlease enter 1 (January) - 12 (December) or 'all' for no month filter: ")
        while month.lower() not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "all"]:
            print("Invalid month selection. Please try again.")
            city = input("Which month would you like data for? \n1-12 or 'all' for no month filter: ")



        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day of the week would you like data for? Please enter 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri' ,'Sat', or 'all' for no day filter: ")
        while day.lower() not in ["sun", "mon", "tue", "wed", "thu", "fri", "sat", "all"]:
            print("Invalid day selection. Please try again.")
            day = input("Which day of the week would you like data for? Please enter 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri' ,'Sat', or 'all' for no day filter: ")

        cont = input("You've chosen {0} as the City, {1} as the month and {2} as the day. \nIf something needs to be fixed enter 'n/no' to go back and fix your selection, else press 'enter' to continue."
                     .format(city.capitalize(), 
                             'All' if month.lower() == 'all' else calendar.month_name[int(month)],
                             'All' if day.lower() == 'all' else day.capitalize()
                     ))


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])


    if city == 'washington': #washington is missing these 2 columns, add them to normalize the data
        df['Gender'] = pd.Series(dtype=str)  # Adding an empty column 'Gender'
        df['Birth Year'] = pd.Series(dtype=float) 

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #print(df.head())
    if month != 'all':
        df = df[df['Start Time'].dt.month == int(month)]


    #Monday is 0 and Sunday is 6
    day_num = 0
    if day != 'all':
        if day == 'sun': day_num = 6
        elif day == 'mon': day_num = 0
        elif day == 'tue': day_num = 1
        elif day == 'wed': day_num = 2
        elif day == 'thu': day_num = 3
        elif day == 'fri': day_num = 4
        elif day == 'sat': day_num = 5
        df = df.loc[df['Start Time'].dt.weekday == int(day_num)]


    #print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

   # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    month_counts = df.groupby('month').size()
    popular_month = month_counts.idxmax()

    #calendar.month_name[popular_month]
    print("The most popular month is ", calendar.month_name[popular_month])
    # display the most common day of week
    df['weekday'] = df['Start Time'].dt.weekday
    day_counts = df.groupby('weekday').size()
    popular_day = day_counts.idxmax()
    print("The most popular day of the week is ", calendar.day_name[popular_day])

    # display the most common start hour
 
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
        # Group by the hour column and count the occurrences
    hour_counts = df.groupby('hour').size()

    # Print the most popular hour
    # find the most common hour (from 0 to 23)
    popular_hour = hour_counts.idxmax()
    popular_hour_string = ''
    if popular_hour > 12:
        popular_hour = popular_hour - 12
        popular_hour_string = str(popular_hour) + ' PM'
    else:
        popular_hour_string = str(popular_hour) + ' AM'

    print("The most popular hour is ", popular_hour_string)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Comb Station'] = df['Start Station'] + ' ' + df['End Station']

    most_frequent_combination = df['Comb Station'].mode()[0]

    print("The most common Start Station is: ", most_common_start_station)
    print("The most common End Station is: ", most_common_end_station)
    print("The most frequent combination Station is: ", most_frequent_combination)
    print('-'*40)
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    #df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['End Time'] = pd.to_datetime(df['End Time'])

    #df['Travel Time'] = df['End Time'] - df['Start Time']
    travel_time = df['Trip Duration'].sum()

    # display total travel time
    print("The total travel time is: ", travel_time)


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The average travel time is: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print("Counts based on user types: ", user_types)

    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        if len(genders):
            print("Counts based on genders: ", genders)
        else:
            print("This city is missing data based on gender.")
    except Exception as e:
        print("This city may not contain Gender data.")
    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]

        print("The earliest birth year of riders is: ", str(earliest))
        print("The youngest birth year of riders is: ", str(most_recent))
        print("With the most common birth year being: ", str(most_common))


    except Exception as e:
        print("This city is missing data based on birth year.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)
        #df = load_data('chicago', '3', 'all')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        
        user_stats(df)

        #False

        raw_data = input('\nWould you like to view the dataset used in this research? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            chunkify(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def chunkify(df):
    """Displays raw data in 5 row chunks."""

    # Set the initial row index to 0
    row_index = 0

    while True:
        print(df[row_index:row_index + 5])
        
        row_index += 5
        
        # Ask the user if they want to continue seeing the raw data
        user_input = input("Enter 'no' to return to the main screen or press enter to keep seeing the data: ") 
        if user_input.lower() == "no":
            break

    
    return




if __name__ == "__main__":
	main()
