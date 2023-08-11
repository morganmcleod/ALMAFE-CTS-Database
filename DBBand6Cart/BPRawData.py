""" Create and read records in the DBBand6Cart.BP_Data table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BPRawDatum import BPRawDatum, COLUMNS

class BPRawData():
    """ Create and read records in the DBBand6Cart.BP_Data table
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, records: List[BPRawDatum]) -> int:
        """ Insert records

        :param List[BPRawDatum] records: to insert
        :return int: number of rows inserted
        """
        q = f"INSERT INTO BP_Data({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for rec in records:
            if values:
                values += ","
            values += "(" + rec.getInsertVals() + ")"
        
        q += values + ";"
        if self.DB.execute(q, commit = True):
            # TODO: use cursor.rowcount, move function to DriverMySQL
            return len(records)
        else:
            return 0
        
    def read(self, fkBeamPattern: int) -> List[BPRawDatum]:
        """ Read all records associated with a given scan

        :param int fkBeamPattern: the scan
        :return List[BPRawDatum]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM BP_Data WHERE fkBeamPattern = {fkBeamPattern} ORDER BY keyBP_Data ASC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BPRawDatum(
            key = row[0],
            fkBeamPattern = row[1],
            Pol = row[2],
            Position_X = row[3],
            Position_Y = row[4],
            SourceAngle = row[5],
            Power = row[6],
            Phase = row[7],
            TimeStamp = makeTimeStamp(row[8])
        ) for row in rows]
