from flood_adapt.object_model.validate.config import validate_content_config_file
from typing import Union


class EconomicGrowth:
    def __init__(self) -> None:
        self.set_default()

    def set_default(self) -> None:
        self.effect_on = "impact"
        self.economic_growth = 0
    
    def set_economic_growth(self, value: Union[int, float]) -> None:
        self.economic_growth = value
    
    def load(self, config: dict, config_path: str) -> None:
        validate_content_config_file(config, config_path, ["economic_growth"])
        self.set_economic_growth(config["economic_growth"])