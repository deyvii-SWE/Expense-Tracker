from datetime import datetime
from pathlib import Path

import json

class Storage():
    def __init__(self):
        self.settings_path = Path("src/data/settings")
        self.expenses_path = Path("src/data/expenses")

    # expense functions
    def create_expense_file(self, file_path, month):
        data = {
            "month": month,
            "expenses": {}
        }
        # creates a empty file
        with open(f"{file_path}\\{month}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_expense_list(self, file_path):
        data = ""

        # load the expense list if the file exists
        if Path(file_path).exists():
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        print(data['expenses'])
        return data['expenses']

    def create_expense_json(self, currency, locale, value, name, file_path, month):
        # search for a avaliable id
        def get_actual_id(data):
            expense_id = 0
            for expense in data:
                expense_id = max(expense_id, int(expense))

            return str(int(expense_id) + 1)

        # verify if the extenses file exists
        if not Path(file_path).is_file():
            self.create_expense_file(file_path, month)

        # loads the file and get the data
        with open(file_path, "r", encoding="utf-8") as file:
            old_data = json.load(file)

        # get the id
        new_id = get_actual_id(old_data['expenses']) if len(old_data['expenses']) > 0 else 0

        # creates a new expense data
        new_expense = {
            new_id: {
                "value": f"{value:.2f}",
                "name": name,
                "currency": currency,
                "locale": locale,
                "register_time": datetime.now().strftime("%H:%M")
            }
        }

        # get the new expense and add to the old_data
        old_data['expenses'] |= new_expense 

        # save
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(old_data, file, indent=4)

    def update_expense_json(self, expenses, file_path, month):
        # verify if the file exists
        if Path(f"{file_path}\\{month}.json").exists():
            # load the old data
            with open(f"{file_path}\\{month}.json", "r", encoding="utf-8") as file:
                old_data = json.load(file)

            # push the updated expense into the old_data
            old_data['expenses'] = expenses

            # save it
            with open(f"{file_path}\\{month}.json", "w", encoding="utf-8") as file:
                json.dump(old_data, file, indent=4, ensure_ascii=False)

    # settings functions
    def create_settings_json(self):

        # get the actuals values
        actual_month = datetime.now().strftime("%b").lower()
        actual_year = datetime.now().year

        # creates the settings path
        self.settings_path.mkdir(parents=True, exist_ok=True)

        # default settings data
        data = {
            "currency": "USD",
            "locale": "en_US",
            "date_format": "MM/DD/YYYY",
            "default_month": actual_month,
            "expenses_file_path": f"src/data/expenses/{actual_year}"
        }

        # creates the settings
        with open(self.settings_path / 'config.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def get_config_data(self):
        # get the config data
        if self.verify_config_json():
            with open(self.settings_path / 'config.json', "r", encoding="utf-8") as file:
                return json.load(file)

    def update_config_data(self, new_data):
        # verifying the existence of the folders and files
        if not self.verify_config_json():
            if not self.verify_folders():
                # creates folders
                self.create_folders()
            # create files
            self.create_settings_json()

        # save the new data into the settings
        with open(self.settings_path / 'config.json', "w", encoding="utf-8") as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)

    # update to the actual month
    def update_actual_month(self):
        # verify if the config json exists
        if self.verify_config_json():
            # load the config.json
            with open(self.settings_path / 'config.json', "r", encoding="utf-8") as file:
                data = json.load(file)

            # change the month for the actual month (reduced)
            data['default_month'] = datetime.now().strftime("%b")

            # update the file
            with open(self.settings_path / 'config.json', "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

    # verify the config json exist
    def verify_config_json(self):
        return Path(self.settings_path / "config.json").is_file()

    # folders
    def verify_folders(self):
        if not self.expenses_path.is_file() or not self.settings_path.is_file():
            return False
        return True

    def create_folders(self, month):
        # verify if the folders exists
        if not self.verify_folders():
            # create the folders
            self.settings_path.mkdir(parents=True, exist_ok=True)
            self.expenses_path.mkdir(parents=True, exist_ok=True)

        # if the actual expense year folder dont exist, creates a new one
        if not Path(f"{self.expenses_path}\\{datetime.now().year}").exists():
            Path(f"{self.expenses_path}\\{datetime.now().year}").mkdir(parents=True, exist_ok=True)

            self.create_expense_file(self.expenses_path, month)

