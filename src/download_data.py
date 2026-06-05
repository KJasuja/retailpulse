"""Download the Online Retail II dataset into data/raw/.

Usage:
    python src/download_data.py
"""
from pathlib import Path
import urllib.request

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
# UCI hosts the file as an .xlsx; mirror/alt sources also work.
URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
OUT = RAW_DIR / "online_retail_II.zip"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        print(f"Already downloaded: {OUT}")
        return
    print(f"Downloading from {URL} ...")
    try:
        urllib.request.urlretrieve(URL, OUT)
        print(f"Saved to {OUT}")
        print("Unzip it, then load the .xlsx in notebooks/01_eda.ipynb.")
    except Exception as e:  # noqa: BLE001
        print(f"Automatic download failed ({e}).")
        print("Manually download from:")
        print("  https://archive.ics.uci.edu/dataset/502/online+retail+ii")
        print(f"and place the file in {RAW_DIR}")


if __name__ == "__main__":
    main()
