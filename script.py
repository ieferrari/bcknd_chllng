import pandas as pd
from fuzzywuzzy import fuzz
from collections import Counter
from typing import List
import typer


# default values
MIN_FUZZY_DIST = 60
INPUT_FILE = "patent-backend-challenge.csv"
COMPANY_SUFFIXES = ["LLC", "LLP", "LTD", "INC"]


def fuzzy_fix_column(df: pd.DataFrame,
                     target_col: str,
                     grouped_by_list: List[str],
                     min_fuzzy_dist: int) -> pd.DataFrame:
    # Fix city names grouped by country
    for cities in df.groupby(grouped_by_list)[target_col].apply(list):
        # assuming the errors are minotrity, we order with top occurences first
        cities = Counter(cities)
        cities = dict(cities) 
        fix_cities = {}
        cities_to_match = cities
        for city_a in cities:
            for city_b in cities_to_match:
                # skip if the second city has been already mapped
                if city_b not in fix_cities.keys():
                    # fuzzy distance between words
                    dist = fuzz.ratio(city_a, city_b)
                    if dist > min_fuzzy_dist:
                        if city_a != city_b:
                            # add to the dict {wrong_str: fixed_str}
                            fix_cities[city_b] = city_a
        # It's actually much faster to use str.replace() than replace(),
        # even though str.replace() requires a loop:
        # https://stackoverflow.com/questions/46342492/use-dictionary-to-replace-a-string-within-a-string-in-pandas-columns
        for old, new in fix_cities.items():
            df[target_col] = df[target_col].str.replace(old, new, regex=False)
    return df


def remove_punctuation_signs(df: pd.DataFrame,
                             target_col: str) -> pd.DataFrame:
    df[target_col] = df[target_col].str.replace('[^\w\s]', '', regex=True)
    return df


def remove_company_suffixes(df: pd.DataFrame,
                            target_col: str,
                            company_suffixes: List[str]) -> pd.DataFrame:
    df[target_col] = df[target_col].str.\
        replace('|'.join(company_suffixes), '', regex=True)
    return df


def remove_multiple_white_spaces(df: pd.DataFrame,
                                 target_col: str) -> pd.DataFrame:
    df[target_col] = df[target_col].str.replace(r'\s+', ' ', regex=True)
    return df


def remove_trailing_white_space(df: pd.DataFrame,
                                target_col: str) -> pd.DataFrame:
    df[target_col] = df[target_col].str.replace(r"^ +| +$", r"", regex=True)
    return df


app = typer.Typer()


@app.command()
def fix_csv(input_file: str = INPUT_FILE,
            min_fuzzy_dist: int = MIN_FUZZY_DIST,
            company_suffixes: List[str] = COMPANY_SUFFIXES):
    """Take a .csv file as input, will use fuzzy match to
      fix the cities names (grouped by country)
    fix the organization name (grouped by country & city)
    output the fixed .csv file adding the fixed_ prefix to input_file name

    Args:
        input_file (str, optional): input .csv file to fix.
        min_fuzzy_dist (int, optional): tune the fuzzy match algorithm.
        company_suffixes (List[str], optional): expressions to remove from
        the organization column.
    """
    df = pd.read_csv(input_file)

    unique_orgs = len(df["organization"].unique())
    print(f"input file: {input_file} , \t unique organizations: {unique_orgs}")

    df = fuzzy_fix_column(df,
                          target_col="city",
                          grouped_by_list=["country"],
                          min_fuzzy_dist=min_fuzzy_dist)
    df = remove_punctuation_signs(df, target_col="organization")
    df = remove_company_suffixes(df,
                                 target_col="organization",
                                 company_suffixes=company_suffixes)
    df = remove_multiple_white_spaces(df, target_col="organization")
    df = remove_trailing_white_space(df, target_col="organization")
    df = fuzzy_fix_column(df,
                          target_col="organization",
                          grouped_by_list=["country", "city"],
                          min_fuzzy_dist=min_fuzzy_dist)

    unique_orgs = len(df["organization"].unique())
    output_file = "fixed_" + input_file
    print(f"input file: {output_file} ,\t unique organizations: {unique_orgs}")

    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    app()
