from flood_adapt.object_model.io.config_io import read_config
from flood_adapt.object_model.validate.config import validate_existence_config_file, validate_content_config_file

from flood_adapt.object_model.risk_drivers.risk_driver_factory import RiskDriverFactory


class Projection:
    """The Projection class containing various risk drivers."""
    def __init__(self, config_file: str = None) -> None:
        self.set_default()
        if config_file:
            self.config_file = config_file

    def set_default(self) -> None:
        self.name = ""
        self.long_name = ""
        self.config_file = None
        self.mandatory_keys = ["name", "long_name"]

        # Set the default values for all risk drivers
        self.slr = RiskDriverFactory.get_risk_drivers('slr')
        self.population_growth_existing = RiskDriverFactory.get_risk_drivers('population_growth_existing')
        self.population_growth_new = RiskDriverFactory.get_risk_drivers('population_growth_new')
        self.economic_growth = RiskDriverFactory.get_risk_drivers('economic_growth')
        self.precipitation_intensity = RiskDriverFactory.get_risk_drivers('precipitation_intensity')
        self.storminess = RiskDriverFactory.get_risk_drivers('storminess')

    def set_name(self, value: str) -> None:
        self.name = value
    
    def set_long_name(self, value: str) -> None:
        self.long_name = value
    
    def set_risk_drivers(self, config: dict) -> None:
        # Load all risk drivers
        if "sea_level_rise" in config.keys():
            self.slr.load(config, self.config_file)

        if "population_growth_existing" in config.keys():
            self.population_growth_existing.load(config, self.config_file)
        
        if "population_growth_new" in config.keys():
            self.population_growth_new.load(config, self.config_file)

        if "economic_growth" in config.keys():
            self.economic_growth.load(config, self.config_file)

        if "rainfall_increase" in config.keys():
            self.precipitation_intensity.load(config, self.config_file)

        if "storm_frequency_increase" in config.keys():
            self.storminess.load(config, self.config_file)

    def load(self) -> None:
        # Validate the existence of the configuration file
        if validate_existence_config_file(self.config_file):
            config = read_config(self.config_file)

        # Validate that the mandatory keys are in the configuration file
        if validate_content_config_file(config, self.config_file, self.mandatory_keys):
            self.set_name(config["name"])
            self.set_long_name(config["long_name"])
            self.set_risk_drivers(config)
    
    # def write(self):
    #     write_config(self.config_file)
    
