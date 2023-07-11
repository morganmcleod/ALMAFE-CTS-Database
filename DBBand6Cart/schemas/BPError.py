''' Schema for records of the DBBand6Cart.BP_Errors table

During each raster scan, referenced by fkBeamPatterns, zero or more errors may be logged here.
'''
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from socket import getfqdn

# CREATE TABLE `BP_Errors` (
#     `keyBP_Errors` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
#     `fkBeamPattern` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `Level` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     `Message` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
#     `TS_First` DATETIME NULL DEFAULT NULL,
#     `System` VARCHAR(30) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
#     `Model` VARCHAR(30) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
#     `Source` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
#     `Occurrences` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `Cleared` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     `Message_Key` INT(10) UNSIGNED NULL DEFAULT NULL,
#     `TS_Last` DATETIME NULL DEFAULT NULL,
#     `TS_Cleared` DATETIME NULL DEFAULT NULL,
#     `Removed` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     `TS` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
#     `FreqSrc` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
#     `FreqRcvr` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
#     `Meas_State` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     PRIMARY KEY (`keyBP_Errors`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyBP_Errors',
    'fkBeamPattern',
    'Level',
    'Message',
    'TS_First',
    'System',
    'Model',
    'Source',
    'TS',
    'FreqSrc',
    'FreqRcvr',
)

class BPErrorLevel(Enum):
    ''' Constants for the Level field
    '''
    INFO     = 0
    WARNING  = 1
    ERROR    = 2
    CRITICAL = 3

class BPError(BaseModel):
    '''A record in the DBBand6Cart.BP_Errors table
    '''
    key: int = 0                     # keyBP_Errors is assigned by the database on insert.
    fkBeamPattern: int
    Level: BPErrorLevel
    Message: str
    TS_First: datetime = datetime.now()
    System: str = getfqdn()
    Model: str
    Source: str
    TS: datetime = datetime.now()
    FreqSrc: float = 0
    FreqRcvr: float = 0