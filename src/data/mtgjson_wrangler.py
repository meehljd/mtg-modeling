""" Wrangle the MTG JSON AllPrices.JSON Data """

import os
from pathlib import Path
import pandas as pd
import polars as pl


class MtgPricesJsonWrangler:
    def __init__(self, paths: dict):
        self.paths = paths
        self.meta = None
        self.data = None

        self.meta_filename = "meta.parquet"
        self.data_filename = "allCardPrices.parquet"

        self._validate_paths()

    def process_price_data(self):
        """  """

        tot_len = 0
        chunk_size = 10000
        for i, start in enumerate(range(0, df.shape[0], chunk_size)):
            print(f"Processing {i*10000}/{df.shape[0]}")
            end = min(start + chunk_size, df.shape[0])
            df_chunk = df.loc[df.index[start:end]]
            df_chunk = _extract_nested_data(df_chunk)
            df_chunk.to_parquet(interim_root / f"AllPrices_chunk_{i}.parquet")
            tot_len += df_chunk.shape[0]
        tot_len

    def raw_json_to_parquet(self, persist: bool = True):
        """Reads the JSON File. Saves the meta and data as Parquet.

        The metadata is saved to the processed directory.  The data is saved
        to the interim directory, as it requires additional processing.

        Args:
            presist: A flag to store the data as members of the class.
            Otherwise data is just pass-through
        """

        # Read JSON
        # NOTE: The polars.read_json() and json.load() methods are MUCH,
        # MUCH slower than pandas.read_json().
        print("Reading JSON")
        df = pd.read_json(str(self.paths["raw_filepath"]))
        df = pd.DataFrame(df)  # Fixes pylint type confusion.

        # Get Metadata
        print("Writing metadata to processed directory")
        meta = df.dropna(subset=["meta"])
        meta = meta.reset_index()
        meta = meta.rename(columns={"index": "field"})
        meta.to_parquet(self.paths["processed_path"] / self.meta_filename)
        print("Metadata written!")

        # Get Data
        print("Writing data to interim directory")
        data = df.dropna(subset=["data"])
        data = data.drop(columns=["meta"])
        data = data.reset_index()
        data = data.rename(columns={"index": "uuid"})
        data.to_parquet(self.paths["interim_path"] / self.data_filename)
        print("Data written!")

        # Persist
        if persist:
            print("Data persisted")
            self.data = data
            self.meta = meta
        else:
            print("Data NOT persisted")

    def _validate_paths(self):
        """Validate paths exist and add needed directories."""

        expected_keys = ["raw_filepath", "interim_path", "processed_path"]

        # Check if path keys are in dict
        for key in expected_keys:
            if key not in self.paths:
                raise KeyError(f"Did not find expected key {key} in paths")

        # Cast as pathlib.Path types
        for key in expected_keys:
            self.paths[key] = Path(self.paths[key])

        # Check existing and make new paths
        self.paths["raw_filepath"].exists()
        self.paths["interim_path"].mkdir(parents=True, exist_ok=True)
        self.paths["processed_path"].mkdir(parents=True, exist_ok=True)
