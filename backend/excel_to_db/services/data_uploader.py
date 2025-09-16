# excel_to_db/services/data_uploader.py
import pandas as pd
from django.apps import apps
from django.db import transaction

def cast_value(value, dtype):
    if pd.isna(value):
        return None
    if dtype == "integer":
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return None
    if dtype == "float":
        try:
            return float(value)
        except Exception:
            return None
    if dtype == "boolean":
        s = str(value).strip().lower()
        if s in ("true", "1", "yes"):
            return True
        if s in ("false", "0", "no"):
            return False
        return None
    if dtype in ("date", "datetime"):
        return pd.to_datetime(value, errors="coerce")
    return str(value)


def upload_data(model_name: str, df: pd.DataFrame, fields: list, batch_size=500):
    Model = apps.get_model("excel_to_db", model_name)
    objs = []
    total = 0
    field_map = {f["original_name"]: f for f in fields}
    for _, row in df.iterrows():
        kw = {}
        for orig_col, info in field_map.items():
            python_field = info["name"]
            dtype = info["dtype"]
            value = row.get(orig_col)
            v = cast_value(value, dtype)
            if hasattr(v, "to_pydatetime"):
                v = v.to_pydatetime()
            kw[python_field] = v
        objs.append(Model(**kw))
        if len(objs) >= batch_size:
            with transaction.atomic():
                Model.objects.bulk_create(objs)
            total += len(objs)
            objs = []
    if objs:
        with transaction.atomic():
            Model.objects.bulk_create(objs)
        total += len(objs)
    return total
