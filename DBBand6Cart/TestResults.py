from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional
import json

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
    timeStamp: Optional[datetime] = datetime.now()
    plots: Optional[List[int]] = []

class TestResults(object):
    '''
    Create, Read, Update, Delete table dbBand6Cart.TestResults records
    '''

    columns = ('keyTestResult',
               'fkCartTests',
               'DataStatus',
               'WhenAccepted',
               'AcceptedBy',
               'MeasurementSW',
               'AnalysisSW',
               'Description',
               'Timestamp',
               'Plots')

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, result:TestResult):
        '''
        Create a new record in the TestResults table
        :param result: contents of record
        :return TestResult of new record or None if failed
        '''
        try:
            plots = json.dumps(result.plots) if result.plots else ''
        except:
            plots = ''
        values = "{},{},'{}','{}','{}','{}','{}','{}','{}'".format(
            result.fkCartTests,
            result.dataStatus.value,
            result.whenAccepted.strftime(self.DB.TIMESTAMP_FORMAT) if result.whenAccepted else '',
            result.acceptedBy if result.acceptedBy else '', 
            result.measurementSW if result.measurementSW else '',
            result.analysisSW if result.analysisSW else '',
            result.description if result.description else '',
            result.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT),
            plots)
    
        # make column list, skipping keyCartTest:
        q = "INSERT INTO TestResults({}) VALUES ({});".format(",".join(self.columns[1:]), values)
        print(q)
        self.DB.execute(q, commit = True)
        
        # get the value for keyCartTest:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            result.key = row[0]
            return result

    def update(self, result:TestResult):
        '''
        Update the given TestResults record
        :param TestResults record to update from, specified by key or fkCartTests
        :return keyTestResult if successful, None otherwise
        '''
        where = " WHERE "
        if result.key:
            where += "keyTestResult = {};".format(result.key)
        elif result.fkCartTests:
            where += "fkCartTests = {};".format(result.fkCartTests)
        else:
            raise ValueError("Either key or fkCartTests must be provided")
            
        q = "UPDATE TestResults SET {} = {}".format(self.columns[2], result.dataStatus.value)
        if not result.whenAccepted:
            result.whenAccepted = datetime.min
        try:
            plots = json.dumps(result.plots) if result.plots else ''
        except:
            plots = ''
        q += ", {} = '{}'".format(self.columns[3], result.whenAccepted.strftime(self.DB.TIMESTAMP_FORMAT))
        q += ", {} = '{}'".format(self.columns[4], result.acceptedBy if result.acceptedBy else '')
        q += ", {} = '{}'".format(self.columns[5], result.measurementSW if result.measurementSW else '')
        q += ", {} = '{}'".format(self.columns[6], result.analysisSW if result.analysisSW else '')
        q += ", {} = '{}'".format(self.columns[7], result.description if result.description else '')
        q += ", {} = '{}'".format(self.columns[8], result.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT))
        q += ", {} = '{}'".format(self.columns[9], plots)
        q += where;
        
        if self.DB.execute(q, commit = True):
            return result
        else:
            return None
    
    def createOrUpdate(self, result:TestResult):
        '''
        Create or update the given TestResults record
        :param result: TestResults record, specified by fkCartTests
        '''
        existing = self.read(fkCartTests = result.fkCartTests) 
        if existing:
            result.key = existing.key
            return self.update(result)
        else:
            return self.create(result)
        
    def read(self, keyResults:int = None, fkCartTests:int = None):
        '''
        Read a specific record from TestResults, specified by the either keyResults or fkCartTest
        :param keyResults: key of record to read or None
        :param fkCartTest: key of record to read or None.  One of the two must be specified.
        :return TestResult or None if not found
        '''
        q = "SELECT {} FROM TestResults WHERE ".format(",".join(self.columns))
        if keyResults:
            q += "keyTestResult = {};".format(keyResults)
        elif fkCartTests:
            q += "fkCartTests = {};".format(fkCartTests)
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
        '''
        Delete the specified TestResults record, specified by the either keyResults or fkCartTest
        :param keyResults: key of record to read or None
        :param fkCartTest: key of record to read or None.  One of the two must be specified.
        :return True if successful
        '''
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
