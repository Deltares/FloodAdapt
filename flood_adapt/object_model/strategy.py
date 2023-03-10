from pathlib import Path
from typing import Optional

import tomli
import tomli_w
from pydantic import BaseModel

from flood_adapt.object_model.direct_impact.impact_strategy import ImpactStrategy
from flood_adapt.object_model.direct_impact.measure.impact_measure import ImpactType
from flood_adapt.object_model.hazard.hazard_strategy import HazardStrategy
from flood_adapt.object_model.hazard.measure.hazard_measure import HazardType
from flood_adapt.object_model.interface.strategies import IStrategy
from flood_adapt.object_model.io.database_io import DatabaseIO
from flood_adapt.object_model.measure import Measure
from flood_adapt.object_model.measure_factory import (
    HazardMeasureFactory,
    ImpactMeasureFactory,
)


class StrategyModel(BaseModel):
    name: str
    long_name: str
    measures: Optional[list[str]] = []


class Strategy(IStrategy):
    """Strategy class that holds all the information for a specific strategy"""

    attrs: StrategyModel

    def get_measures(self) -> None:
        """Gets the measures paths and types"""
        # Get measure paths using a database structure
        measure_paths = [
            str(Path(DatabaseIO().measures_path, measure, "{}.toml".format(measure)))
            for measure in self.attrs.measures
        ]
        # parse measures config files to get type of measure
        measure_types = [
            Measure.load_measure_type(measure_path) for measure_path in measure_paths
        ]
        # Get type of measure
        impact_measures, hazard_measures = [], []

        for i, type in enumerate(measure_types):
            if type in iter(ImpactType):
                config = measure_paths[i]
                impact_measures.append(
                    ImpactMeasureFactory.get_impact_measure(type).load_file(config)
                )
            elif type in iter(HazardType):
                config = measure_paths[i]
                hazard_measures.append(
                    HazardMeasureFactory.get_hazard_measure(type).load_file(config)
                )

        self.ImpactStrategy = ImpactStrategy(impact_measures)
        self.HazardStrategy = HazardStrategy(hazard_measures)

    @staticmethod
    def load_file(filepath: Path):
        """create Strategy from toml file"""

        obj = Strategy()
        with open(filepath, mode="rb") as fp:
            toml = tomli.load(fp)
        obj.attrs = StrategyModel.parse_obj(toml)
        obj.get_measures()
        return obj

    @staticmethod
    def load_dict(data: dict):
        """create Strategy from object, e.g. when initialized from GUI"""

        obj = Strategy()
        obj.attrs = StrategyModel.parse_obj(data)
        obj.get_measures()
        return obj

    def save(self, filepath: Path):
        """save Elavate to a toml file"""
        with open(filepath, "wb") as f:
            tomli_w.dump(self.attrs.dict(exclude_none=True), f)
