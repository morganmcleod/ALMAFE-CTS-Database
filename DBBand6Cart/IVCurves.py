from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.IVCurvePoint import IVCurvePoint, COLUMNS
from .schemas.CombineTestsRecord import CombineTestsRecord
from .schemas.DUT_Type import DUT_Type
from datetime import datetime

class IVCurves():

    """ Create, Read, Update, Delete records in table DBBand6Cart.MxrIVcurves
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, 
            fkMxrPreampAssy: int = None,
            fkMxrTest: int = None, 
            freqLO: float = None,
            mixerChip: str = None
        ) -> list[IVCurvePoint]:
        """ Read iv curve points

        :param int fkMxrPreampAssy: filter for a particular mixer assy
        :param int fkMxrTest: filter for a specific mixer test
        :return List[IVCurvePoint]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM MxrIVcurves WHERE "
        where = ""        
        if fkMxrPreampAssy is not None:
            if where:
                where += " AND "
            where += f"fkMxrPreampAssys = {fkMxrPreampAssy}"
        if fkMxrTest is not None:
            if where:
                where += " AND "
            where += f"fkMxrTests = {fkMxrTest}"
        if freqLO is not None:
            if where:
                where += " AND "
            where += f"FreqLO = {freqLO}"
        if mixerChip is not None:
            if where:
                where += " AND "
            where += f"MixerChip = '{mixerChip}'"

        if not where:
            return []

        q += where + " ORDER BY keyMxrIVsweep ASC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [IVCurvePoint(
            key = row[0],
            fkMxrPreampAssys = row[1],
            fkMixerTest = row[2],
            FreqLO = row[3],
            MixerChip = row[4],
            Imag = row[5],
            Vj = row[6],
            Ij = row[7],
            IFPower = row[8],
            isPCold = True if row[9] else False,
            PumpPwr = row[10],
            timeStamp = makeTimeStamp(row[11])
        ) for row in rows]
    
    def create(self, points: list[IVCurvePoint]) -> bool:
        """ Create new records

        :param list[IVCurvePoint] points: records to insert
        :return bool: true if successful
        """
        q = f"INSERT INTO MxrIVcurves ({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for row in points:
            row.timeStamp = datetime.now()
            if values:
                values += ","
            values += f"({row.getInsertVals()})"
    
        if values == "":
            return False

        q += values + ";"
        return self.DB.execute(q, commit = True)

    def readCartTests(self):
        """
        Read the distinct values of fkMxrTests in the table.
        
        TODO: this query would benefit from an index on fkMxrTests.
        :return list[int]
        """
        # this query excludes all the very old records:
        q = """SELECT fkMxrTests, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS
            FROM MxrIVcurves WHERE fkMxrTests IS NOT NULL AND fkMxrTests > 1
            GROUP BY fkMxrTests;"""
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
        q = f"SELECT TS FROM MxrIVcurves WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False
    
    def readLOFreqs(self, fkMixerTest: int):
        """
        Read the available LO frequencies for a fkCartTest
        :param fkCartTest: fkCartTest or fkMxrTest
        :return list[CombineTestsRecord] or None if not found
        """
        q = f"SELECT MIN(TS), FreqLO FROM MxrIVcurves WHERE fkMxrTests={fkMixerTest}"
        q += " GROUP BY FreqLO;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [CombineTestsRecord(
                key = 0,
                fkParentTest = fkMixerTest,
                fkDutType = DUT_Type.Unknown.value,
                timeStamp = row[0],         # MIN(TS)
                path0_TestId = 0,
                path1 = str(row[1]),        # frequency
                text = str(row[1])          # frequency
            ) for row in rows]
