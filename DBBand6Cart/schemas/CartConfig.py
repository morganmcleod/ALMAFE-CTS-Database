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

# CREATE TABLE 'MxrPreampAssys' (
# 	'keyMxrPreampAssys' INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	'fkPreampPair' INT(20) NULL DEFAULT NULL,
# 	'fkMixerChip0' INT(10) UNSIGNED NULL DEFAULT NULL,
# 	'fkMixerChip1' INT(10) UNSIGNED NULL DEFAULT NULL,
# 	'SN_Hybrid' VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'SN_MagnetCoil' VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'TS' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	'TS_Removed' DATETIME NULL DEFAULT NULL,
# 	'SN' SMALLINT(6) NULL DEFAULT NULL,
# 	'Pol' TINYINT(3) UNSIGNED NULL DEFAULT NULL,
# 	'Notes' VARCHAR(255) NULL DEFAULT 'Status Legend: 0=Failed Testing, 1=Awaiting Testing, 2=Passed Testing, 3=Installed in Cartridge, 4=Marginal, 5=Unavailable' COLLATE 'latin1_swedish_ci',
#   ... other stuff ...
# )

# CREATE TABLE 'MixerChips' (
# 	'keyMixerChips' INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	'fkType' TINYINT(3) UNSIGNED NULL DEFAULT '1' COMMENT '1 = Band6v1, 2 = Band6v2',
# 	'fkInspections' INT(10) UNSIGNED NULL DEFAULT NULL,
# 	'TS' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	'Band' TINYINT(4) NOT NULL DEFAULT '6',
# 	'TS_Removed' DATETIME NULL DEFAULT NULL COMMENT 'Date chip was removed from assy',
# 	'SN' VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'SNa' VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'Orig_Res' INT(10) NULL DEFAULT NULL,
# 	'Final_Res' INT(10) NULL DEFAULT NULL,
# 	'Side' CHAR(2) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'Notes' TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'lnk_Data' VARCHAR(255) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY ('keyMixerChips') USING BTREE
# )

# CREATE TABLE `PreampPairs` (
# 	`keyPreampPairs` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkPreamp0` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`fkPreamp1` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`TS_Removed` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`Notes` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`6to10IR` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`4to6and10to12IR` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`lnk_Data` VARCHAR(250) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY (`keyPreampPairs`) USING BTREE
# )

# schema for cartridge configuration:
class CartConfig(BaseModel):
    id: int                                 # keyCartAssys
    coldCartId: int                         # keyColdCarts
    serialNum: str                          # ColdCarts.SN 
    ESN0: str                               # ColdCarts.ESN0
    ESN1: str                               # ColdCarts.ESN1
    WCA: str = None                         # WCAs.SN
    biasMod: str = None                     # BiasMods.SN
    timeStamp: datetime = datetime.now()    # CartAssemblies.TS

class CartKeys(BaseModel):
    id: int                                 # keyCartAssys
    keyMixer: int                           # keyMixerPreampAssys
    keyChip1: int                           # keyMixerChips
    keyChip2: int                           # keyMixerChips
    keyPreamp1: int                         # keyPreamps
    keyPreamp2: int                         # keyPreamps
    snMixer: str                            # SN of mixerPreampAssy
    snChip1: str
    snChip2: str
    snPreamp1: str
    snPreamp2: str
    timeStamp: datetime
    timeStampMixer: datetime
