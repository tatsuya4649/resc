import pytest
from resc.detect import *

#@pytest.fixture(scope="function",autouse=False)
#def setup_dbase():
#    # Base Class of Resource Detect
#    detect_base = DetectBase()
#    yield detect_base

def test_init():
    with pytest.raises(
        DetectInheritenceError
    ):
        detect_base = DetectBase()

#
#def test_resource(setup_dbase):
#    with pytest.raises(
#        DetectBaseNotImplementedError
#    ) as raiseinfo:
#        setup_dbase.resource
#    print(f"DETECT BASE CLASS RESOURCE IMPL: {raiseinfo.value}")
#
#def test_mode(setup_dbase):
#    with pytest.raises(
#        DetectBaseNotImplementedError
#    ) as raiseinfo:
#        setup_dbase.mode
#    print(f"DETECT BASE CLASS MODE IMPL: {raiseinfo.value}")
#
#def test_check(setup_dbase):
#    with pytest.raises(
#        DetectBaseNotImplementedError
#    ) as raiseinfo:
#        setup_dbase.check
#    print(f"DETECT BASE CLASS CHECK IMPL: {raiseinfo.value}")
#
#def test_threshold(setup_dbase):
#    with pytest.raises(
#        DetectBaseNotImplementedError
#    ) as raiseinfo:
#        setup_dbase.threshold
#    print(f"DETECT BASE CLASS THRESHOLD IMPL: {raiseinfo.value}")
#
#def test_percent(setup_dbase):
#    with pytest.raises(
#        DetectBaseNotImplementedError
#    ) as raiseinfo:
#        setup_dbase.percent
#    print(f"DETECT BASE CLASS PERCENT IMPL: {raiseinfo.value}")
#
