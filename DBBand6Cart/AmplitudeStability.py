""" Create and read records in the DBBand6Cart.AmplitudeStability table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.AmplitudeStabilityRecord import AmplitudeStabilityRecord, COLUMNS
from typing import List

class AmplitudeStability():
    """ Create and read records in the DBBand6Cart.AmplitudeStability table
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor
        
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, records: List[AmplitudeStabilityRecord]) -> bool:
        """ Insert records

        :param records to insert. Each record.key will be updated with the new keyAmplitudeStability
        :return True if success
        """       
        q = f"INSERT INTO AmplitudeStability({','.join(COLUMNS[1:])}) VALUES "
        first = True
        for record in records:
            if first:
                first = False
            else:
                q += ','
            q += f"({record.getInsertVals()})"
        try:
            self.DB.execute(q, commit = True)
            return True
        except:
            return False
    
    def read(self, keyId: int = None, fkCartTest: int = None, fkRawData: int = None) -> List[AmplitudeStabilityRecord]:
        """ Read one or more records
        
        Either keyId or fkCartTest must be provided.
        :param int keyId: of a specific record to read, defaults to None
        :param int fkCartTest: read all associated records, defaults to None
        :return List[AmplitudeStabilityRecord]
        """
        assert keyId or fkCartTest or fkRawData

        q = f"SELECT {','.join(COLUMNS)} FROM AmplitudeStability"
        where = ""

        if keyId:
            where += f"{COLUMNS[0]} = {keyId}"
        if fkCartTest:
            if where:
                where += " AND "
            where += f"{COLUMNS[1]} = {fkCartTest}"
        if fkRawData:
            if where:
                where += " AND "
            where += f"{COLUMNS[2]} = {fkRawData}"

        if where:
            q += " WHERE " + where
        
        q += f" ORDER BY {COLUMNS[0]} ASC;"
    
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        return [AmplitudeStabilityRecord(
            key = row[0],
            fkCartTest = row[1],
            fkRawData = row[2],
            timeStamp = makeTimeStamp(row[3]),
            freqLO = row[4],
            pol = row[5],
            sideband = row[6],
            time = row[7],
            allanVar = row[8],
            errorBar = row[9],
        ) for row in rows]
