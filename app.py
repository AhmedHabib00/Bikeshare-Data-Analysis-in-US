import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
is_washington = False


def get_month():
    month = input('Please Enter a month')
    while month.lower() not in months and month.lower() != 'all':
        month = input('ERROR! Please enter a valid month ')
        # use the index of the months list to get the corresponding int
    if month.lower() != 'all':
        month = months.index(month) + 1
    return month


def get_day():
    day = input('Please Enter a day')
    while day.lower() not in days and day.lower() != 'all':
        day = input('ERROR! Please enter a valid day ')
    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # global months
    global is_washington
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York or Washington?')
    while city.lower() not in CITY_DATA:
        city = input('Error! please enter a valid input')
    if city.lower() == 'washington':
        is_washington = True
    # TO DO: get user input for month (all, january, february, ... , june)
    flag = True
    filter = input(
        'Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter ')
    while flag:
        if filter.lower() == 'month':
            month = get_month()
            day = 'all'
            flag = False
        elif filter.lower() == 'day':
            day = get_day()
            month = 'all'
            flag = False
        elif filter.lower() == 'both':
            month = get_month()
            day = get_day()
            flag = False
        elif filter.lower() == 'none':
            month = 'all'
            day = 'all'
            flag = False
        else:
            filter = input(
                'Error! Please enter a valid filter; Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print('-' * 40)
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print(f"The most common month is: {df['month'].mode()[0]}")

    # TO DO: display the most common day of week
    print(f"The most common day of week is: {df['day_of_week'].mode()[0]}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print(f"The most common start hour is:  {df['hour'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(f"The Most Common Starting Destination is : {df['Start Station'].mode()[0]}")

    # TO DO: display most commonly used end station
    print(f"The Most Common End Destination is : {df['End Station'].mode()[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    most_freq_idx = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The Most Common Combination of Start Station and End Station are: ', most_freq_idx)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print(f"The Total Travel Time is: {total_duration} seconds")

    # TO DO: display mean travel time
    avg_travel_time = total_duration / df['Start Time'].count()
    print(f"The mean travel time is {avg_travel_time} hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    global is_washington
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types are.. ')
    print(user_types)
    # TO DO: Display counts of gender
    if is_washington == False:
        print('The counts of gender are.. ')
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print(
            f'The earliest year of birth is {int(earliest)} while the most recent is {int(most_recent)} and the most common is {int(most_common)}')
    else:
        print('Sorry The information about gender and birth year are not available for Washington')
    view_data = input('Would you like to view 5 rows of individual trip data? y/n')
    start_loc = 0
    while view_data.lower() == 'yes' or view_data.lower() == 'y':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
