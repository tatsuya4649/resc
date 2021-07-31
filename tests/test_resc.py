import os
import sys

from resc import Resc
_INTERVAL=0

def test_resc():
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    res = resc.thresholds
    assert res is not None
    assert isinstance(res,dict)
    print(f'RESC THRESHOLDS {res}')

    res = resc.checks
    assert res is not None
    assert isinstance(res,dict)
    print(f'RESC CHECKS {res}')

    res = resc.over_one
    assert res is not None
    assert isinstance(res,bool)
    print(f'RESC OVER ONE {res}')

    res = resc.overs
    assert res is not None
    assert isinstance(res,list)
    print(f'RESC OVERS {res}')


def test_register():
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="*/1 * * * *",
        rescdir="rescs"
    )
    def hello():
        print("hello resc!!!")
    hello()

    os.environ["RESCPATH"] = "rescs"
    os.environ["RESCOUTPUT"] = "rescoutput.txt"
    @resc.register("*/1 * * * *")
    def world(a,b):
        import time
        print(time.time())
    world(1,b="resc test script")

def test_remote():
    resc = Resc(
        cpu={"threshold":0.0,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="* * * * *",
        rescdir="rescs",
        outputfile="output",
        ip="13.231.122.182",
        username="ubuntu",
        password="example",
        call_first=True,
    )
    def hello():
        print("hello resc!!!")
    hello()
