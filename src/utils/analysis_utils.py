"""
This module provides functions to analyze the structure and data types of a pandas
DataFrame.

It includes functions to get details about the DataFrame's structure,
the data types present in the DataFrame, statistics about the object fields in the
DataFrame, and descriptive statistics about the object fields in the DataFrame.

These functions can be used for exploratory data analysis and to gain insights about
the data contained in a DataFrame.
"""
import pandas as pd


def dataframe_structure(dataframe: pd.DataFrame) -> dict:
    """
    This function takes a pandas DataFrame as input and returns a dictionary
    containing details about its structure.

    Args:
        dataframe (pd.DataFrame): The DataFrame to analyze.

    Returns:
        dict: A dictionary containing details about the structure of the DataFrame.
    """
    structure_details = {
        "Dimensions": dataframe.ndim,
        "Shape": dataframe.shape,
        "Row Count": len(dataframe),
        "Column Count": len(dataframe.columns),
        "Total Datapoints": dataframe.size,
        "Null Datapoints": dataframe.isnull().sum().sum(),
        "Non-Null Datapoints": dataframe.notnull().sum().sum(),
        "Total Memory Usage": dataframe.memory_usage(deep=True).sum(),
        "Average Memory Usage": dataframe.memory_usage(deep=True).mean().round(),
    }

    return structure_details


def datatype_details(dataframe: pd.DataFrame) -> str:
    """
    This function takes a pandas DataFrame as input and returns a string describing
    the datatypes present in the DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame to analyze.

    Returns:
        str: A string describing the datatypes present in the DataFrame.
    """
    available_dtypes = list({str(dt) for dt in dataframe.dtypes})
    for dt in available_dtypes:
        field_count = dataframe.select_dtypes(dt).dtypes.count()
        return f"There are {field_count} fields with {dt} datatype"


def object_fields_count_stats(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a pandas DataFrame as input and returns a DataFrame containing
    statistics about the object fields in the input DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing statistics about the object fields in
        the input DataFrame.
    """

    object_field_count_stats = []

    for col in dataframe.select_dtypes("object").columns:

        row_count = len(dataframe)
        unique_values_count = dataframe[col].nunique()
        distinct_values_count = (dataframe[col].value_counts() == 1).sum()
        null_values_count = dataframe[col].isnull().sum()
        notnull_values_count = dataframe[col].notnull().sum()

        count_stats = {
            "column": col,
            "total_rows": row_count,
            "null_rows": null_values_count,
            "not_null_rows": notnull_values_count,
            "unique_item_count": unique_values_count,
            "distinct_item_count": distinct_values_count,
        }

        object_field_count_stats.append(count_stats)

    return pd.DataFrame(object_field_count_stats).set_index("column")


def describe_object_fields(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a pandas DataFrame as input and returns a DataFrame containing
    descriptive statistics about the object fields in the input DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing descriptive statistics about the object
        fields in the input DataFrame.
    """
    object_field_stats = []

    for col in dataframe.select_dtypes("object").columns:
        count = dataframe[col].notnull().sum()
        unique_values = dataframe[col].nunique()
        longest_value = dataframe[col].str.len().max()
        average_length_value = round(dataframe[col].str.len().mean(), 1)
        shortest_value = dataframe[col].str.len().min()
        max_value_count = (dataframe[col].str.len() == longest_value).sum()
        min_value_count = (dataframe[col].str.len() == shortest_value).sum()

        summary_stats = {
            "column": col,
            "count": count,
            "unique_values": unique_values,
            "longest_values": longest_value,
            "average_length_value": average_length_value,
            "shortest_value": shortest_value,
            "max_value_count": max_value_count,
            "min_value_count": min_value_count,
        }

        object_field_stats.append(summary_stats)

    return pd.DataFrame(object_field_stats).set_index("column")
