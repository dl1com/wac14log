
import jsonhandler
from pathlib import Path

def test_read_contest_info_from_file():
    filename = Path("config/contestinfo.json.sample")
    data = jsonhandler.read_contest_info(filename)
    assert data["contestname"] == "Sample Contest"