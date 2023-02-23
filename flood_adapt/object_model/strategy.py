from flood_adapt.object_model.io.config_io import read_config, write_config
from flood_adapt.object_model.validate.config import validate_existence_config_file, validate_content_config_file
from pathlib import Path

class Strategy:
    """ Strategy class that holds all the information for a specific strategy
    """
    def __init__(self, config_file: str = None, database_path: str = None) -> None:
        self.set_default()
        self.database_path = database_path
        if config_file:
            self.config_file = config_file
            if not self.database_path:
                self.database_path = str(Path(self.config_file).parents[3])

    def set_default(self):
        """ Sets the default values of the Strategy class attributes
        """
        self.name = ""  # Name of the measure
        self.long_name = ""  # Long name of the measure
        self.config_file = None  # path to the configuration file connected with the measure
        self.type = None  # type of strategy (can be "impact" or "hazard")
        self.measures = []  # list of measures names that are used in a strategy
        self.mandatory_keys = ["name", "long_name"]  # mandatory keys in the config file

    def set_name(self, name: str):
        self.name = name
    
    def set_long_name(self, long_name: str):
        self.long_name = long_name
    
    def set_measures(self, measures: list):
        """ Sets the actual Measure class list using the list of measure names

        Args:
            measures (list): list of measures names
        """
        self.measure_paths = [str(Path(self.database_path, "input", "measures", measure, "{}.toml".format(measure))) for measure in measures]
        # parse measures config files to get type of measure
        self.measure_types = [read_config(measure_path)["type"] for measure_path in self.measure_paths]


    def load(self):
        """ loads and updates the class attributes from a configuration file
        """
        # Validate the existence of the configuration file
        if validate_existence_config_file(self.config_file):
            config = read_config(self.config_file)

        # Validate that the mandatory keys are in the configuration file
        if validate_content_config_file(config, self.config_file, self.mandatory_keys):
            self.set_name(config["name"])
            self.set_long_name(config["long_name"])
            if "measures" in config.keys():
                self.set_measures(config["measures"])
        return self