import configparser
import os

class ConfigReader:
    @staticmethod
    def read_config(section, key):
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
        config = configparser.ConfigParser()
        if not config.read(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        if config.has_section(section) and config.has_option(section, key):
            return config[section][key]
        elif config.has_option('DEFAULT', key):
            return config['DEFAULT'][key]
        else:
            available_sections = config.sections()
            raise KeyError(
                f"Section '{section}' or key '{key}' not found in config.ini.\n"
                f"Available sections: {available_sections}\n"
                f"Config path: {config_path}"
            )
