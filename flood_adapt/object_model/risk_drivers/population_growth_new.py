
class PopulationGrowthNew:
    def __init__(self) -> None:
        self.set_default()

        # sea_level_rise = 2
        # sea_level_rise_vertical_units = "feet"
        # subsidence = 0
        # subsidence_vertical_units = "feet"
        # rainfall_increase = 20
        # storm_frequency_increase = 20
        # economic_growth = 20
        # population_growth = 0
        # population_growth_new = 20
        # population_growth_existing = 20
        # new_development_elevation = 1
        # new_development_elevation_vertical_units = "feet"
        # new_development_elevation_reference = "floodmap"
        # new_development_shape_file = "pop_growth_new_20.shp"
    
    def set_default(self) -> None:
        self.value = 0
        self.type = "impact"
    
    def load(self, config: dict) -> None:
        self.value = config["population_growth_existing"]