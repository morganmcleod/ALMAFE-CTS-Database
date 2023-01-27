#
# Run this in the console to set up a CTSDatabase object for interactive use.
#
import os
import sys
from os.path import dirname
# add the top-level project path to PYTHONPATH:
projectRoot = dirname(dirname(dirname(__file__)))
os.chdir(projectRoot)
if not projectRoot in sys.path:
    sys.path.append(projectRoot)

from Database.TestResults import TestResults, TestResult
from Database.TestResultPlots import TestResultPlots, TestResultPlot
from app.LoadConfiguration import loadConfiguration

DBR = TestResults(loadConfiguration('dbBand6Cart'))
DBP = TestResultPlots(loadConfiguration('dbBand6Cart'))
