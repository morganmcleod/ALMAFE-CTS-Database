"""Schema for records of the DBBand6Cart.WCAs table
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `WCAs` (
# 	`keyWCAs` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
# 	`TS_Removed` DATETIME NULL DEFAULT NULL COMMENT 'timestamp removed',
# 	`DT_Tested` DATE NULL DEFAULT NULL,
# 	`DT_Installed` DATE NULL DEFAULT NULL,
# 	`SN` VARCHAR(20) NULL DEFAULT NULL COMMENT 'assigned serial number' COLLATE 'latin1_swedish_ci',
# 	`ESN` VARCHAR(16) NULL DEFAULT NULL COMMENT 'electronic serial number, hexadecimal' COLLATE 'latin1_swedish_ci',
# 	`SN_PwrAmp` VARCHAR(20) NULL DEFAULT NULL COMMENT 'power amp module serial number' COLLATE 'latin1_swedish_ci',
# 	`FloYIG` DOUBLE NULL DEFAULT NULL,
# 	`FhiYIG` DOUBLE NULL DEFAULT NULL,
# 	`Notes` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`lnk_Data` VARCHAR(100) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY (`keyWCAs`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyWCAs', 
    'TS', 
    'SN', 
    'FloYIG',
    'FhiYIG'
)

class WCA(BaseModel):
    """A record in the DBBand6Cart.WCAs table
    """
    key: int                        # keyWCAs is assigned by the database on insert.
    timeStamp: datetime
    serialNum: str
    ytoLowGHz: float
    ytoHighGHz: float
