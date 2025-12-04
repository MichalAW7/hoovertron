import os
import csv
import configparser
from .constants import CONFIG_FILE_PATH # This will now work correctly

class SettingsMixin:
    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE_PATH):
            config.read(CONFIG_FILE_PATH)
            self.dataBaseFile = config.get('Settings', 'last_file', fallback='')
            if self.dataBaseFile:
                self.load_last_test_number()

    def save_config(self):
        config = configparser.ConfigParser()
        config['Settings'] = {'last_file': self.dataBaseFile}
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

    def load_last_test_number(self):
        if os.path.exists(self.dataBaseFile):
            with open(self.dataBaseFile, 'r', encoding='UTF8') as f:
                reader_obj = csv.reader(f)
                next(reader_obj) 
                rows = list(reader_obj)
                if rows:
                    last_row = rows[-1]
                    try:
                        self.testNumber = int(last_row[0])
                    except ValueError:
                        self.testNumber = 1
                else:
                    self.testNumber = 1
                    self.isNewDatabase = False
        else:
            self.testNumber = 1
            self.isNewDatabase = True