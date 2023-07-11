from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BPCenterPower import BPCenterPower, COLUMNS

class BPCenterPowers():
    '''
    Beam pattern center powers table in dbBand6Cart
    '''

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BPCenterPower):
        values = "{},{},{},'{}',{}".format(
            record.fkBeamPatterns,
            record.Amplitude,
            record.Phase,
            datetime.now(),
            1 if record.ScanComplete else 0
        )
        q = f"INSERT INTO BP_Center_Pwrs({','.join(COLUMNS[1:])}) VALUES ({values});"
        self.DB.execute(q, commit = True)

        # get the value for keyBP_Center_Pwrs:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            record.key = row[0]
            return row[0]

    def read(self, keyId:int = None, fkBeamPatterns:int = None) -> List[BPCenterPower]:
        q = f"SELECT {','.join(COLUMNS)} FROM BP_Center_Pwrs"
        where = ""
        if keyId:
            where += f"keyBP_Center_Pwrs = {keyId}"
        if fkBeamPatterns:
            if where:
                where += " AND "
            where += f"fkBeamPatterns = {fkBeamPatterns}"

        if where:
            q += " " + where
        
        q += " ORDER BY keyBP_Center_Pwrs ASC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BPCenterPower(
            key = row[0],
            fkBeamPatterns = row[1],
            Amplitude = row[2],
            Phase = row[3],
            timeStamp = makeTimeStamp(row[4]),
            ScanComplete = row[5] != 0
        ) for row in rows]
    
    def update(self, BPCenterPower):
        '''
        Update the given BPCenterPower record
        :param BPCenterPower
        :return True if successful
        '''
        # TODO: implement BPCenterPowers.update when needed
        raise(NotImplementedError)
    
    def delete(self, key:int):
        '''
        Delete the specified BPCenterPower record
        :param key
        :return True if successful
        '''
        # TODO: implement BPCenterPowers.delete when needed
        raise(NotImplementedError)