from flood_adapt.object_model.validate.config import validate_content_config_file


class Storminess:
    def __init__(self) -> None:
        self.set_default()

    def set_default(self) -> None:
        self.effect_on = "hazard"
        self.value = 0
    
    def load(self, config: dict, config_path: str) -> None:
        validate_content_config_file(config, config_path, ["storm_frequency_increase"])
        self.value = config["storm_frequency_increase"]
