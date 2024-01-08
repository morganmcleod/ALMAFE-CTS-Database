from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .GetLastInsertId import getLastInsertId
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional
import json

# CREATE TABLE `TestResults` (
# 	`keyTestResult` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartTests` INT(11) UNSIGNED NOT NULL DEFAULT '0',
# 	`DataStatus` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
# 	`WhenAccepted` DATETIME NULL DEFAULT NULL,
# 	`AcceptedBy` TINYTEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`MeasurementSW` TINYTEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`AnalysisSW` TINYTEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Timestamp` DATETIME NULL DEFAULT NULL,
# 	`Description` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Plots` TEXT NULL DEFAULT NULL COMMENT 'JSON structure describing plot IDs to load' COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY (`keyTestResult`) USING BTREE,
# 	INDEX `Index 2` (`fkCartTests`) USING BTREE
# )


class DataStatus(Enum):
    UNDEFINED = 0
    MEASURED = 1
    PROCESSED = 2
    REJECTED = 3
    ACCEPTED = 4
    FOR_REPORT = 5

class TestResult(BaseModel):
    key: int = None             # keyResults
    fkCartTests: int = None
    dataStatus: DataStatus = DataStatus.UNDEFINED
    whenAccepted: Optional[datetime] = datetime.min
    acceptedBy: Optional[str] = ""
    measurementSW: Optional[str] = ""
    analysisSW: Optional[str] = ""
    description: Optional[str] = ""
    timeStamp: datetime = None
    plots: Optional[List[int]] = []

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        try:
            plots = json.dumps(self.plots) if self.plots else ''
        except:
            plots = ''
        return "{},{},{},'{}','{}','{}','{}','{}','{}'".format(
            self.fkCartTests,
            self.dataStatus.value,
            f"'{self.whenAccepted}'" if self.whenAccepted else "NULL",
            self.acceptedBy if self.acceptedBy else '', 
            self.measurementSW if self.measurementSW else '',
            self.analysisSW if self.analysisSW else '',
            self.description if self.description else '',
            self.timeStamp,
            plots
        )

COLUMNS = (
    'keyTestResult',
    'fkCartTests',
    'DataStatus',
    'WhenAccepted',
    'AcceptedBy',
    'MeasurementSW',
    'AnalysisSW',
    'Description',
    'Timestamp',
    'Plots'
)

class TestResults(object):
    """
    Create, Read, Update, Delete table dbBand6Cart.TestResults records
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, result:TestResult):
        """
        Create a new record in the TestResults table
        :param result: contents of record
        :return TestResult of new record or None if failed
        """
        # make column list, skipping keyCartTest:
        q = f"INSERT INTO TestResults({','.join(COLUMNS[1:])}) VALUES ({result.getInsertVals()});"
        self.DB.execute(q, commit = True)
        result.key = getLastInsertId(self.DB)
        return result

    def update(self, result:TestResult):
        """
        Update the given TestResults record
        :param TestResults record to update from, specified by key or fkCartTests
        :return keyTestResult if successful, None otherwise
        """
        where = " WHERE "
        if result.key:
            where += "keyTestResult = {};".format(result.key)
        elif result.fkCartTests:
            where += "fkCartTests = {};".format(result.fkCartTests)
        else:
            raise ValueError("Either key or fkCartTests must be provided")
            
        q = "UPDATE TestResults SET "
        if not result.whenAccepted:
            result.whenAccepted = datetime.min
        try:
            plots = json.dumps(result.plots) if result.plots else ''
        except:
            plots = ''
        q += "{} = {}".format(COLUMNS[2], result.dataStatus.value)
        q += ", {} = '{}'".format(COLUMNS[3], result.whenAccepted.strftime(self.DB.TIMESTAMP_FORMAT))
        q += ", {} = '{}'".format(COLUMNS[4], result.acceptedBy if result.acceptedBy else '')
        q += ", {} = '{}'".format(COLUMNS[5], result.measurementSW if result.measurementSW else '')
        q += ", {} = '{}'".format(COLUMNS[6], result.analysisSW if result.analysisSW else '')
        q += ", {} = '{}'".format(COLUMNS[7], result.description if result.description else '')
        q += ", {} = '{}'".format(COLUMNS[8], result.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT))
        q += ", {} = '{}'".format(COLUMNS[9], plots)
        q += where
        
        if self.DB.execute(q, commit = True):
            return result
        else:
            return None
    
    def createOrUpdate(self, result:TestResult):
        """
        Create or update the given TestResults record
        :param result: TestResults record, specified by fkCartTests
        """
        existing = self.read(fkCartTests = result.fkCartTests) 
        if existing:
            result.key = existing.key
            return self.update(result)
        else:
            return self.create(result)
        
    def read(self, keyResults:int = None, fkCartTests:int = None):
        """
        Read a specific record from TestResults, specified by the either keyResults or fkCartTest
        :param keyResults: key of record to read or None
        :param fkCartTest: key of record to read or None.  One of the two must be specified.
        :return TestResult or None if not found
        """
        q = f"SELECT {','.join(COLUMNS)} FROM TestResults WHERE "
        if keyResults:
            q += f"keyTestResult = {keyResults};"
        elif fkCartTests:
            q += f"fkCartTests = {fkCartTests};"
        else:
            raise ValueError("Either keyResults or fkCartTests must be provided")
        
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            try:
                plots = json.loads(row[9]) if row[9] else []
            except:
                plots = []
            return TestResult(key = row[0],
                              fkCartTests = row[1],
                              dataStatus = DataStatus(row[2]),
                              whenAccepted = makeTimeStamp(row[3]) if row[3] else datetime.min,
                              acceptedBy = row[4] if row[4] else '',
                              measurementSW = row[5] if row[5] else '',
                              analysisSW = row[6] if row[6] else '',
                              description = row[7] if row[7] else '',
                              timeStamp = makeTimeStamp(row[8]),
                              plots = plots)
    
    def delete(self, keyResults:int = None, fkCartTests:int = None):
        """
        Delete the specified TestResults record, specified by the either keyResults or fkCartTest
        :param keyResults: key of record to read or None
        :param fkCartTest: key of record to read or None.  One of the two must be specified.
        :return True if successful
        """
        q = "DELETE FROM TestResults WHERE "
        if keyResults:
            q += "keyTestResult = {};".format(keyResults)
        elif fkCartTests:
            q += "fkCartTests = {};".format(fkCartTests)
        else:
            raise ValueError("Either keyResults or fkCartTests must be provided")            
            
        if self.DB.execute(q, commit = True):
            return True
        else:
            return False
