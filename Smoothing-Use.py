# -*- coding: utf-8 -*-
"""
Created on Tue May 21 00:48:36 2024

@author: LocalAdmin
"""

import pandas as pd
# Sample data
data = {
    'frameNum': [0, 1, 2, 3, 9, 5, 6, 0, 1, 2, 3, 9, 5, 6],
    'carId': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    'carCenterXm': [52.86706821, 115.4478321, 114.8895738, 254.342516, 204.8808239, 28.86195803, 205.9415149, 155.1958285, 148.7758572, 271.536874, 52.64376484, 76.03479078, 114.3871412, 253.9517352],
    'carCenterYm': [13.17489767, 28.41535133, 32.15568244, 24.17258768, 23.50267762, 25.56823362, 31.15081737, 30.92751404, 28.08039631, 23.89345849, 13.00742016, 27.24300874, 32.15568244, 24.28423935],
    'speed(m/s)': [8.06966946, 17.39293141, 13.79922428, 9.590399998, 12.59096735, 19.48971936, 14.39808208, 14.68835784, 16.5080027, 8.995993615, 8.06966946, 19.80062355, 13.79922428, 9.590399998],
    'heading': [33.30021297, 359.7088833, 359.5788152, 359.6874366, 359.5720149, 359.5031635, 359.5185343, 359.771754, 359.6931661, 359.7761722, 33.04198877, 359.444905, 359.6648408, 359.6874366],
    # Add other columns if needed
}
df = pd.DataFrame(data) # When reading from csv file: df = pd.read_csv('your_data.csv')
# Define exponential smoothing function
def exponential_smoothing(series, alpha):
    result = [series[0]]  # First value remains unchanged
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result
# Function: Apply smoothing to specified columns of the dataframe
def smooth_dataframe(df, columns, alpha):
    smoothed_data = df.copy()
    df = df.reset_index()
    for column in columns:
        smoothed_data[column] = exponential_smoothing(df[column], alpha)
    return smoothed_data

# Process each carId separately
smoothed_data = []
#Specify the columns to apply exponential smoothing; One can adjust this accordingly
columns_to_smooth = ['carCenterXm', 'carCenterYm', 'speed(m/s)', 'heading']
# Set the alpha value for smoothing.
#The higher the alpha value, the closer the smoothed data will be to the original data. 
alpha = 0.99  # One can adjust this value to change the smoothing effect
for car_id, group in df.groupby('carId'):
    group=group.sort_values(by=['frameNum'])
    group = group.reset_index(drop=True)
    start_idx = 0
    for i in range(1, len(group)):
        if group['frameNum'][i] != group['frameNum'][i-1] + 1:
            # frameNum is not continuous, process the previous series
            sub_group = group.iloc[start_idx:i]
            smoothed_sub_group = smooth_dataframe(sub_group, columns_to_smooth, alpha)
            smoothed_data.append(smoothed_sub_group)
            start_idx = i
    # Process the last series
    sub_group = group.iloc[start_idx:]
    smoothed_sub_group = smooth_dataframe(sub_group, columns_to_smooth, alpha)
    smoothed_data.append(smoothed_sub_group)
# Combine the processed data
result_df = pd.concat(smoothed_data).sort_values(by=['carId', 'frameNum'])
print(result_df) # Print the result; Optional, skip this when processing large amount of data
# Save to CSV file
result_df.to_csv('smoothed_data.csv', index=False)
