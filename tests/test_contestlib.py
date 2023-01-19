
from contestlib import ContestLib

cl = ContestLib("config/contestinfo.json.sample")

def test_get_bands():
    assert ["160m", "80m"] == cl.get_bands()

def test_get_callsigns():
    assert ["DL1FOO", "DB2BAR"] == cl.get_callsigns()

def test_is_callsign():
    assert cl.is_callsign("DL3FOO") is True
    assert cl.is_callsign("dl") is False
    assert cl.is_callsign("test2!s") is False
