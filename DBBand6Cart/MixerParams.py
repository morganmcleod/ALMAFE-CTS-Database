from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.MixerParam import MixerParam, COLUMNS
from typing import List

class MixerParams():
    '''
    Create, Read, Update, Delete dbBand6Cart records related to MixerParam
    '''
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyMixerChips:int, latestOnly:bool = True) -> List[MixerParam]:
        q = f"SELECT {','.join(COLUMNS)} FROM MixerParams WHERE fkMixerChips = {keyMixerChips} ORDER BY FreqLO ASC, TS DESC;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        if latestOnly:
            keep = {}
            for row in rows:
                FreqLO = row[2]
                if FreqLO not in keep.keys():
                    keep[FreqLO] = row
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

    def create(self, mixerParams:List[MixerParam]) -> int:
        q = f"INSERT INTO MixerParams ({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for row in mixerParams:
            value = ",".join([
                row.fkMixerChips,
                row.FreqLO,
                row.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT),
                row.VJ,
                row.IJ,
                row.IMAG
            ])
            if values != "":
                values += ","
            values += "(" + value + ")"
        if values == "":
            return 0
        q += values + ";"
        self.DB.execute(q, commit = True)
        
        # get the last value for keyMixerParams:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return 0
        else:
            return row[0]


