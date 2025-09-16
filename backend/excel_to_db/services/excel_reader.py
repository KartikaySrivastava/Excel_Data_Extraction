# excel_to_db/services/excel_reader.py
import pandas as pd
from .utils import sanitize_column

def infer_dtype(series: pd.Series) -> str:
    s = series.dropna()
    if s.empty:
        return "char"

    numeric = pd.to_numeric(s, errors="coerce")
    numeric_non_na = numeric.dropna()
    if not numeric_non_na.empty:
        if (numeric_non_na % 1 == 0).all():
            return "integer"
        return "float"

    lowered = s.astype(str).str.lower()
    if lowered.isin(["true", "false", "yes", "no", "0", "1"]).all():
        return "boolean"

    parsed = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    if parsed.notna().sum() / max(1, len(s)) > 0.7:
        times = parsed.dt.time
        zero_time = pd.Timestamp(0).time()
        if any(t != zero_time for t in times.dropna()):
            return "datetime"
        return "date"

    max_len = s.astype(str).str.len().max()
    if max_len is not None and max_len > 255:
        return "text"
    return "char"


def read_excel(filepath: str, sheet_name=0):
    """
    Returns (df, fields)
    fields: list of dict: { original_name, name (sanitized), dtype }
    """
    df = pd.read_excel(filepath, sheet_name=sheet_name, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    fields = []
    for col in df.columns:
        series = df[col]
        dtype = infer_dtype(series)
        fields.append({
            "original_name": col,
            "name": sanitize_column(col),
            "dtype": dtype
        })
    return df, fields
