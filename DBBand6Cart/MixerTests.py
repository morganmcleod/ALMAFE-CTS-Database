""" Create, Read, Update, Delete records in table DBBand6Cart.MixerTests
"""
import configparser
from datetime import datetime
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.MixerTest import MixerTest, COLUMNS
from .GetLastInsertId import getLastInsertId
from typing import List, Optional

class MixerTests():
    """
    Create, Read, Update, Delete table dbBand6Cart.MixerTests records
    Each record represents a measurement initiated by the MTS user.
    """
    def __init__(self, 
            connectionInfo:dict = None, 
            driver:DriverMySQL = None, 
            defaultFkTestSystem = None
        ):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        # string which gets reused below:
        self.queryColumns = ",".join(['MT.' + name for name in COLUMNS])
        # load the default value for fkTestSystem:
        if defaultFkTestSystem is not None:
            self.defaultFkTestSystem = defaultFkTestSystem
        else:
            try:
                config = configparser.ConfigParser()
                config.read('ALMAFE-CTS-Database.ini')
                self.defaultFkTestSystem = int(config['MixerTests']['fkTestSystem'])
            except:
                self.defaultFkTestSystem = 0
                
    def create(self, mixerTest:MixerTest) -> int:
        """
        Create a new record in the MixerTests table
        :param mixerTest: contents of record
        :return int keyMixerTest of new record or None if failed
        """
        # use the fkTestSystem loaded from the config file:
        if mixerTest.fkTestSystem == 0:
            mixerTest.fkTestSystem = self.defaultFkTestSystem
        if mixerTest.timeStamp is None:
            mixerTest.timeStamp = datetime.now()
        # make column list, skipping keyMixerTest:
        q = f"INSERT INTO MxrTests({','.join(COLUMNS[1:])}) VALUES ({mixerTest.getInsertVals()});"
        self.DB.execute(q, commit = True)
        mixerTest.key = getLastInsertId(self.DB)
        return mixerTest.key
        
    def read(self, 
            keyMixerTest:int = None, 
            configId:int = None, 
            keyTestType:int = None,
            keyTestSystem: int = None,
            serialNum:str = None) -> Optional[List[MixerTest]]:
        """
        Read one or more MixerTest records

        :param keyMixerTest: optional int filter for a single mixerTest
        :param configId: int filter for this configuration
        :param keyTestType: optional int filter for one test type
        :param keyTestSystem: optional int filter for one test system
        :param serialNum: str filter all MxrPreampAssys configs for a given serial num
        :return list[MixerTest] or None if not found
        """
        q = f"SELECT {self.queryColumns} FROM MxrTests AS MT"
        where = ""
        
        if serialNum:
            q += " JOIN MxrPreampAssys AS MA ON MT.fkMxrPreampAssys = MA.keyMxrPreampAssys" 
            where = f" WHERE MA.SN = '{serialNum}'"

        if keyMixerTest: 
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += f" MT.keyMxrTest = {keyMixerTest}"
            
        if configId:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += f" MT.fkMxrPreampAssys = {configId}"
        
        if keyTestType:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += f" MT.fkTestType = {keyTestType}"

        if keyTestSystem:
            if not where:
                where = " WHERE"
            else: 
                where += " AND"
            where += f" MT.fkTestSystem = {keyTestSystem}"
        
        q += where          
        q += " ORDER BY MT.keyMxrTest DESC;"
    
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        return [MixerTest(
            key = row[0],
            configId = row[1],
            fkSoftwareVersion = row[2],
            fkTestType = row[3],
            fkTestSystem = row[4],
            timeStamp =  makeTimeStamp(row[5]), 
            description = row[6] if row[6] else '',
            operator = row[7] if row[6] else ''
        ) for row in rows]
            
    def update(self, mixerTest: MixerTest):
        """
        Update the given MixerTests record
        :param mixerTest: MixerTest record
        :return True if successful
        """
        q = "UPDATE MxrTests SET "
        q += f"fkMxrPreampAssys={mixerTest.configId}"
        q += f", fkSoftwareVersion={mixerTest.fkSoftwareVersion}"
        q += f", fkTestType={mixerTest.fkTestType}"
        q += f", fkTestSystem={mixerTest.fkTestSystem}"
        if mixerTest.timeStamp:
            q += f", Timestamp='{mixerTest.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT)}'"
        else:
            q += f", Timestamp='{datetime.now().strftime(self.DB.TIMESTAMP_FORMAT)}'"
        q += f", Description='{mixerTest.description}'"
        q += f", Operator='{mixerTest.operator}'"
        q += f" WHERE keyMxrTest={mixerTest.key}"
        return self.DB.execute(q, commit = True)

    def delete(self, keyMixerTest:int):
        """
        Delete the specified MixerTests record
        :param keyMixerTest
        :return True if successful
        """
        return self.deleteMany([keyMixerTest])
        
    def deleteMany(self, keys:List[int]):
        """
        Delete the specified MixerTests records
        :param List[keyMixerTest]
        :return True if successful
        """
        strKeys = [str(key) for key in keys]
        q = f"DELETE FROM MxrTests WHERE keyMxrTest in ({','.join(strKeys)});"
        return self.DB.execute(q, commit = True)
