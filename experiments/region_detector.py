import pandas as pd
import re
from typing import List, Optional
from loguru import logger
from langchain.tools import GooglePlacesTool


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(file_path)


def convert_postcodes_to_list(postcodes: str) -> List[int]:
    """
    Convert a string of postcodes to a list of integers.

    Args:
        postcodes (str): The string of postcodes.

    Returns:
        List[int]: The list of postcodes as integers.
    """
    return [int(i) for i in postcodes.strip("[]").split(", ")]


def return_postal(place: str) -> Optional[int]:
    """
    Get the postal code of a place.

    Args:
        place (str): The name of the place.

    Returns:
        Optional[int]: The postal code of the place, or None if the postal code is not an integer.
    """
    places = GooglePlacesTool()
    try:
        return int(places.run(place).split("\n")[1][-6:-4])
    except ValueError:
        logger.error(f"Postal code for {place} is not an integer.")
        return None


def find_region(postal_code: Optional[int], regions_df: pd.DataFrame) -> str:
    """
    Find the region corresponding to a postal code.

    Args:
        postal_code (Optional[int]): The postal code.
        regions_df (pd.DataFrame): The DataFrame containing the regions and postcodes.

    Returns:
        str: The region corresponding to the postal code, or 'Unknown' if the postal code is None.
    """
    if postal_code is None:
        return "Unknown"
    for i, row in regions_df.iterrows():
        if postal_code in row["Postcodes"]:
            return row["Region"]
    return "Unknown"


def main():
    # Load the CSV files
    logger.info("Loading CSV files...")
    places_df = load_csv("./data/data.csv")
    regions_df = load_csv("./data/postcode_data.csv")

    # Convert the Postcodes column to lists of integers
    logger.info("Converting postcodes to lists of integers...")
    regions_df["Postcodes"] = regions_df["Postcodes"].apply(convert_postcodes_to_list)

    # Add Region columns
    logger.info("Adding Region...")
    places_df["Region"] = places_df["location"].apply(
        lambda x: find_region(return_postal(x), regions_df)
    )

    # Save the updated dataframe to a new CSV file
    logger.info("Saving the updated DataFrame to a new CSV file...")
    places_df.to_csv("data/main.csv", index=False)
    logger.info("Done.")


if __name__ == "__main__":
    main()
