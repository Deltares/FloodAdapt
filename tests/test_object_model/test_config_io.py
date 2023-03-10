from pathlib import Path

test_database = Path().absolute() / "tests" / "test_database"


def test_read_config():
    from flood_adapt.object_model.io.config_io import read_config

    test_toml = (
        test_database
        / "charleston"
        / "input"
        / "events"
        / "extreme12ft"
        / "extreme12ft.toml"
    )
    assert test_toml.is_file()

    config = read_config(test_toml)

    assert config
    assert isinstance(config, dict)


def test_read_write_config():
    from flood_adapt.object_model.io.config_io import read_config, write_config

    test_toml = (
        test_database
        / "charleston"
        / "input"
        / "events"
        / "extreme12ft"
        / "extreme12ft.toml"
    )
    assert test_toml.is_file()

    config = read_config(test_toml)

    assert config
    assert isinstance(config, dict)

    out_path = test_database / "test_output_toml.toml"
    write_config(config=config, file_path=out_path)

    assert out_path.is_file()

    # Remove the written toml file
    out_path.unlink()
