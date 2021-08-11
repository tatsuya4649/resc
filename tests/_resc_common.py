
import pytest
from resc import Resc

_INTERVAL=0
@pytest.fixture(scope="function",autouse=False)
def setup_resc():
    resc = Resc(
        cpu={"threshold": 80, "interval":_INTERVAL},
        memory={"threshold": 80},
        disk={"threshold": 80, "path":"/"},
        net={"threshold": 1000, "kind": "all"},
        ps={"threshold": 90.0, "mode": "percent", "limits": "soft"},
        file={"threshold": 80.0, "mode": "percent"},
    )
    yield resc
