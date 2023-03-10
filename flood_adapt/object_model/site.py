from enum import Enum
from pathlib import Path
from typing import Optional, Union

import tomli
import tomli_w
from pydantic import BaseModel

from flood_adapt.object_model.io.unitfulvalue import (
    UnitfulDischarge,
    UnitfulLength,
    UnitTypesLength,
)


class Cstype(str, Enum):
    """class describing the accepted input for the variable cstype in SiteConfig"""

    projected = "projected"
    spherical = "spherical"


class Floodmap_type(str, Enum):
    """class describing the accepted input for the variable floodmap in SiteConfig"""

    water_level = "water_level"
    water_depth = "water_depth"


class SfincsModel(BaseModel):
    """class describing the accepted input for the variable sfincs in SiteConfig"""

    csname: str
    cstype: Cstype
    version: str
    offshore_model: str
    overland_model: str
    datum_offshore_model: str
    datum_overland_model: str
    diff_datum_offshore_overland: UnitfulLength
    tidal_components: str
    ambient_air_pressure: float
    floodmap_no_data_value: float
    floodmap_units: UnitTypesLength


class SlrModel(BaseModel):
    """class describing the accepted input for the variable slr in SiteConfig"""

    vertical_offset: UnitfulLength
    relative_to_year: int


class GuiModel(BaseModel):
    """class describing the accepted input for the variable gui in SiteConfig"""

    tide_harmonic_amplitude: UnitfulLength


class RiskModel(BaseModel):
    """class describing the accepted input for the variable risk in SiteConfig"""

    flooding_threshold: UnitfulLength
    return_periods: list


class DemModel(BaseModel):
    """class describing the accepted input for the variable dem in SiteConfig"""

    filename: str
    units: UnitTypesLength
    indexfilename: str


class FiatModel(BaseModel):
    """class describing the accepted input for the variable fiat in SiteConfig"""

    exposure_crs: str
    aggregation_shapefiles: str
    aggregation_field_names: str
    floodmap_type: Floodmap_type


class RiverModel(BaseModel):
    """class describing the accepted input for the variable river in SiteConfig"""

    # TODO: add functionality to use multiple rivers

    name: str
    long_name: str
    mean_discharge: UnitfulDischarge
    x_coordinate: float
    y_coordinate: float


class Obs_stationModel(BaseModel):
    """class describing the accepted input for the variable obs_station in SiteConfig"""

    name: Union[int, str]
    long_name: str
    ID: int
    lat: float
    lon: float
    mllw: UnitfulLength
    mhhw: UnitfulLength
    localdatum: UnitfulLength
    msl: UnitfulLength


class SiteConfigModel(BaseModel):
    """BaseModel describing the expected variables and data types of attributes of the siteConfig class"""

    name: str
    long_name: str
    lat: float
    lon: float
    sfincs: SfincsModel
    slr: SlrModel
    gui: GuiModel
    risk: RiskModel
    dem: DemModel
    fiat: FiatModel
    river: Optional[RiverModel]
    obs_station: Optional[Obs_stationModel]


class SiteConfig:
    """Class for general variables of the object_model"""

    attrs: SiteConfigModel

    @staticmethod
    def load_file(filepath: Path):
        """create SiteConfig from toml file"""

        obj = SiteConfig()
        with open(filepath, mode="rb") as fp:
            toml = tomli.load(fp)
        obj.attrs = SiteConfigModel.parse_obj(toml)
        return obj

    @staticmethod
    def load_dict(data: dict):
        """create Synthetic from object, e.g. when initialized from GUI"""

        obj = SiteConfig()
        obj.attrs = SiteConfig.parse_obj(data)
        return obj

    def save(self, file: Path):
        """write toml file from model object"""
        with open(file, "wb") as f:
            tomli_w.dump(self.attrs.dict(), f)
