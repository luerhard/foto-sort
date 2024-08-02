from configparser import ConfigParser
from pathlib import Path

from appdirs import user_config_dir

class ConfigManager:
    def __init__(self, config_file=None) -> None:
        if config_file is None:
            config_dir = Path(user_config_dir("fotosort", "luerhard"))
            self.config_file = config_dir / "config.ini"
        else:
            self.config_file = Path(config_file)

        self.load()

    def load(self):
        self.config = ConfigParser()
        if self.config_file.exists():
            self.config.read(self.config_file)

        changed = False
        if "OUT" not in self.config:
            self.config["OUT"] = {"path": ""}
            changed = True
        if "IN" not in self.config:
            self.config["IN"] = {}
            changed = True
        if changed:
            self.save()

    def save(self):
        with self.config_file.open("w") as f:
            self.config.write(f)

    def get_out_path(self):
        path = self.config["OUT"]["path"]
        if path:
            return Path(path)
        return None

    def get_in_paths(self):
        paths = []
        for key in self.config["IN"].keys():
            path = self.config["IN"][key]
            if path:
                paths.append(Path(path))
        if not paths:
            return None
        else:
            return paths

    def set_in_paths(self, paths):
        self.config["IN"] = {}
        for i, path in enumerate(paths, 1):
            path = Path(path)
            self.config["IN"][f"path_{i}"] = str(path.absolute())
        self.save()

    def set_out_path(self, path):
        self.config["OUT"]["path"] = str(path.absolute())
        self.save()


if __name__ == "__main__":
    test_path = Path(__file__).parent
    config_file = test_path / "test_config.yaml"
    test_path.mkdir(parents=True, exist_ok=True)

    config = ConfigManager(config_file)

    print(config.get_out_path())

    out = Path("test")
    out2 = Path("test2")
    config.set_out_path(out)
    config.set_in_paths([out, out2])
    print(config.get_out_path())

    ass

    print(config.get_in_paths())

    print("dones")
