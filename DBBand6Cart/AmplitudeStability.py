""" Create and read records in the DBBand6Cart.AmplitudeStability table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.AmplitudeStabilityRecord import AmplitudeStabilityRecord, COLUMNS
from .schemas.CombineTestsRecord import CombineTestsRecord
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
    
    def readSubTests(self, fkParentTest:int) -> List[CombineTestsRecord]:
        q = f"SELECT MIN(TS), FreqLO, Pol, SB FROM AmplitudeStability WHERE fkCartTest={fkParentTest} GROUP BY FreqLO, Pol, SB;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [CombineTestsRecord(
                key = row[1],
                fkParentTest = fkParentTest,
                fkDutType = 0,
                timeStamp = makeTimeStamp(row[0]),  # MIN(TimeStamp)
                path0_TestId = 0,
                path1 = str(row[1]),
                path2 = f"{row[2]} {row[3]}",
                text = f"{row[1]}",
                description = f"pol{row[2]} {'LSB' if row[3] == 1 else 'USB'}"
            ) for row in rows]

    def readCartTests(self):
        """
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return list[int]
        """
        q = """SELECT fkCartTest, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS 
            FROM AmplitudeStability GROUP BY fkCartTest;"""
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return {row[0] : {
                'numMeasurements': row[1], 
                'minTS': makeTimeStamp(row[2]), 
                'maxTS': makeTimeStamp(row[3])
            } for row in rows}
