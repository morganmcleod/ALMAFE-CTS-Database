""" Create and read records in the DBBand6Cart.PhaseDrift_Calc_Data table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.PhaseStabilityRecord import PhaseStabilityRecord, COLUMNS
from .schemas.CombineTestsRecord import CombineTestsRecord
from typing import List
from datetime import datetime

class PhaseStability():
    """ Create and read records in the DBBand6Cart.PhaseDrift_Calc_Data table
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor
        
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, records: List[PhaseStabilityRecord]) -> bool:
        """ Insert records

        :param records to insert. Each record.key will be updated with the new keyAmplitudeStability
        :return True if success
        """       
        q = f"INSERT INTO PhaseDrift_Calc_Data({','.join(COLUMNS[1:])}) VALUES "
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
    
    def read(self, keyId: int = None, fkCartTest: int = None, fkRawData: int = None) -> List[PhaseStabilityRecord]:
        """ Read one or more records
        
        Either keyId or fkCartTest must be provided.
        :param int keyId: of a specific record to read, defaults to None
        :param int fkCartTest: read all associated records, defaults to None
        :return List[PhaseStabilityRecord]
        """
        assert keyId or fkCartTest or fkRawData

        q = f"SELECT {','.join(COLUMNS)} FROM PhaseDrift_Calc_Data"
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
        return [PhaseStabilityRecord(
            key = row[0],
            fkCartTest = row[1],
            fkRawData = row[2],
            timeStamp = makeTimeStamp(row[3]),
            freqLO = row[4],
            freqCarrier = row[5],
            pol = row[6],
            sideband = row[7],
            time = row[8],
            allanDev = row[9],
            errorBar = row[10],
        ) for row in rows]
    
    def readSubTests(self, fkParentTest:int) -> List[CombineTestsRecord]:
        q = f"SELECT MIN(TS), FreqCarrier, Pol, SB FROM PhaseDrift_Calc_Data WHERE fkCartTest={fkParentTest} GROUP BY FreqLO, Pol, SB;"
        
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
            FROM PhaseDrift_Calc_Data GROUP BY fkCartTest ORDER BY fkCartTest;"""
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

    def isNewerData(self, timeStamp: datetime) -> bool:
        q = f"SELECT TS FROM PhaseDrift_Calc_Data WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False