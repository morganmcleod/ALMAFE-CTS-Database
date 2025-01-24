""" Schema for records of the DBBand6Cart.BeamPatterns table

One self is created per raster scan.  
There are up to five scans for each fkCartTest and FreqCarrier/FreqLO combination.
"""
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `BeamPatterns` (
# 	`keyBeamPattern` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartTest` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`FreqLO` FLOAT NULL DEFAULT NULL,
# 	`FreqCarrier` FLOAT NULL DEFAULT NULL,
# 	`Co_OR_XPol` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
# 	`Beam_Center_X` FLOAT NULL DEFAULT NULL,
# 	`Beam_Center_Y` FLOAT NULL DEFAULT NULL,
# 	`Center_Pwr_Before` FLOAT NULL DEFAULT NULL,
# 	`Center_Pwr_After` FLOAT NULL DEFAULT NULL,
# 	`Scan_Angle` FLOAT NULL DEFAULT NULL,
# 	`Scan_Port` INT(10) NULL DEFAULT NULL,
# 	`Lvl_Angle` FLOAT NULL DEFAULT NULL,
# 	`Lvl_Port` INT(10) NULL DEFAULT NULL,
# 	`AutoLevel` FLOAT NULL DEFAULT NULL COMMENT 'Commanded autolevel',
# 	`Resolution` FLOAT UNSIGNED NULL DEFAULT NULL COMMENT 'millimeters between points',
# 	`SourcePosition` TINYINT(3) UNSIGNED NULL DEFAULT '0' COMMENT '1=pol 0 copol, 2= pol 1 copol, 3 = pol0+180, 4=pol1+180',
# 	`isStopProcessing` TINYINT(4) NULL DEFAULT NULL COMMENT 'If 1, don\'t process pattern',
# 	`TimeStamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
# 	PRIMARY KEY (`keyBeamPattern`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyBeamPattern',
 	'fkCartTest',
	'FreqLO',
	'FreqCarrier',
	'Beam_Center_X',
	'Beam_Center_Y',
	'Scan_Angle',
	'Scan_Port',
	'Lvl_Angle',
    'AutoLevel',        # 'Commanded autolevel'
	'Resolution',       # 'millimeters between points'
	'SourcePosition',   # '1=pol 0 copol, 2= pol 1 copol, 3 = pol0+180, 4=pol1+180'
	'TimeStamp' 
)

class BP_Class(Enum):
    POL0_COPOL = "pol0 copol"
    POL1_COPOL = "pol1 copol"
    POL0_XPOL = "pol0 xpol"
    POL1_XPOL = "pol1 xpol"
    POL0_180 = "pol0 180"
    POL1_180 = "pol1 180"

class BeamPattern(BaseModel):
    """A self in the DBBand6Cart.BeamPatterns table
    """
    key: int = 0                # keyBeamPattern is assigned by the database on insert.
    fkCartTest: int
    FreqLO: float
    FreqCarrier: float
    Beam_Center_X: float
    Beam_Center_Y: float
    Scan_Angle: float
    Scan_Port: int
    Lvl_Angle: float
    AutoLevel: float
    Resolution: float
    SourcePosition: int
    timeStamp: datetime = None

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},{},{},{},{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.FreqLO,
            self.FreqCarrier,
            self.Beam_Center_X,
            self.Beam_Center_Y,
            self.Scan_Angle,
            self.Scan_Port,
            self.Lvl_Angle,
            self.AutoLevel,
            self.Resolution,
            self.SourcePosition
        )

    def clasify(self) -> BP_Class:
        if self.Scan_Angle == self.Lvl_Angle:
            if self.SourcePosition == 3:
                if self.Scan_Port in (1, 2):
                    return BP_Class.POL0_180
                elif self.Scan_Port in (3, 4):
                    return BP_Class.POL1_180
            else:
                if self.Scan_Port in (1, 2):
                    return BP_Class.POL0_COPOL
                elif self.Scan_Port in (3, 4):
                    return BP_Class.POL1_COPOL
        else:
            if self.Scan_Port in (1, 2):
                return BP_Class.POL0_XPOL
            elif self.Scan_Port in (3, 4):
                return BP_Class.POL1_XPOL

    def getDescription(self):
        return self.clasify().value
