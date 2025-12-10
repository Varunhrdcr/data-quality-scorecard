import pandas as pd
from pathlib import Path

# Change this if your file name changes
DATA_FILE_NAME = "load_dataset.xlsx"


def get_data_path() -> Path:
    """
    Returns the Path object pointing to the dataset.
    Looks for: ../data/load_dataset.xlsx relative to this file.
    """
    # src/ directory
    src_dir = Path(__file__).resolve().parent
    # project root = parent of src/
    project_root = src_dir.parent
    data_path = project_root / "data" / DATA_FILE_NAME

    if not data_path.exists():
        # Fallback: try same directory as this file
        alt_path = src_dir / DATA_FILE_NAME
        if alt_path.exists():
            return alt_path

        raise FileNotFoundError(
            f"Could not find {DATA_FILE_NAME} in 'data/' or 'src/' folder.\n"
            f"Looked at: {data_path} and {alt_path}"
        )

    return data_path


def load_dataset():
    """
    Loads the Excel file as a pandas DataFrame.
    """
    data_path = get_data_path()
    df = pd.read_excel(data_path)
    return df
