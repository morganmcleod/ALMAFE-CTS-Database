""" Create, Read, Update, Delete records in table DBBand6Cart.MixerParams
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.MixerParam import MixerParam, COLUMNS
from typing import List
from datetime import datetime
from bisect import bisect_left


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

        :param int keyMixerChips: key of mixer chip
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
                FreqLO = row[3]
                if FreqLO not in keep.keys():
                    keep[FreqLO] = row
            # now we have only one row per FreqLO:
            rows = [keep[FreqLO] for FreqLO in keep.keys()]

        return [MixerParam(
            key = row[0],
            fkMixerChips = row[1],
            Temperature = row[2],
            FreqLO = row[3],
            timeStamp = makeTimeStamp(row[4]),
            VJ = row[5],
            IJ = row[6],
            IMAG = row[7]
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

    def interpolate(self, FreqLO:float, mixerParams:List[MixerParam]) -> MixerParam:
        # workaround for Python 3.9
        # 3.10 allows us to pass a key function to bisect_left
        FreqLOs = [x.FreqLO for x in mixerParams]
        
        pos = bisect_left(FreqLOs, FreqLO)
        if pos == 0:
            return mixerParams[0]
        if pos == len(mixerParams):
            return mixerParams[-1]
        if mixerParams[pos].FreqLO == FreqLO:
            return mixerParams[pos]
        before = mixerParams[pos - 1]
        after = mixerParams[pos]
        scale = (FreqLO - before.FreqLO) / (after.FreqLO - before.FreqLO)
        return MixerParam(
            FreqLO = FreqLO,
            VJ = before.VJ + ((after.VJ - before.VJ) * scale),
            IJ = before.IJ + ((after.IJ - before.IJ) * scale),
            IMAG = before.IMAG + ((after.IMAG - before.IMAG) * scale)
        )