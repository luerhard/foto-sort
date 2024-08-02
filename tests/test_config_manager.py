from pathlib import Path

from fotosort.config_manager import ConfigManager


def test_config_manager_out(tmp_path):
    test_path = Path(tmp_path).parent
    config_file = test_path / "test_config.yaml"
    config = ConfigManager(config_file)

    assert config.get_out_path() is None
    out = Path("test")
    config.set_out_path(out)
    assert config.get_out_path() == out.absolute()


def test_config_manager_in(tmp_path):
    test_path = Path(tmp_path).parent
    config_file = test_path / "test_config.yaml"
    config = ConfigManager(config_file)

    assert config.get_in_paths() is None
    p1 = Path("test")
    p2 = Path("test")
    config.set_in_paths([p1, p2])
    assert config.get_in_paths() == [p1.absolute(), p2.absolute()]
