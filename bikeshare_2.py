import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    flagName = False
    while not flagName:
        city = input('Let\'s choose a city from: Washington, Chicago or New York City: ').lower()
        if (city == 'washington') or (city == 'chicago') or (city == 'new york city'):
            flagName = True
        else:
            print('That\' not a valid name though, is it? Take a deep breath, a sip of water, contemplate the vastness of the cosmos and let\'s try again.')

    flagName = False
    while not flagName:
        month = input('Would you also like to filter by a specific month?\nPlease enter full name for a month between January and June (e.g.\'March\') or \'all\' if no filter: ').lower()
        if month in ("january", "february", "march", "april", "may", "june", "all"):
            flagName = True
        else:
            print('Looks like you\'ve entered an invalid name. Let\'s try again, shall we?: ')

    flagName = False
    while not flagName:
        day = input('Would you like to filter by a specific weekday?\nPlease enter the name of the day of week if yes, or \'all\' if none: ').lower()
        if day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"):
            flagName = True
        else:
            print('Looks you\'ve entered an invalid name. Let\'s try again, shall we?: ')
    day = day.title()
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_the_week'] = df['Start Time'].dt.weekday_name


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df[df['month'] == month]


    if day != 'all' and day != 'All':
        df = df[df['day_of_the_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    most_common_month = df['Start Time'].dt.month.mode()[0]
    most_common_month = months[most_common_month]
    most_common_dow = df['Start Time'].dt.weekday_name.mode()[0]
    most_common_start_hour = df['hour'].mode()[0]

    # display the most common month
    print("The most common month is {}".format(most_common_month.title()))

    # display the most common day of week
    print("The most common day of the week is {}".format(most_common_dow))

    # display the most common start hour
    print("The most common start hour is {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_common_strt_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    df['Start-End Station'] = df['Start Station'] + " - " +  df['End Station']
    most_frequent_comb = df['Start-End Station'].mode()[0]

    # display most commonly used start station
    print("The most commonly used start station is {}".format(most_common_strt_station))

    # display most commonly used end station
    print("The most commonly used end station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip is \"{}\"".format(most_frequent_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    # display total travel time
    print('The total travel time is {}'.format(total_travel_time))

    # display mean travel time
    print('The average travel time is {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_type_cnt = df['User Type'].value_counts()

    # Display counts of user types
    print("Below you can see what and how many User Types there are:\n")
    print(user_type_cnt)

    try:
        # Display counts of gender
        gender_cnt = df['Gender'].value_counts()
        min_yob = df['Birth Year'].min()
        max_yob = df['Birth Year'].max()
        mode_yob = df['Birth Year'].mode()[0]
        print("\nBelow you can see the total number of users by gender:\n")
        print(gender_cnt)

        # Display earliest, most recent, and most common year of birth
        print("\nBelow you can see, in sequence, the earliest, most recent and most common year of birth amongst our users:\n")
        print(int(min_yob))
        print(int(max_yob))
        print(int(mode_yob))
    except KeyError:
        print("\nThere is no data available for Washington\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Provides option to see file's raw data, 5 lines at a time.
    User can choose between 'yes' or 'no' input.

    """
    index_from = 0
    index_to = 5
    while True:
        raw_data = input("Would you like to see some raw data?\nPlease type \'yes\' or \'no\': ").lower()
        if raw_data != 'no':
            print(df.iloc[index_from:index_to])
            index_from += 5
            index_to += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
