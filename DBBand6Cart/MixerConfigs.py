""" Read records from the DBBand6Cart.MxrPreampAssys table plus helpers for child table keys

Each record in MxrTests references a record in MxrPreampAssys, designating the mixer-preamp configuration for the test.
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from typing import List, Optional
from .schemas.MixerConfig import MixerConfig, MixerKeys

class MixerConfigs(object):
    """ Read mixer Configurations in dbBand6Cart
    
    The notion of Configuration is represented in the database by keyMxrPreampAssys of the MxrPreampAssys table
    """
    #TODO: implement MixerConfigs.create, MixerConfigs.update, MixerConfigs.delete when needed

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
    
    def read(self, keyMxrPreampAssys:int = None, serialNum:str = None, latestOnly:bool = True) -> Optional[List[MixerConfig]]:
        """ Read one or more configuration records

        :param keyMxrPreampAssys: int selector to read a single config
        :param serialNum: to match in MxrPreampAssys table
        :param latestOnly: if True find only the latest configuration for serialNum
        :return list of MixerConfig or None if not found
        """
        q = "SELECT MP0.keyMxrPreampAssys, MP0.SN, MP0.TS FROM MxrPreampAssys as MP0"
        
        where = ""
        
        # if we want a specific record:
        if keyMxrPreampAssys:
            if where:
                where += " AND "
            where += f"MP0.keyMxrPreampAssys = {keyMxrPreampAssys}"
        
        # if there might be a collection of records and we want the newest:
        elif latestOnly:
            q += " LEFT JOIN MxrPreampAssys AS MP1 ON MP0.SN = MP1.SN AND MP1.keyMxrPreampAssys > MP0.keyMxrPreampAssys"
            if where:
                where += " AND "
            where += "MP1.keyMxrPreampAssys IS NULL"

        # for a specific serial number:
        if serialNum:
            if where:
                where += " AND "
            where += "MP0.SN = '{:03d}'".format(int(serialNum))
        if where:
            q += " WHERE " + where
        q += " ORDER BY SN DESC, MP0.keyMxrPreampAssys DESC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        return [MixerConfig(id = row[0],
                            serialNum = str(row[1]),
                            timeStamp = makeTimeStamp(row[2]))
                for row in rows if row[1]]

    def readKeys(self, keyMxrPreampAssys:int):
        """Read the database keys all the CCA components of the given keyCartAssys and pol

        :param int keyMxrPreampAssys: _description_
        :param int pol: _description_
        """
        q = f"""SELECT 
            MP.keyMxrPreampAssys AS keyMixer,
            MP.SN as snMixer,
            MP.fkMixerChip0, MP.fkMixerChip1,
            PP.fkPreamp0, PP.fkPreamp1,
            M0.SN as snChip1, M1.SN as snChip2,
            P0.SN as snPreamp1, P1.SN as snPreamp2,
            MP.TS AS TSMixer
            FROM MxrPreampAssys AS MP
            LEFT JOIN PreampPairs AS PP ON MP.fkPreampPair = PP.keyPreampPairs
            JOIN MixerChips as M0 ON MP.fkMixerChip0 = M0.keyMixerChips
            LEFT JOIN MixerChips as M1 ON MP.fkMixerChip1 = M1.keyMixerChips
            LEFT JOIN Preamps AS P0 ON PP.fkPreamp0 = P0.keyPreamps
            LEFT JOIN Preamps AS P1 ON PP.fkPreamp1 = P1.keyPreamps
            WHERE MP.keyMxrPreampAssys = {keyMxrPreampAssys}"""
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        
        return MixerKeys(
            id = row[0],
            snMixer = str(row[1]) if row[1] else '0',
            keyChip1 = row[2] if row[2] else 0,
            keyChip2 = row[3] if row[3] else 0,
            keyPreamp1 = row[4] if row[4] else 0,
            keyPreamp2 = row[5] if row[5] else 0,
            snChip1 = row[6] if row[6] else '',
            snChip2 = row[7] if row[7] else '',
            snPreamp1 = row[8] if row[8] else '',
            snPreamp2 = row[9] if row[9] else '',
            timeStamp = makeTimeStamp(row[10])
        )
