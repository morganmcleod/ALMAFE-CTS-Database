""" Create, Read, Update, Delete records in table DBBand6Cart.MixerParams
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.PreampParam import PreampParam, COLUMNS
from typing import List
from datetime import datetime

class PreampParams():
    """ Create, Read, Update, Delete records in table DBBand6Cart.MixerParams
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyPreamp:int, latestOnly:bool = True) -> List[PreampParam]:
        """ Read preamnp paramters for a given preamp

        :param int keyPreamp: id of preamp
        :param bool latestOnly: If true, only get the most recent set, defaults to True
        :return List[PreampParam]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM PreampParams WHERE fkPreamps = {keyPreamp} ORDER BY FreqLO ASC, TS DESC;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []

        # keep only the newest records for each FreqLO        
        if latestOnly:
            # using a dict to cache FreqLOs seen and their rows:
            keep = {}
            for row in rows:
                FreqLO = row[2]
                if FreqLO not in keep.keys():
                    keep[FreqLO] = row
            # now we have only one row per FreqLO:
            rows = [keep[FreqLO] for FreqLO in keep.keys()]

        return [PreampParam(
            key = row[0],
            fkPreamps = row[1],
            temperature = row[2] if row[2] else 0,
            FreqLO = row[3],
            timeStamp = makeTimeStamp(row[4]),
            VD1 = row[5] if row[5] else 0,
            VD2 = row[6] if row[6] else 0,
            VD3 = row[7] if row[7] else 0,
            ID1 = row[8] if row[8] else 0,
            ID2 = row[9] if row[9] else 0,
            ID3 = row[10] if row[10] else 0
        ) for row in rows]

    def create(self, fkPreamps: int,preampParams:List[PreampParam]) -> bool:
        """ Create new records

        :param List[PreampParam] mixerParams: records to insert
        :return bool: true if successful
        """
        q = f"INSERT INTO PreampParams ({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for row in preampParams:
            row.fkPreamps = fkPreamps
            row.timeStamp = datetime.now()
            if values:
                values += ","
            values += f"({row.getInsertVals()})"
        
        if values == "":
            return False
        
        q += values + ";"
        return self.DB.execute(q, commit = True)
