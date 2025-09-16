# excel_to_db/services/model_generator.py
from pathlib import Path
from typing import List, Dict

FIELD_TEMPLATE = "    {name} = {field_def}\n"

def django_field_from_dtype(dtype: str, max_len: int = 255) -> str:
    if dtype == "integer":
        return "models.IntegerField(null=True, blank=True)"
    if dtype == "float":
        return "models.FloatField(null=True, blank=True)"
    if dtype == "boolean":
        return "models.BooleanField(null=True, blank=True)"
    if dtype == "date":
        return "models.DateField(null=True, blank=True)"
    if dtype == "datetime":
        return "models.DateTimeField(null=True, blank=True)"
    if dtype == "text":
        return "models.TextField(null=True, blank=True)"
    return f"models.CharField(max_length={max_len}, null=True, blank=True)"


def generate_model_file(model_name: str, fields: List[Dict], app_dir: Path):
    models_generated_path = app_dir / "models_generated.py"
    import_lines = "from django.db import models\n\n"
    class_lines = f"class {model_name}(models.Model):\n"
    class_lines += "    # auto-generated model from Excel\n"
    for f in fields:
        field_name = f["name"]
        field_def = django_field_from_dtype(f["dtype"])
        class_lines += FIELD_TEMPLATE.format(name=field_name, field_def=field_def)
    class_lines += "\n    def __str__(self):\n"
    class_lines += "        return f\"{self.pk}\"\n\n"
    with open(models_generated_path, "w", encoding="utf-8") as fh:
        fh.write(import_lines + class_lines)
    return models_generated_path
