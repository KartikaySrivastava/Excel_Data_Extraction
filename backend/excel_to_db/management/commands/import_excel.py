# # excel_to_db/management/commands/import_excel.py
import os
from pathlib import Path
from django.core.management.base import BaseCommand

from excel_to_db.services.excel_reader import read_excel
from excel_to_db.services.data_uploader import upload_data


class Command(BaseCommand):
    help = "Import an Excel file into the fixed ExcelData model"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, required=True, help="Path to Excel file (xlsx)")

    def handle(self, *args, **options):
        filepath = options["file"]

        if not os.path.exists(filepath):
            self.stderr.write(self.style.ERROR(f"File not found: {filepath}"))
            return

        df, fields = read_excel(filepath)
        self.stdout.write(self.style.SUCCESS(f"Detected columns: {[f['original_name'] for f in fields]}"))

        count = upload_data("ExcelData", df)
        self.stdout.write(self.style.SUCCESS(f"Uploaded {count} rows into ExcelData"))
