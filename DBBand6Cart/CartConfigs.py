from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime

# CartTests reference CartAssemblies which reference ColdCarts
# So 'configuration' for CartTests comes from CartAssemblies.

# CREATE TABLE `CartAssemblies` (
#     `keyCartAssys` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
#     `fkColdCarts` INT(10) UNSIGNED NOT NULL DEFAULT '0',
#     `fkWCAs` INT(10) UNSIGNED NOT NULL DEFAULT '0',
#     `fkBiasMods` INT(10) UNSIGNED NOT NULL DEFAULT '0',
#     `fkWarmIFPlates` INT(10) UNSIGNED NOT NULL DEFAULT '0',
#     `TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     `TS_Removed` DATETIME NULL DEFAULT NULL,
#     `SN` INT(20) NULL DEFAULT NULL,
#     `SN_Photomixer` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     `Notes` VARCHAR(255) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
#     `lnk_DB_Delivery` VARCHAR(255) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# )
#
# CREATE TABLE `ColdCarts` (
#     `keyColdCarts` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
#     `fkMxrPreampAssy0` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkMxrPreampAssy1` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor0` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor1` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor2` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor3` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor4` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `fkTempSensor5` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     `SN` VARCHAR(20) NULL DEFAULT NULL COMMENT 'assigned serial number' COLLATE 'latin1_swedish_ci',
#     `ESN0` VARCHAR(16) NULL DEFAULT NULL COMMENT 'electronic serial number Pol0' COLLATE 'latin1_swedish_ci',
#     `ESN1` VARCHAR(16) NULL DEFAULT NULL COMMENT 'ESN Pol1' COLLATE 'latin1_swedish_ci',
#     ... lots of other fks ...
# )

# schema for cartridge configuration:
class CartConfig(BaseModel):
    id: int                                 # keyCartAssys
    serialNum: str                          # ColdCarts.SN 
    ESN0: str                               # ColdCarts.ESN0
    ESN1: str                               # ColdCarts.ESN1
    WCA: str = None                         # WCAs.SN
    biasMod: str = None                     # BiasMods.SN
    timeStamp: datetime = datetime.now()    # CartAssemblies.TS

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
        q = '''SELECT CA0.keyCartAssys, CC.SN, CC.ESN0, CC.ESN1, CA0.TS, 
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
                               serialNum = row[1] if row[1] else '',
                               ESN0 = row[2] if row[2] else '',
                               ESN1 = row[3] if row[3] else '',
                               timeStamp = makeTimeStamp(row[4]),
                               WCA = row[5] if row[5] else '',
                               biasMod = row[6] if row[6] else '')
                               for row in rows]
