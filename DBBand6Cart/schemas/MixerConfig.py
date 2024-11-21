"""Schema for records of the DBBand6Cart.MxrPreampAssys table plus helpers for child table keys

Each record in MxrTests references a record in MxrPreampAssys, designating the mixer-preamp configuration for the test.
"""
from pydantic import BaseModel
from datetime import datetime

# MxrTests reference MxrPreampAssys
# So 'configuration' for CartTests comes from MxrPreampAssys.

# CREATE TABLE `MxrPreampAssys` (
# 	`keyMxrPreampAssys` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkPreampPair` INT(20) NULL DEFAULT NULL,
# 	`fkMixerChip0` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`fkMixerChip1` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`SN_Hybrid` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`SN_MagnetCoil` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`TS_Removed` DATETIME NULL DEFAULT NULL,
# 	`SN` SMALLINT(6) NULL DEFAULT NULL,
# 	`Pol` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
# 	`Notes` VARCHAR(255) NULL DEFAULT 'Status Legend: 0=Failed Testing, 1=Awaiting Testing, 2=Passed Testing, 3=Installed in Cartridge, 4=Marginal, 5=Unavailable' COLLATE 'latin1_swedish_ci',
#   Other stuff...
# )

class MixerConfig(BaseModel):
    """A record in the DBBand6Cart.MxrPreampAssys table
    """
    key: int = 0                            # keyMxrPreampAssys is assigned by the database on insert.
    serialNum: str
    timeStamp: datetime

class MixerKeys(BaseModel):
    key: int                                # keyMixerPreampAssys
    keyChip1: int                           # keyMixerChips
    keyChip2: int                           # keyMixerChips
    keyPreamp1: int                         # keyPreamps accessed via PreampPairs
    keyPreamp2: int                         # keyPreamps accessed via PreampPairs
    snMixer: str                            # MxrPreampAssys.SN
    snChip1: str
    snChip2: str
    snPreamp1: str
    snPreamp2: str
    timeStamp: datetime