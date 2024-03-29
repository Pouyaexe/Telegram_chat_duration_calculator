# an app to convert jason to df
import json
import pandas as pd  # pd is used for dataframes


# load data using Python JSON module
with open("result.json", "r", encoding="utf8") as f:
    data = json.loads(f.read())
# Flatten data
df = pd.json_normalize(data, record_path=["messages"])

total_messages = len(df)


# extracting the the 'date' column from the dataframe into a new dataframe
def extract_date(df):
    df_date = df.loc[:, ["date"]]
    return df_date


unique_users = df["from"].unique()

if len(unique_users) < 2:
    print("Not enough unique users in the chat.")
else:
    x = unique_users[0]
    y = unique_users[1]


dfs = extract_date(df)

# convert the 'date' column to datetime

dfs["date"] = pd.to_datetime(dfs["date"])

# saving df as csv
dfs.to_csv("data.csv", index=False)


# calculating the difference between the dates into a new dataframe
def diff_date(df):
    df_diff = df.loc[:, ["date"]]
    df_diff["date"] = df_diff["date"].diff()
    return df_diff


df_diff = diff_date(dfs)


# converting the difference to to seconds and save it to a new dataframe
def diff_to_seconds(df):
    df_diff_seconds = df.loc[:, ["date"]]
    df_diff_seconds["date"] = df_diff_seconds["date"].dt.total_seconds()
    return df_diff_seconds


df_diff_seconds = diff_to_seconds(df_diff)

# adding all rows that are less than 15 minimumutes to a new dataframe


def less_than_15_minutes(df):
    df_less_than_15_minutes = df.loc[df["date"] < 900, :]
    return df_less_than_15_minutes


df_less_than_15_minutes = less_than_15_minutes(df_diff_seconds)

# Now calculating the sum of all of the rows in date column

sum = df_less_than_15_minutes.sum().iloc[0]
# sum is in seconds, converting it the date format and printing it
import datetime, time

print("Total Messages between", x, "and", y, ":", total_messages)

print("Days, Hours:Minutes:Seconds")
print(datetime.timedelta(seconds=sum))
