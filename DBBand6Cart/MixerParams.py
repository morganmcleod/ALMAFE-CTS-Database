""" Create, Read, Update, Delete records in table DBBand6Cart.MixerParams
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.MixerParam import MixerParam, COLUMNS
from typing import List
from datetime import datetime

class MixerParams():
    """ Create, Read, Update, Delete records in table DBBand6Cart.MixerParams
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyMixerChips:int, latestOnly:bool = True) -> List[MixerParam]:
        """ Read mixer paramters for a given mixer chip

        :param int keyMixerChips: id of mixer chip
        :param bool latestOnly: If true, only get the most recent set, defaults to True
        :return List[MixerParam]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM MixerParams WHERE fkMixerChips = {keyMixerChips} ORDER BY FreqLO ASC, TS DESC;"
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

        return [MixerParam(
            key = row[0],
            fkMixerChips = row[1],
            FreqLO = row[2],
            timeStamp = makeTimeStamp(row[3]),
            VJ = row[4],
            IJ = row[5],
            IMAG = row[6]
        ) for row in rows]

    def create(self, keyChip:int, mixerParams:List[MixerParam]) -> bool:
        """ Create new records

        :param List[MixerParam] mixerParams: records to insert
        :return bool: true if successful
        """
        q = f"INSERT INTO MixerParams ({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for row in mixerParams:
            row.fkMixerChips = keyChip
            row.timeStamp = datetime.now()
            if values:
                values += ","
            values += f"({row.getInsertVals()})"

        if values == "":
            return False

        q += values + ";"
        return self.DB.execute(q, commit = True)
