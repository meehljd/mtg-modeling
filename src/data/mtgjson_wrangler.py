"""Wrangle the MTG JSON AllPrices.JSON Data"""

import os
from pathlib import Path
import pandas as pd
import polars as pl


class MtgPricesJsonWrangler:
    def __init__(
        self,
        paths: dict,
        filename: str = None,
        interim_filename: str = "nested_prices.parquet",
    ):
        self.paths = paths

        self.meta_filename = "meta.parquet"
        self.interim_filename = interim_filename
        self.final_filename = filename

        self._validate_paths()

    def unstack_data(self):
        """Unstack the data from the interim directory and save to interim directory.

        The data is unstacked and saved to the interim directory.  The data is

        """
        df = pl.read_parquet(self.paths["interim"] / self.interim_filename)
        df_tidy = df.lazy()

        indices = {
            "medium": "uuid",
            "providers": "medium",
            "list": ["providers", "currency"],
            "finish": "list",
            "date": "finish",
        }
        accum_index = []

        print("Unstacking data...")

        for var, index in indices.items():
            accum_index.extend(index if isinstance(index, list) else [index])
            df_tidy = df_tidy.pipe(
                self._unnest_and_unpivot, var_name=var, index=accum_index
            )

        df_tidy = (
            df_tidy.rename({"data": "price"})
            .with_columns(pl.col("date").cast(pl.Date))
            .sort(["uuid", "medium", "providers", "currency", "list", "finish", "date"])
            .collect()
        )

        print("Data unstacked!\nSaving data...")

        if self.final_filename is None:
            min_date = df_tidy["date"].min()
            max_date = df_tidy["date"].max()
            self.final_filename = (
                self.paths["interim"] / f"flat_prices_{min_date}_{max_date}.parquet"
            )
        df_tidy.write_parquet(self.final_filename)

        print("Data saved!")

    def load_data(self):
        """Load the data from the interim directory"""
        if self.final_filename:
            print("Final data loaded!")
            return pl.read_parquet(self.final_filename)
        else:
            raise ValueError("No data to load.  Run unstack_data() first.")

    def raw_json_to_parquet(self):
        """Reads the JSON File. Saves the meta and data as Parquet.

        The metadata is saved to the processed directory.  The data is saved
        to the interim directory, as it requires additional processing.

        Args:
            persist: A flag to store the data as members of the class.
            Otherwise data is just pass-through
        """

        # Read JSON
        # NOTE: The polars.read_json() and json.load() methods are MUCH,
        # MUCH slower than pandas.read_json().
        print("Reading JSON")
        df = pd.read_json(str(self.paths["raw_file"]))
        df = pd.DataFrame(df)  # Fixes pylint type confusion.

        # Get Metadata
        print("Writing data...")
        (
            df.dropna(subset=["meta"])
            .drop(columns=["data"])
            .reset_index()
            .rename(columns={"index": "field"})
            .to_parquet(self.paths["interim"] / self.meta_filename)
        )
        print("Metadata written!")

        # Get Data
        (
            df.dropna(subset=["data"])
            .drop(columns=["meta"])
            .reset_index()
            .rename(columns={"index": "uuid"})
            .to_parquet(self.paths["interim"] / self.interim_filename)
        )
        print("Interim data written!")

    def _unnest_and_unpivot(
        self, df: pl.DataFrame, index: list, var_name: str
    ) -> pl.DataFrame:
        """Takes a DataFrame with a nested column and unnests it, then unpivots the data column"""
        return (
            df.unnest("data")
            .unpivot(index=index, value_name="data", variable_name=var_name)
            .drop_nulls("data")
        )

    def _validate_paths(self):
        """Validate paths exist and add needed directories."""

        expected_keys = ["raw_file", "interim", "processed"]

        # Check if path keys are in dict
        for key in expected_keys:
            if key not in self.paths:
                raise KeyError(f"Did not find expected key {key} in paths")

        # Cast as pathlib.Path types
        for key in expected_keys:
            self.paths[key] = Path(self.paths[key])

        # Check existing and make new paths
        self.paths["raw_file"].exists()
        self.paths["interim"].mkdir(parents=True, exist_ok=True)
        self.paths["processed"].mkdir(parents=True, exist_ok=True)

        if self.final_filename is not None:
            self.final_filename = self.paths["interim"] / self.final_filename
