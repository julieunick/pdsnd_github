import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. While loops are set up to handle invalid inputs.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # collects city input from user
    city_input = input("\nPlease enter the city name (chicago, new york city, or washington): ").lower()
    while True:
        if city_input == "chicago" or city_input == "new york city" or city_input == "washington":
            city = city_input
            break
        else:
            city_input = input("Unexpected input. Please enter the city name (chicago, new york city, or washington): ").lower()

    # collects month input from user
    month_input = input("\nPlease enter which month you would like the information for. You may enter 'all' or a month name: ").lower()
    while True:
        if month_input == "all" or month_input == "january" or month_input == "february" or month_input == "march" or month_input == "april" or month_input == "may" or month_input == "june":
            month = month_input
            break
        else:
            month_input = input("Unexpected input. Please enter which month you would like the information for. You may enter 'all' or a month name from January to June: ").lower()


    # collects weekday input from user
    day_input = input("\nPlease enter which day you would like the information for. You may enter 'all' or the name of a weekday: ").lower()
    while True:
        if day_input == "all" or day_input == "monday" or day_input == "tuesday" or day_input == "wednesday" or day_input == "thursday" or day_input == "friday" or day_input == "saturday" or day_input == "sunday":
            day = day_input
            break
        else:
            day_input = input("Unexpected input. Please enter which month you would like the information for. You may enter 'all' or the name of a weekday: ").lower()

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

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name


    # filter by month if applicable to create new dataframe
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df["month"] == month]

    # filter by day of week if applicable to create new dataframe
    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month_name()
    popular_month = df["month"].mode()[0]

    print("Most Frequent Month:", popular_month)


    # Display the most common day of week
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    popular_day = df["day_of_week"].mode()[0]

    print('Most Frequent Day:', popular_day)


    # Display the most common start hour
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]

    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print("Most Popular Start Station:", common_start_station)



    # Display most commonly used end station
    common_end_station = df["End Station"].mode()[0]

    print("Most Popular End Station:", common_end_station)

    # Display most frequent combination of start station and end station trip
    df["station_combination"] = "'{}' and '{}'".format(df["Start Station"], df["End Station"])
    common_station_combo = df["station_combination"].mode()[0]
    print("Most Popular Combination Of Start Station and End Station:", common_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Travel Time:", total_travel_time, "seconds")


    # Display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean Travel Time:", mean_travel_time, "seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Practice Problem #2 information was utilized for this portion.
    """

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("Count Of User Types:")
    print(user_types)

    # check if the requested city is either "chicago" or "new york city", as only those datafiles contain gender or birth year information
    if city != "washington":
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts:")
        print(gender_counts)


        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        print("\nEarliest Birth Year:", earliest_year)

        most_recent = int(df["Birth Year"].max())
        print("Most Recent Birth Year:", most_recent)

        most_common = int(df["Birth Year"].mode()[0])
        print("Most Common Birth Year:", most_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data when requested. 5 lines of data are displayed at a time"""

    data_input = input("\nWould you like to see raw data for your selection? Enter yes or no: ").lower()

    # variables to get the row index range
    previous_row_count = 0
    new_row_count = 0

    while True:
        if data_input == "yes":
            new_row_count += 5
            previous_row_count = new_row_count - 5
            print(df[previous_row_count:new_row_count])
            data_input = input("\nWould you like to see additional raw data for your selection? Enter yes or no: ").lower()
        elif data_input == "no":
            break
        else:
            data_input = input("Unexpected input. Would you like to see raw data for your selection? Enter yes or no: ").lower()


def main():
    """Calls the helper functionas to retrieve the data filters, calculate statistics, and prompt to restart the program"""
    while True:
        city, month, day = get_filters()
        print("Retreiving data for the following: \nCity: {}\nMonth: {}\nDay: {}".format(city,month,day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no: ").lower()

        while True:
            if restart == 'yes' or restart == 'no':
                break
            else:
                restart = input("\nUnexpected input. Would you like to restart? Enter yes or no: ").lower()

        if restart != "yes":
            break
            print("Thank you for your query!")



if __name__ == "__main__":
	main()
