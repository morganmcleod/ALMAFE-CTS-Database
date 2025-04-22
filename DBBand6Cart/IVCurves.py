from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.IVCurvePoint import IVCurvePoint, COLUMNS
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
            fkMxrTest: int = None
        ) -> list[IVCurvePoint]:
        """ Read iv curve points

        :param int fkMxrPreampAssy: filter for a particular mixer assy
        :param int fkMxrTest: filter for a specific mixer test
        :return List[IVCurvePoint]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM MxrIVcurves WHERE "
        where = None        
        if fkMxrPreampAssy is not None:
            if where:
                where += " AND "
            where += f"fkMxrPreampAssys = {fkMxrPreampAssy}"
        if fkMxrTest is not None:
            if where:
                where += " AND "
            where += f"fkMxrTests = {fkMxrTest}"
        if not where:
            return []

        q += where + " ORDER BY keyMxrIVsweep ASC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [IVCurvePoint(
            key = row[0],
            fkMixerChips = row[1],
            fkMixerTest = row[2],
            FreqLO = row[3],
            MixerChip = row[4],
            Imag = row[5],
            Vj = row[6],
            Ij = row[7],
            IFPower = row[8],
            PumpPwr = row[9],
            timeStamp = makeTimeStamp(row[10])
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
