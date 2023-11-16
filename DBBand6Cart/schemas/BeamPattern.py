""" Schema for records of the DBBand6Cart.BeamPatterns table

One self is created per raster scan.  
There are up to five scans for each fkCartTest and FreqCarrier/FreqLO combination.
"""
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

    def getDescription(self):
        if self.Scan_Angle == self.Lvl_Angle:
            if self.SourcePosition == 1:
                return "pol0 copol"
            elif self.SourcePosition == 2:
                return "pol1 copol"
            elif self.SourcePosition == 3:
                return "pol0 180"
            elif self.SourcePosition == 3:
                return "pol1 180"
        else:
            if self.SourcePosition == 1:
                return "pol1 xpol"
            elif self.SourcePosition == 2:
                return "pol0 xpol"
            elif self.SourcePosition == 3:
                return "pol0 180"
            elif self.SourcePosition == 3:
                return "pol1 180"

