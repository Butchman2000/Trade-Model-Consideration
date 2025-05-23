# Program: config_loader_module.py
# Author: Brian Anderson
# Origin Date: May2025
# Version: 1.1
# Purpose:
#
#    /Provide a clean, minimal interface for accessing config.ini

import configparser  # Built-in Python module for reading .ini configuration files
import os

class ConfigLoader:
    # This is responsible for reading values from a .ini-style configuration file.
    # It exposes typed accessor methods for common data types (float, string, list).
    
    def __init__(self, config_path="config.ini"):
        # This initializes the loader, which by default, looks for a file named 'config.ini'
        # in the working dir. Can specify different path by passing it as a config_path.
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_float(self, section, key):
        # Collect single float value from a given section and key in the config file.
        # Example usage: get_float("GLOBAL_CONSTRAINTS", "max_bin_weight")
        
        return float(self.config[section][key])

    def get_str(self, section, key):
        # Fetch a string value from the config.
        # Useful for things like file paths, labels, or algorithm names.
      
        return self.config[section][key]

    def get_list(self, section, key):
        # Grab a comma-separated list from the config and return it as a Python list.
        # Example in config:   features = spy_rsi, vix, atm_iv, pe_ratio
        # Will be returned as: ['spy_rsi', 'vix', 'atm_iv', 'pe_ratio']
        
        return [item.strip() for item in self.config[section][key].split(",")]

    def get_constraints(self):
        # Bundle all global numeric constraints into a dictionary for easy use.
        # Typically used in strategy modules that allocate capital or enforce limits.
        
        return {
            "max_bin_weight": self.get_float("GLOBAL_CONSTRAINTS", "max_bin_weight"),
            "min_bin_weight": self.get_float("GLOBAL_CONSTRAINTS", "min_bin_weight"),
            "total_portfolio_allocation": self.get_float("GLOBAL_CONSTRAINTS", "total_portfolio_allocation"),
            "liquidity_reserve": self.get_float("GLOBAL_CONSTRAINTS", "liquidity_reserve")
        }

    def get_model_params(self):
        # This returns hyperparameters for a machine learning model defined in config.
        # These values can be passed directly into model constructors like RandomForestClassifier.
        
        return {
            "type": self.get_str("MODEL", "type"),  # For logging or conditional logic
            "n_estimators": int(self.config["MODEL"]["n_estimators"]),
            "random_state": int(self.config["MODEL"]["random_state"])
        }

    def get_data_spec(self):
        '''
        Retrieves dataset configuration:
        - source: filename of the dataset
        - features: list of feature column names
        - target: name of the target variable
        Used to load and prepare training/test data in ML modules.
        '''
       
        return {
            "source": self.get_str("DATA", "source"),
            "features": self.get_list("DATA", "features"),
            "target": self.get_str("DATA", "target")
        }
