# # excel_to_db/services/data_uploader.py
import pandas as pd
from django.apps import apps
from django.db import transaction


def cast_value(value, field_type="CharField"):
    if pd.isna(value):
        return None

    if field_type in ("CharField", "TextField"):
        return str(value)

    if field_type == "IntegerField":
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return None

    if field_type == "FloatField":
        try:
            return float(value)
        except Exception:
            return None

    if field_type == "BooleanField":
        s = str(value).strip().lower()
        if s in ("true", "1", "yes"):
            return True
        if s in ("false", "0", "no"):
            return False
        return None

    if field_type in ("DateField", "DateTimeField"):
        return pd.to_datetime(value, errors="coerce")

    return str(value)


def upload_data(model_name: str, df: pd.DataFrame, batch_size=5000):
    Model = apps.get_model("excel_to_db", model_name)

    # Remove unnamed columns from DataFrame
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"[^a-z0-9]+", "_", regex=True)
                  .str.strip("_")
    )
    objs = []
    total = 0

    model_fields = {f.name: f.get_internal_type() for f in Model._meta.get_fields() if f.name != "id"}

    for _, row in df.iterrows():
        kw = {}
        for col in df.columns:
            col_lower = col.strip().lower()
            for field_name in model_fields.keys():
                if col_lower == field_name.lower():
                    field_type = model_fields[field_name]
                    value = row.get(col)
                    v = cast_value(value, field_type)
                    if hasattr(v, "to_pydatetime"):
                        v = v.to_pydatetime()
                    kw[field_name] = v
                    break

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
