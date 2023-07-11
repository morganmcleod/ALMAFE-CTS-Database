import os
import sys
from os.path import dirname
import unittest

# add the top-level project path to PYTHONPATH:
projectRoot = dirname(dirname(dirname(dirname(__file__))))
if not projectRoot in sys.path:
    sys.path.append(projectRoot)

# and change to that directory:
os.chdir(projectRoot)

from DBBand6Cart.Tests.Unit.CartConfigs import test_CartConfigs
from DBBand6Cart.Tests.Unit.MixerConfigs import test_MixerConfigs
from DBBand6Cart.Tests.Unit.CartTests import test_CartTests
from DBBand6Cart.Tests.Unit.TestTypes import test_TestTypes
from DBBand6Cart.Tests.Unit.MixerTests import test_MixerTests
from DBBand6Cart.Tests.Unit.Mixers import test_Mixers
from DBBand6Cart.Tests.Unit.Preamps import test_Preamps
        
if __name__ == "__main__":
    try:
        unittest.main() # run all tests
    except SystemExit:
        pass