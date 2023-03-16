from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from .schemas.CartConfig import CartConfig, CartKeys

class CartConfigs(object):
    '''
    Read cartridge Configurations in dbBand6Cart
    The notion of Configuration is represented in the database by keyCartAssys of the CartAssemblies table
    The serial number and ESN comes from the ColdCarts table.
    '''
    #TODO: implement CartConfigs.create, CartConfigs.update, CartConfigs.delete when needed

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
    
    def read(self, keyCartAssys:int = None, serialNum:str = None, latestOnly:bool = True):
        '''
        Read one or more configuration records
        :param keyCartAssys: int selector to read a single config
        :param serialNum: to match in ColdCarts table
        :param latestOnly: if True find only the latest configuration for serialNum
        :return list of CartConfig or None if not found
        '''
        q = '''SELECT CA0.keyCartAssys, CC.keyColdCarts, CC.SN, CC.ESN0, CC.ESN1, CA0.TS, 
               WCAs.SN AS WCASN, BiasMods.SN AS BiasModSN
               FROM ColdCarts as CC, CartAssemblies AS CA0'''
        
        where = " WHERE CA0.fkColdCarts = CC.keyColdCarts"
        
        # if we want a specific record:
        if keyCartAssys:
            where += " AND CA0.keyCartAssys = {}".format(keyCartAssys)
        
        # if there might be a collection of records and we want the newest:
        elif latestOnly:
            q += " LEFT JOIN CartAssemblies AS CA1 ON CA0.SN = CA1.SN AND CA1.keyCartAssys > CA0.keyCartAssys"
            where += " AND CA1.keyCartAssys IS NULL"

        q += ''' LEFT JOIN WCAs ON CA0.fkWCAs = WCAs.keyWCAs
                 LEFT JOIN BiasMods ON CA0.fkBiasMods = BiasMods.keyBiasMods'''

        # for a specific serial number:
        if serialNum:
            where += " AND CC.SN = '{:03d}'".format(int(serialNum))
        q += where
        q += " ORDER BY CC.SN, CA0.keyCartAssys DESC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [CartConfig(id = row[0],
                               coldCartId = row[1],
                               serialNum = row[2] if row[2] else '',
                               ESN0 = row[3] if row[3] else '',
                               ESN1 = row[4] if row[4] else '',
                               timeStamp = makeTimeStamp(row[5]),
                               WCA = row[6] if row[6] else '',
                               biasMod = row[7] if row[7] else '')
                               for row in rows]

    def readKeys(self, keyCartAssys:int, pol:int):
        """Read the database keys all the CCA components of the given keyCartAssys and pol

        :param int keyCartAssys: _description_
        :param int pol: _description_
        """
        q = f"""SELECT 
            CA.keyCartAssys, MP.keyMxrPreampAssys AS keyMixer,
            MP.fkMixerChip0, MP.fkMixerChip1,
            PP.fkPreamp0, PP.fkPreamp1,
            MP.SN as snMixer,
            M0.SN as snChip1, M1.SN as snChip2,
            P0.SN as snPreamp1, P1.SN as snPreamp2,
            CA.TS, MP.TS AS TSMixer
            FROM CartAssemblies AS CA JOIN ColdCarts AS CC ON CA.fkColdCarts = CC.keyColdCarts
            JOIN MxrPreampAssys AS MP ON CC.fkMxrPreampAssy{pol} = MP.keyMxrPreampAssys
            JOIN PreampPairs AS PP ON MP.fkPreampPair = PP.keyPreampPairs
            JOIN MixerChips as M0 ON MP.fkMixerChip0 = M0.keyMixerChips
            JOIN MixerChips as M1 ON MP.fkMixerChip1 = M1.keyMixerChips
            JOIN Preamps AS P0 ON PP.fkPreamp0 = P0.keyPreamps
            JOIN Preamps AS P1 ON PP.fkPreamp1 = P1.keyPreamps
            WHERE CA.keyCartAssys = {keyCartAssys}"""
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        return CartKeys(
            id = row[0],
            keyMixer = row[1],
            keyChip1 = row[2],
            keyChip2 = row[3],
            keyPreamp1 = row[4],
            keyPreamp2 = row[5],
            snMixer = row[6] if row[6] else '',
            snChip1 = row[7] if row[7] else '',
            snChip2 = row[8] if row[8] else '',
            snPreamp1 = row[9] if row[9] else '',
            snPreamp2 = row[10] if row[10] else '',
            timeStamp = makeTimeStamp(row[11]),
            timeStampMixer = makeTimeStamp(row[12])
        )