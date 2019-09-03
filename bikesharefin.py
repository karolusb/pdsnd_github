import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'c':'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Please select a city (chicago or c, new york city or ny , or washington or w): ").lower()
        if city not in (CITY_DATA):
            print("I did not understand your choice, please try again.")
        else:
            break

    print('Great! You selected ' + city + '.')

    while True:
        month = input('Please select the month you wish to view, or select all (months are january, february, march, april, may, june):').lower()
        if month not in (months) and month != 'all':
            print("I did not understand your choice, please try again.")
        else:
            break
    print('Great! You selected ' + month + '.')

    while True:
        day = input('Please select the day you wish to view, or select all (days are sunday, monday, tuesday, wednesday, thursday, friday, saturday):').lower()
        if day not in (days) and day != 'all':
            print("I did not understand your choice, please try again.")
        else:
            break
    print('Great! You selected ' + day + '.')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format=True)
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    # we will want this one later
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most commonly traveled month was:", popular_month)
    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print("The most commonly traveled day was:", popular_day)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most commonly traveled hour was:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most popular starting location was:", popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most popular ending location was:", popular_end)
    # TO DO: display most frequent combination of start station and end station trip

    popular_trip = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most popular trip was from {} to {}".format(popular_trip[0], popular_trip[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = round(df['Trip Duration'].sum() / 60, 2)
    print("The total travel time for the selected period was {} minutes.".format(total_trip_duration))


    # display mean travel time
    avg_trip_duration = round(df['Trip Duration'].mean() / 60, 2)
    print("The average travel time for the selected period was {} minutes.".format(avg_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#### We are solid to this point.
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for  user, count in df['User Type'].value_counts().items():
        print('\nThere were {} {}s'.format(count, user))

    # Display counts of gender
    try:
        for  mf, count in df['Gender'].value_counts().items():
            print('\nThere were {} {}s'.format(count, mf))
    except:
        print('\nGender data not available')
    # Display earliest, most recent, and most common year of birth
    try:
        early = int(df['Birth Year'].min())
        late = int(df['Birth Year'].max())
        m_c = int(df['Birth Year'].mode()[0])
        print(('\nThe earliest birth year was {}, the latest birth year was {},'
        + '\nand the most common birth year was {}.').format(early, late, m_c))
    except:
        print('\nBirth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    while True:
        n = 0
        view_data = input('\nWould you like to view the raw data?\n').lower()
        while view_data == 'yes':
            print(df.iloc[n:n+5])
            n += 5
            view_data = input('\nWould you like to see more data?\n').lower()
        if view_data != 'yes':
            break

def main():
    pd.set_option('display.max_columns', None)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            print('\nThank you for using bikeshare.py')
            break


if __name__ == "__main__":
	main()
