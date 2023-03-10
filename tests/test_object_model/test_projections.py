from pathlib import Path

import pytest

from flood_adapt.object_model.direct_impact.socio_economic_change import (
    SocioEconomicChange,
)
from flood_adapt.object_model.hazard.physical_projection import (
    PhysicalProjection,
)
from flood_adapt.object_model.projection import Projection

test_database = Path().absolute() / "tests" / "test_database"


def test_projection_read():
    test_toml = (
        test_database
        / "charleston"
        / "input"
        / "projections"
        / "all_projections"
        / "all_projections.toml"
    )
    assert test_toml.is_file()

    projection = Projection.load_file(test_toml)

    # Assert that the configured risk drivers are set to the values from the toml file
    assert isinstance(projection.PhysicalProjection, PhysicalProjection)
    assert isinstance(projection.SocioEconomicChange, SocioEconomicChange)
    assert projection.attrs.name == "all_projections"
    assert projection.attrs.long_name == "all_projections"
    assert projection.PhysicalProjection.attrs.sea_level_rise.value == 2
    assert projection.SocioEconomicChange.attrs.economic_growth == 20
    with pytest.raises(AttributeError):
        projection.SocioEconomicChange.attrs.sea_level_rise.value
    with pytest.raises(AttributeError):
        projection.PhysicalProjection.attrs.economic_growth


def test_projection_only_slr():
    test_toml = (
        test_database
        / "charleston"
        / "input"
        / "projections"
        / "SLR_2ft"
        / "SLR_2ft.toml"
    )

    assert test_toml.is_file()

    projection = Projection.load_file(test_toml)

    # Assert that all unconfigured risk drivers are set to the default values
    assert projection.PhysicalProjection.attrs.storm_frequency_increase == 0

    # Assert that the configured risk drivers are set to the values from the toml file
    assert projection.attrs.name == "SLR_2ft"
    assert projection.attrs.long_name == "SLR_2ft"
    assert projection.PhysicalProjection.attrs.sea_level_rise.value == 2
    assert projection.PhysicalProjection.attrs.sea_level_rise.units == "feet"
