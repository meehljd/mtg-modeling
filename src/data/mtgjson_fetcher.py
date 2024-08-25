"""Fetches MTG JSON data from API"""

import os
import platform
from pathlib import Path
from datetime import datetime


class MtgJsonFetcher:
    
    def __init__(self, dataset: str, save_root: str = "data/raw/mtgjson"):
        self.dataset = dataset
        self.save_root = Path(save_root)
        self.final_path = self.save_root / Path(self.dataset).stem
        self._validate_inputs()

        self.os_name = platform.system()
        self.filename = self._get_filename()
        self.filepath = self.save_root / self.filename
        self.api_url = f"https://mtgjson.com/api/v5/{self.filename}"

    def fetch(self):
        """Fetches the data from the URL and decompresses."""

        print(f"Downloading {self.dataset} Data")
        print(f"Starting datetime: {datetime.now()}")

        if self.os_name == "Linux":
            size = self._linux_data_fetch()
        elif self.os_name == "Windows":
            size = self._windows_data_fetch()
        else:
            raise ValueError(f"OS {self.os_name} not supported.")

        print(f"Downloaded {self.dataset} Data")
        print(f"Final size: {size}")
        print(f"Final path: {self.final_path}")

        print(f"Finished datetime: {datetime.now()}")

    def _validate_inputs(self):
        """Validates the inputs for the fetcher"""

        # Validate dataset
        valid_datasets = ["AllPrices.json", "AllPrintingsParquetFiles"]
        if self.dataset not in valid_datasets:
            raise ValueError(f"Dataset must be one of {valid_datasets}.")

        # Make directory if it doesn't exist
        os.makedirs(self.save_root, exist_ok=True)
        os.makedirs(self.final_path, exist_ok=True)

    def _get_filename(self):
        """Gets the filename for the dataset"""

        if self.os_name == "Linux":
            if self.dataset == "AllPrintingsParquetFiles":
                file_ext = "tar.gz"
            else:
                file_ext = "gz"
        elif self.os_name == "Windows":
            file_ext = "zip"
        else:
            raise ValueError(f"OS {self.os_name} not supported.")

        return f"{self.dataset}.{file_ext}"

    def _linux_data_fetch(self):
        """Linux commands"""
        os.system(f"wget -P {self.save_root} --progress=dot:giga {self.api_url}")
        if "tar" in self.filepath.name:
            os.system(f"tar -xzf {self.filepath} -C {self.save_root}")
        else:
            os.system(f"gunzip -c  {self.filepath} > {self.final_path / self.dataset}")
        os.system(f"rm {self.filepath}")
        size = os.system(f"du -sh {self.save_root}")
        return size

    def _windows_data_fetch(self):
        """Windows commands (using PowerShell)"""
        os.system(
            f"powershell Invoke-WebRequest -Uri {self.api_url} -OutFile {self.filepath}"
        )
        os.system(
            f"powershell Expand-Archive -Path {self.filepath} -DestinationPath {self.final_path}"
        )
        os.system(f"powershell Remove-Item {self.filepath}")
        size = os.system(
            f"powershell Get-ChildItem {self.save_root} | "
            f"Measure-Object -Property Length -Sum | "
            f"ForEach-Object {{ $_.Sum / 1MB }}"
        )
        return size
