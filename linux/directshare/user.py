import json
import os
from pathlib import Path

from gi.repository import GLib

config_dir = Path(GLib.get_user_config_dir()) / "direct-share"
config_dir.mkdir(parents=True, exist_ok=True)
config_file = config_dir / "config.json"
if config_file.exists():
    config = json.loads(config_file.read_text())
    os.environ["LANGUAGE"] = config.get("LANGUAGE", "en")
