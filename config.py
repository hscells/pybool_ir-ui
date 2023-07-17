import toml
import serp
import importlib

class AppConfig:
    def __init__(self, config_path="config.toml"):
        with open(config_path, "r") as f:
            config = toml.load(f)

        if "app" in config:
            self.default_query = config["app"]["default_query"]
            self.page_title = config["app"]["page_title"]
            self.render_serp_item = getattr(serp, config["app"]["serp_renderer"])
        else:
            raise ValueError("missing app config")

        if "parser" in config:
            parts = config["parser"]["class"].split(".")
            module = importlib.import_module(".".join(parts[:-1]))
            cls = getattr(module, parts[-1])
            parse_args = config["parser"]["parser_args"]
            self.parser = cls(**parse_args)
        else:
            raise ValueError("missing parser config")

        if "indexer" in config:
            parts = config["indexer"]["class"].split(".")
            module = importlib.import_module(".".join(parts[:-1]))
            cls = getattr(module, parts[-1])
            indexer_path = config["indexer"]["path"]
            indexer_args = config["indexer"]["indexer_args"]
            self.indexer = cls(indexer_path, **indexer_args)
        else:
            raise ValueError("missing indexer config")
