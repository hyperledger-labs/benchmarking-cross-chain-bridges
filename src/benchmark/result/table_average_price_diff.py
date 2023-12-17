import pandas as pd
import numpy as np

# Create empty DataFrames
avg_table_df = pd.DataFrame(columns=['aggregator', 'source-chain', 'dest-chain', 'avg-over', 'avg-under', 'avg-diff', 'total-count'])
count_over_table_df = pd.DataFrame(columns=['aggregator', 'source-chain', 'dest-chain', '<1\%', '<5\%', '<10\%', '<20\%', '<30\%', '>=30\%'])
count_under_table_df = pd.DataFrame(columns=['aggregator', 'source-chain', 'dest-chain', '<-1\%', '<-5\%', '<-10\%', '<-20\%', '<-30\%','>=-30\%'])

def table_average_price_diff(coin_gecko_prices, quote_value, aggregator, source_chain, dest_chain):
    global avg_table_df, count_over_table_df, count_under_table_df  # Ensure you are referencing the global variables

    price_diff = quote_value - coin_gecko_prices

    price_diff_over = price_diff[quote_value > coin_gecko_prices]
    price_diff_under = price_diff[quote_value < coin_gecko_prices]

    avg_price_diff_over = np.mean(price_diff_over) 
    avg_price_diff_under = -1 * np.mean(price_diff_under)
    avg_price_diff = np.mean(price_diff) if len(price_diff) > 0 else 0

    # Round to 2 decimal places
    avg_price_diff_over = round(avg_price_diff_over, 2)
    avg_price_diff_under = round(avg_price_diff_under, 2)
    avg_price_diff = round(avg_price_diff, 2)
    total_count = len(price_diff)

    # Create a new DataFrame for the current data (avg_table_df)
    avg_data = pd.DataFrame({
        'aggregator': [aggregator],
        'source-chain': [source_chain],
        'dest-chain': [dest_chain],
        'avg-over': [avg_price_diff_over],
        'avg-under': [avg_price_diff_under],
        'avg-diff': [avg_price_diff],
        'total-count': [total_count]
    })

    # Concatenate the new data with the existing data for avg_table_df
    avg_table_df = pd.concat([avg_table_df, avg_data], ignore_index=True)

    over_1 = np.sum(price_diff_over < 1)
    over_5 = np.sum((price_diff_over < 5) & (price_diff_over >= 1))
    over_10 = np.sum((price_diff_over < 10) & (price_diff_over >= 5))
    over_20 = np.sum((price_diff_over < 20) & (price_diff_over >= 10))
    over_30 = np.sum((price_diff_over < 30) & (price_diff_over >= 20))
    over_beyond_30 = np.sum(price_diff_over >= 30)

    # Create DataFrames for count_over_table_df and count_under_table_df
    count_data_over = pd.DataFrame({
        'aggregator': [aggregator],
        'source-chain': [source_chain],
        'dest-chain': [dest_chain],
        '<1\%': [over_1],
        '<5\%': [over_5],
        '<10\%': [over_10],
        '<20\%': [over_20],
        '<30\%': [over_30],
        '>=30\%': [over_beyond_30],
    })

    under_1 = np.sum(price_diff_under > -1)
    under_5 = np.sum((price_diff_under > -5) & (price_diff_under < -1))
    under_10 = np.sum((price_diff_under > -10) & (price_diff_under < -5))
    under_20 = np.sum((price_diff_under > -20) & (price_diff_under < -10))
    under_30 = np.sum((price_diff_under < -20) & (price_diff_under >= -30))
    under_beyond_30 = np.sum(price_diff_under < -30)

    count_data_under = pd.DataFrame({
        'aggregator': [aggregator],
        'source-chain': [source_chain],
        'dest-chain': [dest_chain],
        '<-1\%': [under_1],
        '<-5\%': [under_5],
        '<-10\%': [under_10],
        '<-20\%': [under_20],
        '<-30\%': [under_30],
        '>=-30\%': [under_beyond_30],
    })

    # Concatenate the new data with the existing data for count_over_table_df
    count_over_table_df = pd.concat([count_over_table_df, count_data_over], ignore_index=True)

    # Concatenate the new data with the existing data for count_under_table_df
    count_under_table_df = pd.concat([count_under_table_df, count_data_under], ignore_index=True)

    avg_table_df.fillna(0, inplace=True)
    count_over_table_df.fillna(0, inplace=True)
    count_under_table_df.fillna(0, inplace=True)

    return {
        'avg_table_df': avg_table_df,
        'count_over_table_df': count_over_table_df,
        'count_under_table_df': count_under_table_df
    }