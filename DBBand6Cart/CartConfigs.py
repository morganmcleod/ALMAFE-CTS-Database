""" Create and read records in the DBBand6Cart.ColdCarts table and its child tables
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from typing import List, Optional
from .schemas.CartConfig import CartConfig, CartKeys

class CartConfigs(object):
    """ Read cartridge Configurations in dbBand6Cart
    
    The notion of Configuration is represented in the database by keyColdCarts of the ColdCarts table
    """
    #TODO: implement CartConfigs.create, CartConfigs.update, CartConfigs.delete when needed

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
    
    def read(self, keyColdCart:int = None, serialNum:str = None, latestOnly:bool = True) -> List[CartConfig]:
        """ Read one or more configuration records
        
        :param keyColdCarts: int selector to read a single config
        :param serialNum: to match in ColdCarts table
        :param latestOnly: if True find only the latest configuration for serialNum
        :return list of CartConfig or None if not found
        """
        q = "SELECT CC0.keyColdCarts, CC0.SN, CC0.ESN0, CC0.ESN1, CC0.TS FROM ColdCarts as CC0"
        
        where = ""
        
        # if we want a specific record:
        if keyColdCart:
            if where:
                where += " AND "
            where += f"CC0.keyColdCarts = {keyColdCart}"
        
        # if there might be a collection of records and we want the newest:
        elif latestOnly:
            q += " LEFT JOIN ColdCarts AS CC1 ON CC0.SN = CC1.SN AND CC1.keyColdCarts > CC0.keyColdCarts"
            if where:
                where += " AND "
            where += "CC1.keyColdCarts IS NULL"

        # for a specific serial number:
        if serialNum:
            where += " AND CC.SN = '{:03d}'".format(int(serialNum))
        if where:
            q += " WHERE " + where
        q += " ORDER BY CC0.SN, CC0.keyColdCarts DESC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        return [CartConfig(
            id = row[0],
            serialNum = row[1] if row[1] else '',
            ESN0 = row[2] if row[2] else '',
            ESN1 = row[3] if row[3] else '',
            timeStamp = makeTimeStamp(row[4])
        ) for row in rows]

    def readKeys(self, keyColdCarts:int, pol:int) -> Optional[CartKeys]:
        """Read the database keys and serial numbers for the CCA components for a config Id and pol

        :param int keyColdCarts: configuration Id
        :param int pol: pol 0 or 1
        :return list of CartKeys or None of not found
        """
        q = f"""SELECT 
            CC.keyColdCarts, MP.keyMxrPreampAssys AS keyMixer, MP.SN AS snMixer,
            MP.fkMixerChip0, MP.fkMixerChip1,
            PP.fkPreamp0, PP.fkPreamp1,
            M0.SN as snChip1, M1.SN as snChip2,
            P0.SN as snPreamp1, P1.SN as snPreamp2,
            CC.TS, MP.TS AS TSMixer
            FROM ColdCarts AS CC
            JOIN MxrPreampAssys AS MP ON CC.fkMxrPreampAssy{pol} = MP.keyMxrPreampAssys
            JOIN PreampPairs AS PP ON MP.fkPreampPair = PP.keyPreampPairs
            JOIN MixerChips as M0 ON MP.fkMixerChip0 = M0.keyMixerChips
            JOIN MixerChips as M1 ON MP.fkMixerChip1 = M1.keyMixerChips
            JOIN Preamps AS P0 ON PP.fkPreamp0 = P0.keyPreamps
            JOIN Preamps AS P1 ON PP.fkPreamp1 = P1.keyPreamps
            WHERE CC.keyColdCarts = {keyColdCarts};"""
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        return CartKeys(
            id = row[0],
            keyMixer = row[1],
            snMixer = row[2],
            keyChip1 = row[3],
            keyChip2 = row[4],
            keyPreamp1 = row[5],
            keyPreamp2 = row[6],
            snChip1 = row[7] if row[7] else '',
            snChip2 = row[8] if row[8] else '',
            snPreamp1 = row[9] if row[9] else '',
            snPreamp2 = row[10] if row[10] else '',
            timeStamp = makeTimeStamp(row[11]),
            timeStampMixer = makeTimeStamp(row[12])
        )
