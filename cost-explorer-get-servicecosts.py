import boto3
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create a Cost Explorer client
ce = boto3.client('ce')

# Define the granularity and metrics
granularity = 'MONTHLY'
metrics = ['BlendedCost']
groupby = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]

# Initialize the DataFrame
df = pd.DataFrame()

# Get the cost and usage for the past 6 months
for i in range(6):
    # Calculate the start and end dates for the month
    today = datetime.now()
    end_date = today.replace(day=1) - relativedelta(days=1) - relativedelta(months=i)
    start_date = end_date.replace(day=1)
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    
    # Get the cost and usage
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end,
        },
        Granularity=granularity,
        Metrics=metrics,
        GroupBy=groupby,
    )
    
    # Process the response and create a DataFrame for the current month
    data = []
    for item in response['ResultsByTime']:
        for group in item['Groups']:
            service = group['Keys'][0]
            cost = round(float(group['Metrics']['BlendedCost']['Amount']), 1)
            data.append([service, cost])
    
    # Create a DataFrame for the current month and sort it by cost
    month_df = pd.DataFrame(data, columns=['Service', start_date.strftime('%B %Y')])
    month_df = month_df.sort_values(start_date.strftime('%B %Y'), ascending=False)
    
    # Select the top 10 most expensive services
    top_10_month_df = month_df.head(10)
    
    # Merge the current month's top 10 DataFrame with the main DataFrame
    if df.empty:
        df = top_10_month_df
    else:
        df = pd.merge(df, top_10_month_df, on='Service', how='outer')

# Fill NaN values with 0
df = df.fillna(0)

# Save the DataFrame to a text file
output_file = 'top_10_service_cost_past_six_months.txt'
df.to_csv(output_file, sep='\t', index=False)

print(f'Data saved to {output_file}')
