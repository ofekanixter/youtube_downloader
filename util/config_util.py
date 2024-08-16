import json
import os
config_file = 'C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader/util/configurations.json'
class ConfigUtil:
    def load_config(self):
        """
        Loads the configuration file.

        Parameters:
        config_file (str): Path to the configuration file.

        Returns:
        dict: The configuration data, or an empty dictionary if the file doesn't exist.
        """
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_config(self,config_data):
        """
        Saves the configuration data to a file.

        Parameters:
        config_file (str): Path to the configuration file.
        config_data (dict): The configuration data to save.
        """
        with open(config_file, 'w') as file:
            json.dump(config_data, file, indent=4)

    def add_config(self,config_file, key, value):
        """
        Adds or updates a configuration key-value pair in the JSON configuration file.

        Parameters:
        config_file (str): Path to the configuration file.
        key (str): The key to add or update.
        value: The value to set for the key.
        """
        # Load existing configuration
        try:
            with open(config_file, 'r') as file:
                config_data = json.load(file)
        except FileNotFoundError:
            config_data = {}
        except json.JSONDecodeError:
            config_data = {}

        # Update the configuration
        config_data[key] = value

        # Save the updated configuration
        with open(config_file, 'w') as file:
            json.dump(config_data, file, indent=4)

        print(f"Configuration '{key}' added/updated successfully.")

        import json

    def remove_config(self,config_file, key):
        """
        Removes a configuration key-value pair from the JSON configuration file.

        Parameters:
        config_file (str): Path to the configuration file.
        key (str): The key to remove.
        """
        # Load existing configuration
        try:
            with open(config_file, 'r') as file:
                config_data = json.load(file)
        except FileNotFoundError:
            print("Configuration file not found.")
            return
        except json.JSONDecodeError:
            print("Error reading configuration file.")
            return

        # Remove the configuration if it exists
        if key in config_data:
            del config_data[key]
            
            # Save the updated configuration
            with open(config_file, 'w') as file:
                json.dump(config_data, file, indent=4)
            
            print(f"Configuration '{key}' removed successfully.")
        else:
            print(f"Configuration '{key}' not found.")
