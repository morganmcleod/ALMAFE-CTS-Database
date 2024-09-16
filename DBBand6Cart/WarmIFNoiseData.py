from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pandas import DataFrame
import numpy as np
from .schemas.WarmIFNoise import COLUMNS, WarmIFNoise
from .schemas.DUT_Type import DUT_Type
from datetime import datetime
from typing import Dict, Union, List

EXTENDED_COLUMNS = COLUMNS
EXTENDED_COLUMNS += (
    'Y_dB',
    'Gain_dB',
    'Tr_K'
)

class WarmIFNoiseData(object):
    """
    Create, Read, Update, Delete records in dbBand6Cart.WarmIF_Noise_Data
    We use pandas.DataFrame to convey records in and out.
    """ 
    BOLTZMANN = 1.38E-23 # J/K
    BW_NOISE = 100000000 # Hz
    PAD_DB = 0
    PAD_R = 10 ** (-PAD_DB / 10) # ratio

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, records: List[WarmIFNoise]):
        """
        Create records in WarmIF_Noise_Data
        :param data: WarmIFNoise record
        """
        if len(records) > 0:
            # make column list, skipping keyCartTest:
            q = f"INSERT INTO WarmIF_Noise_Data({','.join(COLUMNS[1:])}) VALUES "
            first = True
            for rec in records:
                if not first:
                    q += ","
                first = False
                q += "(" + rec.getInsertVals() + ")"
            q += ";"
            self.DB.execute(q, commit = True)
    
    def read(self, fkCartTest:int, dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        """

        if dutType == DUT_Type.Band6_MxrPreampAssys:
            q = f"SELECT {','.join(EXTENDED_COLUMNS[0:7])}, "
            q += "10.0 * LOG10(Phot) + 30 AS `Phot_dBm`, "
            q += "10.0 * LOG10(Pcold) + 30 AS `Pcold_dBm`, "
            q += "10.0 * LOG10(Phot/Pcold) AS `Y_dB`, "
            q += "TifCold, TifHot, Ambient, 0 as `NoiseDiodeENR`, "
            q += f"10.0 * LOG10((Phot - Pcold) / (TifHot-TifCold) / {self.BOLTZMANN} / {self.BW_NOISE}) AS `Gain_dB`, "
            q += "(TifHot - (Phot/Pcold) * TifCold) / ((Phot/Pcold)-1) AS `Tr_K` "
            q += f"FROM WarmIF_Noise_Data WHERE (fkDUT_Type = {dutType.value} AND "
            q += f"fkCartTest = {fkCartTest} AND Attn = ( "
            q += f"SELECT MIN(Attn) FROM WarmIF_Noise_Data WHERE fkCartTest = {fkCartTest})) "
            q += "ORDER BY Attn, YIG_Freq;"
            self.DB.execute(q)
            rows = self.DB.fetchall()
            if not rows:
                return None
            return DataFrame(rows, columns = EXTENDED_COLUMNS)
        
        elif dutType == DUT_Type.Band6_Cartridge:
            q = f"SELECT {','.join(EXTENDED_COLUMNS[0:7])}, "
            q += "10.0 * LOG10(Phot) + 30 AS `Phot_dBm`, "
            q += "10.0 * LOG10(Pcold) + 30 AS `Pcold_dBm`, "
            q += "10.0 * LOG10(Phot/Pcold) AS `Y_dB`, "
            q += "Ambient AS `TifCold`, "
            q += f"290 * (POWER(10.0 ,(IF(NoiseDiodeENR = 0, 15.4, NoiseDiodeENR) / 10)) - 1) * {self.PAD_R} + Ambient * (1 - {self.PAD_R}) AS `TifHot`, "
            q += "Ambient, NoiseDiodeENR, "
            q += "0 as `Gain_dB`, 0 as `Tr_K` "
            q += f"FROM WarmIF_Noise_Data WHERE (fkDUT_Type = {dutType.value} AND "
            q += f"fkCartTest = {fkCartTest} AND Attn = ( "
            q += f"SELECT MIN(Attn) FROM WarmIF_Noise_Data WHERE fkCartTest = {fkCartTest})) "
            q += "ORDER BY Attn, YIG_Freq;"
            self.DB.execute(q)
            rows = self.DB.fetchall()
            if not rows:
                return None
            df = DataFrame(rows, columns = EXTENDED_COLUMNS)
            df['Gain_dB'] = 10.0 * np.log10(10 ** (df['Y_dB'] / 10) / (df['TifHot'] - df['Ambient']) / self.BOLTZMANN / self.BW_NOISE)
            df['Tr_K'] = (df['TifHot'] - 10 ** (df['Y_dB'] / 10) * df['Ambient']) / (10 ** (df['Y_dB'] / 10) - 1)
            return df
    
    def readCartTests(self, dutType:DUT_Type = DUT_Type.Unknown) -> Dict[int, Dict[str, Union[int, datetime]]]:
        """
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return dict: {cartTestId: {'numMeasurements': int, 'minTS': datetime, 'maxTS': datetime}
        """
        q = "SELECT fkCartTest, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS FROM WarmIF_Noise_Data"
        if dutType != DUT_Type.Unknown:
            q += f" WHERE fkDUT_Type = {dutType.value}"
        q += " GROUP BY fkCartTest ORDER BY fkCartTest;"
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
        q = f"SELECT TS FROM WarmIF_Noise_Data WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False
