
def get_data(input_date):
        
    import pandas as pd
    import json
    import requests
    import numpy as np
    import requests
    import datetime
    import yfinance as yf
    data= yf.download("AAPL","2018-06-12", input_date)
    stock_info_df= pd.DataFrame(data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']])
    stock_info_df = stock_info_df.sort_values(by='Date',ascending=True)
    stock_info_df.reset_index(drop=False, inplace=True)
    stock_info_df['Date'] = pd.to_datetime(stock_info_df['Date'])



    # Define the start and end dates
    start_date = '2018-01-01'
    end_date = input_date

    # Create an empty list to store the dates
    dates = []

    # Iterate over each month
    for year in range(pd.to_datetime(start_date).year, pd.to_datetime(end_date).year + 1):
        for month in range(1, 13):
            # Create the start and end dates for the current month
            month_start = f"{year}-{month:02d}-01"
            month_end = pd.to_datetime(month_start) + pd.offsets.MonthEnd(0)

            # Generate a range of dates for the current month
            month_dates = pd.date_range(start=month_start, end=month_end, freq='D')

            # Append the dates to the list
            dates.extend(month_dates)

    # Create a DataFrame from the list of dates
    all_days_df = pd.DataFrame({'Date': dates})

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=WIB4EPEUDA7KJFOG'
    r = requests.get(url)
    data_str = r.text

    # Parse the string into a dictionary
    data = json.loads(data_str)

    df_CPI = pd.DataFrame(data['data'])
    df_CPI.rename(columns={'date': 'Date'}, inplace=True)
    df_CPI.rename(columns={'value': 'CPI'}, inplace=True)
    df_CPI = df_CPI[df_CPI['Date'] >= '2018-05-12']
    df_CPI = df_CPI.sort_values(by='Date',ascending=True)
    df_CPI.reset_index(drop=True, inplace=True)
    df_CPI['Date'] = pd.to_datetime(df_CPI['Date'])

    df_CPI_daily = all_days_df.merge(df_CPI, on='Date', how='left')

    df_CPI_daily['CPI'] = df_CPI_daily['CPI'].fillna(method='ffill')

    df_CPI_daily = df_CPI_daily[df_CPI_daily['Date'] >= '2018-06-12']
    df_CPI_daily = df_CPI_daily[df_CPI_daily['Date'] <= input_date]

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=WIB4EPEUDA7KJFOG'
    r = requests.get(url)
    data_str = r.text

    # Parse the string into a dictionary
    data = json.loads(data_str)

    df_interest = pd.DataFrame(data['data'])
    df_interest.rename(columns={'date': 'Date'}, inplace=True)
    df_interest.rename(columns={'value': 'Interest'}, inplace=True)
    # Convert 'Date' column to datetime format
    df_interest['Date'] = pd.to_datetime(df_interest['Date'])

    # Filter the DataFrame
    df_interest = df_interest[df_interest['Date'] >= '2018-06-12']
    df_CPI_daily = df_CPI_daily[df_CPI_daily['Date'] <= input_date]
    df_interest = df_interest.sort_values(by='Date',ascending=True)
    # Convert 'Interest' column to numeric
    df_interest['Interest'] = pd.to_numeric(df_interest['Interest'], errors='coerce')
    df_interest['Interest'] = df_interest['Interest'] / 100
    df_interest.reset_index(drop=True, inplace=True)

    # Convert the 'Date' column in df_interest to datetime data type
    df_interest['Date'] = pd.to_datetime(df_interest['Date'])
    # Convert the 'Date' column in df_CPI to datetime data type

    # Perform the merge
    df_interest_cpi = df_CPI_daily.merge(df_interest, on='Date', how='left')

    # Specify the file path of the CSV file
    csv_file_path = 'AAPL_Financials.csv'

    # Read the CSV file using pandas
    aapl_finances_df = pd.read_csv(csv_file_path)

    #12th junen 2018
    aapl_finances_df = aapl_finances_df.drop(aapl_finances_df[aapl_finances_df.index > 22].index)

    aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'].str.replace('$', '')
    aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'].str.replace('$', '')
    aapl_finances_df['Apple Quarterly EPS'] = aapl_finances_df['Apple Quarterly EPS'].str.replace('$','')
    aapl_finances_df['Apple Quarterly Operating Margin'] = aapl_finances_df['Apple Quarterly Operating Margin'].str.replace('%','')
    # Convert the column to numeric type
    aapl_finances_df['Apple Quarterly Operating Margin'] = pd.to_numeric(aapl_finances_df['Apple Quarterly Operating Margin'], errors='coerce')
    aapl_finances_df['Apple Quarterly Operating Margin'] = aapl_finances_df['Apple Quarterly Operating Margin'] / 100

    aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'].str.replace(',', '.')
    aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'].str.replace(',', '.')
    aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'].str.replace(',', '.')
    aapl_finances_df=aapl_finances_df.sort_values(by='Dates',ascending=True)
    aapl_finances_df.reset_index(drop=True, inplace=True)
    aapl_finances_df.rename(columns={'Dates': 'Date'}, inplace=True)

    # Assuming the DataFrame is already defined as "aapl_finances_df"

    # Convert the "Date" column to datetime format
    aapl_finances_df['Date'] = pd.to_datetime(aapl_finances_df['Date'])

    # Add a new column "Day of Week" representing the day of the week as a number (0-6)
    aapl_finances_df['Day of Week'] = aapl_finances_df['Date'].dt.weekday

    # Assuming the DataFrame is already defined as "aapl_finances_df"

    # Convert the "Date" column to datetime format
    aapl_finances_df['Date'] = pd.to_datetime(aapl_finances_df['Date'])

    # Add a new column "Day of Week" representing the day of the week as a number (0-6)
    aapl_finances_df['Day of Week'] = aapl_finances_df['Date'].dt.weekday

    # Subtract the corresponding value from the day if "Day of Week" is greater than 4
    aapl_finances_df.loc[aapl_finances_df['Day of Week'] > 4, 'Date'] -= pd.to_timedelta(aapl_finances_df['Day of Week'] - 4, unit='D')

    # Update the "Day of Week" column to represent the correct day of the week (4 for values > 4)
    aapl_finances_df['Day of Week'] = aapl_finances_df['Date'].dt.weekday

    aapl_finances_df = aapl_finances_df.drop('Day of Week', axis=1)

    df_EPS=pd.DataFrame(aapl_finances_df[['Date', 'Apple Quarterly EPS']])


    # Convert "Date" column to datetime in df_new
    stock_info_df['Date'] = pd.to_datetime(stock_info_df['Date'])

    # Convert "Date" column to datetime in df_EPS
    df_EPS['Date'] = pd.to_datetime(df_EPS['Date'])

    # Merge df_EPS onto df_new using left merge
    merged_financial_df = stock_info_df.merge(df_EPS, on='Date', how='left')


    import pandas as pd

    # Convert "Date" column to datetime in df_new
    stock_info_df['Date'] = pd.to_datetime(stock_info_df['Date'])

    # Convert "Date" column to datetime in df_EPS
    df_EPS['Date'] = pd.to_datetime(df_EPS['Date'])

    # Merge df_EPS onto df_new using left merge
    merged_financial_df = stock_info_df.merge(df_EPS, on='Date', how='left')

    # Find missing date entries
    missing_dates = df_EPS[~df_EPS['Date'].isin(merged_financial_df['Date'])]

    # Create a new DataFrame with missing dates
    df_new = pd.DataFrame(missing_dates)

    # Add the entries from df_new to merged_financial_df
    merged_financial_df = pd.concat([merged_financial_df, df_new])

    # Sort the DataFrame by the "Date" column
    merged_financial_df = merged_financial_df.sort_values('Date')

    # Reset the index
    merged_financial_df = merged_financial_df.reset_index(drop=True)

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    merged_financial_df['Apple Quarterly EPS'] = merged_financial_df['Apple Quarterly EPS'].fillna(method='ffill')

    merged_financial_df = merged_financial_df.sort_values('Date', ascending=True)
    merged_financial_df['Yearly EPS'] = np.nan

    start_date = pd.to_datetime('2018-06-12')

    merged_financial_df['Apple Quarterly EPS'] = merged_financial_df['Apple Quarterly EPS'].astype(float)

    for index, row in merged_financial_df.iterrows():
        current_date = row['Date']

        if current_date >= start_date:
            previous_values = merged_financial_df[(merged_financial_df['Date'] < current_date) & (~merged_financial_df['Apple Quarterly EPS'].isna())]['Apple Quarterly EPS'].unique()
            if len(previous_values) >= 3:
                previous_values = previous_values[-3:]
                yearly_eps = row['Apple Quarterly EPS'] + previous_values.sum()
                merged_financial_df.at[index, 'Yearly EPS'] = yearly_eps


    # Convert "Date" column to datetime format
    merged_financial_df['Date'] = pd.to_datetime(merged_financial_df['Date'])

    # Calculate the PE ratio
    merged_financial_df['PE'] = merged_financial_df['Close'] / merged_financial_df['Yearly EPS']

    # Filter data from the date 2018-06-29 onwards
    merged_financial_df = merged_financial_df[merged_financial_df['Date'] >= '2018-06-12']

    merged_financial_df = merged_financial_df.copy()
    #merged_financial_df.rename(columns={'Apple Quarterly EPS': 'Quarterly EPS'}, inplace=True)

    aapl_finances_df = all_days_df.merge(aapl_finances_df, on='Date', how='left')

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Revenue\n(Millions of US $)'].fillna(method='ffill')

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'] = aapl_finances_df['Apple Quarterly Net Income\n(Millions of US $)'].fillna(method='ffill')

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    aapl_finances_df['Apple Quarterly Operating Margin'] = aapl_finances_df['Apple Quarterly Operating Margin'].fillna(method='ffill')

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    aapl_finances_df['Apple Quarterly EPS'] = aapl_finances_df['Apple Quarterly EPS'].fillna(method='ffill')

    # Filter the DataFrame to keep only the entries on or after '2018-06-12'
    aapl_finances_df = aapl_finances_df[aapl_finances_df['Date'] >= '2018-06-12']
    aapl_finances_df = aapl_finances_df[aapl_finances_df['Date'] <= input_date]
    # Reset the index of the DataFrame
    aapl_finances_df = aapl_finances_df.reset_index(drop=True)

    df_final = merged_financial_df.merge(aapl_finances_df, on='Date', how='left')

    df_final = df_final.merge(df_interest_cpi, on='Date', how='left')


    import pandas as pd

    # Sorted dates without duplicates
    sorted_dates = [
        '2018-07-12', '2018-09-21', '2018-10-26', '2018-10-30', '2018-11-07',
        '2019-03-18', '2019-03-19', '2019-03-20', '2019-03-25', '2019-05-21',
        '2019-05-28', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06',
        '2019-06-07', '2019-07-09', '2019-08-20', '2019-09-10', '2019-09-20',
        '2019-09-25', '2020-03-18', '2020-04-24', '2020-05-04', '2020-06-22',
        '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-08-04',
        '2020-09-15', '2020-09-18', '2020-10-13', '2020-10-23', '2020-11-10',
        '2020-11-13', '2020-11-16', '2020-11-17', '2020-12-15', '2021-04-20',
        '2021-04-30', '2021-05-21', '2021-07-13', '2021-09-14', '2021-09-24',
        '2021-10-08', '2021-10-18', '2021-10-26', '2021-11-01', '2022-03-08',
        '2022-03-18', '2022-06-06', '2022-06-07', '2022-06-08', '2022-06-09',
        '2022-06-10', '2022-06-24', '2022-07-15', '2022-09-07', '2022-09-16',
        '2022-09-23', '2022-10-07', '2022-10-26', '2022-11-04', '2023-01-24',
        '2023-02-03', '2023-06-05' , '2023-06-06'
    ]

    # Create DataFrame with dates and a column with all entries as "1"
    flag_df = pd.DataFrame({'Date': sorted_dates})
    flag_df['Flag'] = 1

    # Display the DataFrame
    event_dates = flag_df["Date"].to_list()


    # Convert "Date" column to datetime in df_EPS
    flag_df['Date'] = pd.to_datetime(flag_df['Date'])

    # Merge df_EPS onto df_new using left merge
    df_final = df_final.merge(flag_df, on='Date', how='left')
    df_final['Flag'] = df_final['Flag'].fillna(0)


    # Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'PCE',
        'api_key': '55f5943ac55f44a9be924f4751900af3',
        'file_type': 'json',
        'observation_start': '2018-06-12',
        'observation_end': input_date
    }

    r = requests.get(url, params=params)
    data = r.json()
    # Extract the 'observations' list from the JSON data
    observations = data['observations']
    # Create a pandas DataFrame with only 'date' and 'value' columns
    PCE_monthly_df = pd.DataFrame(observations, columns=['date', 'value'])
    # Convert 'value' column to float
    PCE_monthly_df['value'] = PCE_monthly_df['value'].astype(float)
    PCE_monthly_df.rename(columns={'date': 'Date'}, inplace=True)
    PCE_monthly_df.rename(columns={'value': 'PCE'}, inplace=True)

    # Calculate the slope using linear regression
    values = PCE_monthly_df['PCE'].values
    time = np.arange(len(values))
    slope, _ = np.polyfit(time, values, 1)

    # Get the last date in the DataFrame
    last_date = datetime.datetime.strptime(PCE_monthly_df['Date'].iloc[-1], '%Y-%m-%d')

    # Generate the next two months' dates (first day of the month)
    next_date_1 = datetime.datetime(last_date.year, last_date.month + 1, 1)
    next_date_2 = datetime.datetime(last_date.year, last_date.month + 2, 1)

    # Create a DataFrame with the extrapolated dates
    extrapolated_dates = pd.DataFrame({'Date': [next_date_1, next_date_2]})

    # Extrapolate the next two months' values based on the calculated slope
    extrapolated_values = values[-1] + slope * (len(values) + np.arange(2))

    # Add the extrapolated values to the DataFrame
    extrapolated_dates['PCE'] = extrapolated_values

    # Concatenate the extrapolated dates DataFrame with the original DataFrame
    extrapolated_df = pd.concat([PCE_monthly_df, extrapolated_dates])

    extrapolated_df['Date'] = pd.to_datetime(extrapolated_df['Date']).dt.strftime('%Y-%m-%d')
    # Round the values in the 'PCE' column to one decimal point
    extrapolated_df['PCE'] = extrapolated_df['PCE'].round(1)

    extrapolated_df = extrapolated_df.reset_index(drop=True)

    # Convert 'Date' column to datetime format
    extrapolated_df['Date'] = pd.to_datetime(extrapolated_df['Date'])

    # Create a new DataFrame with a 'Date' column containing all dates from 2018-06-01 to 2023-06-30
    date_range = pd.date_range(start='2018-06-01', end=input_date, freq='D')
    new_2_df = pd.DataFrame({'Date': date_range})

    # Convert 'Date' column to datetime format
    new_2_df['Date'] = pd.to_datetime(new_2_df['Date'])

    # Merge the new DataFrame with 'extrapolated_df' based on the 'Date' column
    PCE_daily_df = pd.merge(new_2_df, extrapolated_df, on='Date', how='left')

    # Forward fill the 'PCE' column to fill missing values with the corresponding month's constant value
    PCE_daily_df['PCE'] = PCE_daily_df['PCE'].fillna(method='ffill')


    # Convert "Date" column to datetime in df_new
    PCE_daily_df['Date'] = pd.to_datetime(PCE_daily_df['Date'])

    # Merge df_EPS onto df_new using left merge
    df_final = df_final.merge(PCE_daily_df, on='Date', how='left')


    # Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'VIXCLS',
        'api_key': '55f5943ac55f44a9be924f4751900af3',
        'file_type': 'json',
        'observation_start': '2018-06-12',
        'observation_end': input_date
    }

    r = requests.get(url, params=params)
    data = r.json()

    # Extract the 'observations' list from the JSON data
    observations = data['observations']

    # Create a pandas DataFrame with only 'date' and 'value' columns
    vix_daily_df = pd.DataFrame(observations, columns=['date', 'value'])

    vix_daily_df.rename(columns={'date': 'Date'}, inplace=True)
    vix_daily_df.rename(columns={'value': 'VIX'}, inplace=True)
    
    # Convert "Date" column to datetime in df_new
    vix_daily_df['Date'] = pd.to_datetime(vix_daily_df['Date'])

    # Merge df_EPS onto df_new using left merge
    df_final = df_final.merge(vix_daily_df, on='Date', how='left')

    symbol = "^VIX"
    data = yf.Ticker(symbol)
    historical_data = data.history(period="5d")  # Fetching data for a longer period (5 days)
    previous_close = historical_data["Close"].iloc[-2]  # Using iloc to retrieve the second-to-last value
    df_final.loc[df_final.index[-1], "VIX"] = previous_close

    df_final['Interest'] = df_final['Interest'].fillna(method='ffill')

    df_final = df_final.drop('Apple Quarterly EPS_y', axis=1)
    df_final.rename(columns={'Apple Quarterly EPS_x': 'Quarterly EPS'}, inplace=True)
    df_final.rename(columns={'Apple Quarterly Revenue\n(Millions of US $)': 'Quarterly Revenue'}, inplace=True)
    df_final.rename(columns={'Apple Quarterly Net Income\n(Millions of US $)': 'Quarterly Net Income'}, inplace=True)
    df_final.rename(columns={'Apple Quarterly Operating Margin': 'Quarterly Operating Margin'}, inplace=True)

    return df_final
