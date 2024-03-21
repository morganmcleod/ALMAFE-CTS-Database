""" Create and read records in the DBBand6Cart.BP_Center_Pwrs table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from typing import List, Optional
from .schemas.BPCenterPower import BPCenterPower, COLUMNS
from .GetLastInsertId import getLastInsertId
from datetime import datetime

class BPCenterPowers():
    """ Create and read records in the DBBand6Cart.BP_Center_Pwrs table
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BPCenterPower) -> Optional[int]:
        """ Insert one record

        :param record to insert. record.key will be updated with the new keyBP_Center_Pwrs
        :return keyBP_Center_Pwrs: int or None if error.
        """
        q = f"INSERT INTO BP_Center_Pwrs({','.join(COLUMNS[1:])}) VALUES ({record.getInsertVals()});"
        self.DB.execute(q, commit = True)

        record.key = getLastInsertId(self.DB)
        return record.key

    def read(self, keyId:int = None, fkBeamPatterns:int = None) -> List[BPCenterPower]:
        """ Read one or more records
        
        Either keyId or fkBeamPatterns must be provided.
        :param int keyId: of a specific record to read, defaults to None
        :param int fkBeamPatterns: read all associated records, defaults to None
        :return List[BPCenterPower]
        """
        assert keyId or fkBeamPatterns

        q = f"SELECT {','.join(COLUMNS)} FROM BP_Center_Pwrs"
        where = ""
        
        if keyId:
            where += f"keyBP_Center_Pwrs = {keyId}"
        if fkBeamPatterns:
            if where:
                where += " AND "
            where += f"fkBeamPatterns = {fkBeamPatterns}"

        if where:
            q += " WHERE " + where
        
        q += f" ORDER BY {COLUMNS[0]} ASC;"
        
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
    
    def readCounts(self):
        # returns dict {(testId, keyBeamPattern): {numCenterPowers, timeStamp}}
        q = """SELECT CT.keyCartTest, BP.keyBeamPattern, COUNT(CP.keyBP_Center_Pwrs), CT.Timestamp
        FROM CartTests AS CT JOIN BeamPatterns AS BP ON CT.keyCartTest = BP.fkCartTest
        JOIN BP_Center_Pwrs AS CP ON BP.keyBeamPattern = CP.fkBeamPatterns
        WHERE CP.ScanComplete = 1
        GROUP BY CT.keyCartTest, BP.keyBeamPattern
        ORDER BY keyCartTest DESC, keyBeamPattern ASC;"""
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return {(row[0], row[1]) : {
                'numMeasurements': row[2], 
                'timeStamp': makeTimeStamp(row[3])
            } for row in rows}
    
    def isNewerData(self, timeStamp: datetime) -> bool:
        q = f"SELECT TS FROM BP_Center_Pwrs WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False

    def update(self, BPCenterPower):
        """ Update the given BPCenterPower record
        
        :param BPCenterPower
        :return True if successful
        """
        # TODO: implement BPCenterPowers.update when needed
        raise(NotImplementedError)
    
    def delete(self, key:int):
        """ Delete the specified BPCenterPower record
        
        :param key
        :return True if successful
        """
        # TODO: implement BPCenterPowers.delete when needed
        raise(NotImplementedError)
    