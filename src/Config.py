class Config():
    def __init__(self):
        self.currency = "USD"
        self.locale = "en_US"
        self.date_format = "MM/DD/YYYY"
        self.default_month = "current"
        self.expenses_file_path = ""

    # loads a config by the data
    def load_config(self, data):
        self.currency = data['currency']
        self.locale = data['locale']
        self.date_format = data['date_format']
        self.default_month = data['default_month']
        self.expenses_file_path = data['expenses_file_path']
