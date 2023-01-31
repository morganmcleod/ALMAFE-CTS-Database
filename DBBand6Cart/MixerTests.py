from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.MixerTest import MixerTest, COLUMNS
from typing import List

class MixerTests():
    '''
    Create, Read, Update, Delete table dbBand6Cart.MixerTests records
    Each record represents a set of measurement data, normally taken as a single measurement operation.
    '''
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        # string which gets reused below:
        self.queryColumns = ",".join(['MT.' + name for name in COLUMNS])
        
    def create(self, mixerTest:MixerTest):
        '''
        Create a new record in the MixerTests table
        :param mixerTest: contents of record
        :return int keyMixerTest of new record or None if failed
        '''
        values = "{},{},{},'{}','{}','{}'".format(mixerTest.configId, 
                                                  mixerTest.fkSoftwareVersion, 
                                                  mixerTest.fkTestType,
                                                  mixerTest.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT),
                                                  mixerTest.description, 
                                                  mixerTest.operator)
        
        # make column list, skipping keyMixerTest:
        q = "INSERT INTO MxrTests({}) VALUES ({});".format(",".join(COLUMNS[1:]), values)
        self.DB.execute(q, commit = True)
        
        # get the value for keyMixerTest:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            mixerTest.key = row[0]
            return row[0]
        
    def read(self, keyMixerTest:int = None, 
                   configId:int = None, 
                   keyTestType:int = None):
        '''
        Read one or more MixerTest records

        :param keyMixerTest: optional int filter for a single mixerTest
        :param configId: int filter for this configuration
        :param keyTestType: keyMixerTest: optional int filter for a single mixerTest
        :return list[MixerTest] or None if not found
        '''
        q = "SELECT {} FROM MxrTests AS MT".format(self.queryColumns)                
        where = ""
        
        if keyMixerTest: 
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " MT.keyMxrTest = {}".format(keyMixerTest)
            
        if configId:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " MT.fkMxrPreampAssys = {}".format(configId)
        
        if keyTestType:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " MT.fkTestType = {}".format(keyTestType)

        q += where          
        q += " ORDER BY MT.keyMxrTest DESC;"
    
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of MixerTest:            
            return [MixerTest(key = row[0],
                              configId = row[1],
                              fkSoftwareVersion = row[2],
                              fkTestType = row[3],
                              timeStamp =  makeTimeStamp(row[4]), 
                              description = row[5] if row[5] else '',
                              operator = row[6] if row[6] else ''
                             ) for row in rows]
            
    def update(self, MixerTest):
        '''
        Update the given MixerTests record
        :param MixerTest
        :return True if successful
        '''
        # TODO: implement MixerTests.update when needed
        raise(NotImplementedError)
    
    def delete(self, keyMixerTest:int):
        '''
        Delete the specified MixerTests record
        :param keyMixerTest
        :return True if successful
        '''
        return self.deleteMany([keyMixerTest])
        
    def deleteMany(self, keys:List[int]):
        '''
        Delete the specified MixerTests records
        :param List[keyMixerTest]
        :return True if successful
        '''
        strKeys = [str(key) for key in keys]
        q = "DELETE FROM MxrTests WHERE keyMxrTest in ({});".format(','.join(strKeys))
        return self.DB.execute(q, commit = True)
