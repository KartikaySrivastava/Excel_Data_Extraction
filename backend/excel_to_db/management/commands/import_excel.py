# excel_to_db/management/commands/import_excel.py
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command

from excel_to_db.services.excel_reader import read_excel
from excel_to_db.services.model_generator import generate_model_file
from excel_to_db.services.data_uploader import upload_data


class Command(BaseCommand):
    help = "Import an Excel file to the DB creating model + migrations automatically"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, required=True, help="Path to Excel file (xlsx)")
        parser.add_argument("--model", type=str, default="ExcelData", help="Name of the Django model to create")
        parser.add_argument("--app-dir", type=str, default=None, help="Path to app directory (optional)")

    def handle(self, *args, **options):
        filepath = options["file"]
        model_name = options["model"]
        app_dir_override = options["app_dir"]

        if not os.path.exists(filepath):
            self.stderr.write(self.style.ERROR(f"File not found: {filepath}"))
            return

        df, fields = read_excel(filepath)
        self.stdout.write(self.style.SUCCESS(f"Detected columns: {[f['original_name'] for f in fields]}"))

        if app_dir_override:
            app_dir = Path(app_dir_override)
        else:
            this_file = Path(__file__).resolve()
            app_dir = this_file.parent.parent.parent

        generated_path = generate_model_file(model_name, fields, app_dir)
        self.stdout.write(self.style.SUCCESS(f"Generated model at: {generated_path}"))

        self.stdout.write(self.style.NOTICE("Running makemigrations..."))
        call_command("makemigrations", "excel_to_db")
        self.stdout.write(self.style.NOTICE("Running migrate..."))
        call_command("migrate")

        count = upload_data(model_name, df, fields)
        self.stdout.write(self.style.SUCCESS(f"Uploaded {count} rows into {model_name}"))
