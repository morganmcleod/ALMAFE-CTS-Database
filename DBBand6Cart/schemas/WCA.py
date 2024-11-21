"""Schema for records of the DBBand6Cart.WCAs table
"""
from pydantic import BaseModel
from typing import Optional
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


# CREATE TABLE `LOParams` (
# 	`keyLOParams` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkWCAs` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`FreqLO` DECIMAL(10,6) NOT NULL DEFAULT '0.000000' COMMENT 'LO frequency GHz',
# 	`TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
# 	`VDP0` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp drain bias V',
# 	`VDP1` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp drain bias V',
# 	`VGP0` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp gate bias V',
# 	`VGP1` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp gate bias V',
# 	`AttenP0` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp attenuation dB',
# 	`AttenP1` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'power amp attenuation dB',
# 	`VDAMC` FLOAT(4,2) NULL DEFAULT NULL COMMENT 'AMC control drain for prototype carts V',
# 	PRIMARY KEY (`keyLOParams`) USING BTREE,
# 	INDEX `WCA` (`fkWCAs`) USING BTREE
# )



# The subset of columns to read/write:
COLUMNS = (
    'keyWCAs', 
    'TS', 
    'SN', 
    'FloYIG',
    'FhiYIG',
    'VGP0',
    'VGP1'
)

class WCA(BaseModel):
    """A record in the DBBand6Cart.WCAs table
    """
    key: int = 0                       # keyWCAs is assigned by the database on insert.
    timeStamp: Optional[datetime] = None
    serialNum: str = ""
    ytoLowGHz: float = 0
    ytoHighGHz: float = 0
    VGp0: float = 0
    VGp1: float = 0
