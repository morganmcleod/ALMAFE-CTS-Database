""" Schema for records of the DBBand6Cart.ColdCarts table plus helpers for child table keys

Each record in CartTests references a record in ColdCarts, designating the cartridge configuration for the test.
"""
from pydantic import BaseModel
from datetime import datetime

# Historically all test data in the CartTests table referenced CartAssemblies, 
# so that the WCA, Bias Module, Warm IF plate, etc. could be associated with the test data.
#
# However, since the start of ALMA operations and maintenance the cold cartridge, represented
# by the ColdCarts table, is the unit under test.  And the CartAssemblies table was not being updated.
# 
# Since mid-2023 the CTS software now associates CartTests with ColdCarts instead of CartAssemblies.

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

class CartConfig(BaseModel):
    """A record in the DBBand6Cart.ColdCarts table
    """
    id: int = 0                             # keyColdCarts is assigned by the database on insert.
    serialNum: str
    ESN0: str
    ESN1: str
    timeStamp: datetime

class CartKeys(BaseModel):
    """This data model collects the child record keys, serial numbers, and useful metadata
    """
    id: int                                 # keyColdCarts
    keyMixer: int                           # keyMixerPreampAssys
    keyChip1: int                           # keyMixerChips
    keyChip2: int                           # keyMixerChips
    keyPreamp1: int                         # keyPreamps accessed via PreampPairs
    keyPreamp2: int                         # keyPreamps accessed via PreampPairs
    snMixer: int                            # MxrPreampAssys.SN
    snChip1: str
    snChip2: str
    snPreamp1: str
    snPreamp2: str
    timeStamp: datetime
    timeStampMixer: datetime
