""" Create, Read, Update, Delete table dbBand6Cart.CartTests records
"""    
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.CartTest import CartTest, COLUMNS
from .GetLastInsertId import getLastInsertId
from typing import List, Optional
from datetime import datetime
import configparser

class CartTests(object):
    """ Create, Read, Update, Delete table dbBand6Cart.CartTests records

    Each record represents a measurement initiated by the CTS user.
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        # string which gets reused below:
        self.queryColumns = ",".join(['CT.' + name for name in COLUMNS])
        # load the default value for fkTestSystem:
        try:
            config = configparser.ConfigParser()
            config.read('ALMAFE-CTS-Database.ini')
            self.defaultFkTestSystem = int(config['CartTests']['fkTestSystem'])
        except:
            self.defaultFkTestSystem = 0
        
    def create(self, cartTest:CartTest) -> Optional[int]:
        """
        Create a new record in the CartTests table
        :param cartTest: contents of record
        :return int keyCartTest of new record or None if failed
        """
        # use the fkTestSystem loaded from the config file:
        if cartTest.fkTestSystem == 0:
            cartTest.fkTestSystem = self.defaultFkTestSystem
        # make column list, skipping keyCartTest:
        q = f"INSERT INTO CartTests({','.join(COLUMNS[1:])}) VALUES ({cartTest.getInsertVals()});"
        self.DB.execute(q, commit = True)
        cartTest.key = getLastInsertId(self.DB)
        return cartTest.key
        
    def read(self, keyCartTest:int = None, 
                   configId:int = None, 
                   keyTestType:int = None,
                   serialNum:str = None, 
                   withSelection = False) -> Optional[List[CartTest]]:
        """
        Read one or more CartTest records

        TODO: Performance of this query would benefit from an index on fkCartAssembly
        TODO: ideally for performance, isSelection would be a native column on CartTests
        
        :param keyCartTest: optional int filter for a single cartTest
        :param configId: int filter for this configuration
        :param keyTestType: keyCartTest: optional int filter for a single cartTest
        :param serialNum: optional filter by CartAssembly.sn instead of configId to get all configs for this SN
        :param withSelection: if true, the isSelection column is derived from a JOIN with the CartTestsSelection table.
        :return list[CartTest] or None if not found
        """
        sel = ", SEL.fkCartTests" if withSelection else ""
        q = f"SELECT {self.queryColumns}{sel} FROM CartTests AS CT"
        where = ""
        
        if serialNum:
            q += " JOIN ColdCarts AS CC ON CT.fkColdCarts = CC.keyColdCarts" 
            where = f" WHERE CC.SN = '{int(serialNum):03}'"
        
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
            where += " CT.fkColdCarts = {}".format(configId)
        
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

        return [CartTest(key = row[0],
            cartAssyId = row[1],
            configId = row[2],
            fkSoftwareVersion = row[3],
            fkTestType = row[4],
            fkTestSystem = row[5],
            timeStamp =  makeTimeStamp(row[6]), 
            description = row[7] if row[7] else '',
            operator = row[8] if row[8] else '',
            testSysName = row[9] if row[9] else '',
            isSelection = True if withSelection and row[10] else False,
        ) for row in rows]
            
    def update(self, CartTest):
        """
        Update the given CartTests record
        :param CartTest
        :return True if successful
        """
        # TODO: implement CartTests.update when needed
        raise(NotImplementedError)
    
    def delete(self, keyCartTest:int):
        """
        Delete the specified CartTests record
        :param keyCartTest
        :return True if successful
        """
        return self.deleteMany([keyCartTest])
        
    def deleteMany(self, keys:List[int]):
        """
        Delete the specified CartTests records
        :param List[keyCartTest]
        :return True if successful
        """
        strKeys = [str(key) for key in keys]
        q = f"DELETE FROM CartTests WHERE keyCartTest in ({','.join(strKeys)});"
        return self.DB.execute(q, commit = True)
