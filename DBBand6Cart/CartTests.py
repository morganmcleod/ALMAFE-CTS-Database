from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.CartTest import CartTest, COLUMNS
from typing import List, Optional

class CartTests(object):
    '''
    Create, Read, Update, Delete table dbBand6Cart.CartTests records
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
        self.queryColumns = ",".join(['CT.' + name for name in COLUMNS])
        
    def create(self, cartTest:CartTest) -> Optional[int]:
        '''
        Create a new record in the CartTests table
        :param cartTest: contents of record
        :return int keyCartTest of new record or None if failed
        '''
        values = "{},{},{},{},'{}','{}','{}','{}'".format(cartTest.configId, 
                                                     cartTest.fkSoftwareVersion, 
                                                     cartTest.fkTestType,
                                                     cartTest.fkTestSystem, 
                                                     cartTest.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT),
                                                     cartTest.description, 
                                                     cartTest.operator,
                                                     cartTest.testSysName)
        
        # make column list, skipping keyCartTest:
        q = "INSERT INTO CartTests({}) VALUES ({});".format(",".join(COLUMNS[1:]), values)
        self.DB.execute(q, commit = True)
        
        # get the value for keyCartTest:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            cartTest.key = row[0]
            return row[0]
        
    def read(self, keyCartTest:int = None, 
                   configId:int = None, 
                   keyTestType:int = None,
                   serialNum:str = None, 
                   withSelection = False):
        '''
        Read one or more CartTest records

        TODO: Performance of this query would benefit from an index on fkCartAssembly

        :param keyCartTest: optional int filter for a single cartTest
        :param configId: int filter for this configuration
        :param keyTestType: keyCartTest: optional int filter for a single cartTest
        :param serialNum: optional filter by CartAssembly.sn instead of configId to get all configs for this SN
        :param withSelection: if true, the isSelection column is derived from a JOIN with the CartTestsSelection table.
              TODO ideally for performance, this would be a native column on CartTests
        :return list[CartTest] or None if not found
        '''
        q = "SELECT {}{} FROM CartTests AS CT".format(self.queryColumns, ", SEL.fkCartTests" if withSelection else "")                
        where = ""
        
        if serialNum:
            q += " JOIN CartAssemblies AS CA ON CT.fkCartAssembly = CA.keyCartAssys" 
            where = " WHERE CA.SN = {}".format(int(serialNum))
        
        if withSelection:
            q += " LEFT JOIN (SELECT DISTINCT fkCartTests FROM CartTestsSelection) AS SEL ON SEL.fkCartTests = CT.keyCartTest"
        
        if keyCartTest: 
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " CT.keyCartTest = {}".format(keyCartTest)
            
        if configId:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " fkCartAssembly = {}".format(configId)
        
        if keyTestType:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += " CT.fkTestType = {}".format(keyTestType)

        q += where          
        q += " ORDER BY CT.keyCartTest DESC;"
    
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of CartTest:            
            return [CartTest(key = row[0],
                             configId = row[1],
                             fkSoftwareVersion = row[2],
                             fkTestType = row[3],
                             fkTestSystem = row[4],
                             timeStamp =  makeTimeStamp(row[5]), 
                             description = row[6] if row[6] else '',
                             operator = row[7] if row[7] else '',
                             testSysName = row[8] if row[8] else '',
                             isSelection = True if withSelection and row[9] else False,
                             ) for row in rows]
            
    def update(self, CartTest):
        '''
        Update the given CartTests record
        :param CartTest
        :return True if successful
        '''
        # TODO: implement CartTests.update when needed
        raise(NotImplementedError)
    
    def delete(self, keyCartTest:int):
        '''
        Delete the specified CartTests record
        :param keyCartTest
        :return True if successful
        '''
        return self.deleteMany([keyCartTest])
        
    def deleteMany(self, keys:List[int]):
        '''
        Delete the specified CartTests records
        :param List[keyCartTest]
        :return True if successful
        '''
        strKeys = [str(key) for key in keys]
        q = "DELETE FROM CartTests WHERE keyCartTest in ({});".format(','.join(strKeys))
        return self.DB.execute(q, commit = True)
