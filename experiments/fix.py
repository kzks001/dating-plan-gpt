import pandas as pd
from typing import Any
from loguru import logger
from dateutil.parser import parse


def convert_time(row: pd.Series) -> pd.Series:
    """
    Convert time to 24-hour format and split the rows into day_open and day_close for the operating hours.

    Args:
        row (pd.Series): A row of the DataFrame.

    Returns:
        pd.Series: The updated row with new columns for each day's opening and closing times.
    """
    # Define the days of the week
    days = [
        "Monday_hours",
        "Tuesday_hours",
        "Wednesday_hours",
        "Thursday_hours",
        "Friday_hours",
        "Saturday_hours",
        "Sunday_hours",
    ]

    # Iterate over each day
    for day in days:
        # Check if the day is not closed and not open 24 hours
        if row[day] != "Closed" and row[day] != "Open 24 hours":
            # Check if the day contains two ranges of time
            if "," in row[day]:
                logger.info(f"Removing row due to multiple time ranges: {row['name']}")
                return None
            # Split the opening and closing times
            times = row[day].split(" to ")
            # Check if there are opening and closing times
            if len(times) == 2:
                open_time, close_time = times
                # Convert the times to 24-hour format
                open_time = parse(open_time).strftime("%H:%M")
                close_time = parse(close_time).strftime("%H:%M")
                # Add the new columns to the row
                row[day + "_open"] = open_time
                row[day + "_close"] = close_time
            else:
                logger.info(f"Unexpected time format in row: {row['name']}")
                return None
        # Check if the day is open 24 hours
        elif row[day] == "Open 24 hours":
            row[day + "_open"] = "00:00"
            row[day + "_close"] = "23:59"
        # If the day is closed
        else:
            row[day + "_open"] = "Closed"
            row[day + "_close"] = "Closed"
    return row


def main():
    # Load the CSV data into a DataFrame
    df = pd.read_csv("data/main_short.csv")

    # Apply the function to the DataFrame
    df = df.apply(convert_time, axis=1)

    # Remove rows with None (those with multiple time ranges or unexpected time format)
    df = df.dropna()

    # Drop the original columns
    df = df.drop(
        columns=[
            "Monday_hours",
            "Tuesday_hours",
            "Wednesday_hours",
            "Thursday_hours",
            "Friday_hours",
            "Saturday_hours",
            "Sunday_hours",
        ]
    )

    # Save the DataFrame back to a CSV file
    df.to_csv("new_file.csv", index=False)


if __name__ == "__main__":
    main()
