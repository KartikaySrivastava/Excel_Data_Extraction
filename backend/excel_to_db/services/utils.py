# excel_to_db/services/utils.py
import re

def sanitize_column(col_name: str) -> str:
    """
    Turn Excel column header into a safe python attribute:
    """
    if col_name is None:
        col_name = "field"
    s = str(col_name).strip()
    s = re.sub(r'\W+', '_', s)
    s = s.strip('_').lower()
    if not s:
        s = "field"
    if s[0].isdigit():
        s = "f_" + s
    return s
