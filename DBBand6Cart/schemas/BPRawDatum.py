""" Schema for records of the DBBand6Cart.BP_Data table

During each raster scan, referenced by fkBeamPatterns, raw near-field data is inserted here.
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `BP_Data` (
#     `keyBP_Data` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
#     `fkBeamPattern` INT(10) UNSIGNED NULL DEFAULT '0',
#     `fkBP_Calc_Data` INT(10) UNSIGNED NULL DEFAULT '0',
#     `Pol` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
#     `Position_X` FLOAT NULL DEFAULT NULL,
#     `Position_Y` FLOAT NULL DEFAULT NULL,
#     `SourceAngle` FLOAT NULL DEFAULT NULL,
#     `Power` FLOAT NULL DEFAULT NULL,
#     `Phase` FLOAT NULL DEFAULT NULL,
#     `TimeStamp` DATETIME NULL DEFAULT NULL,
#     PRIMARY KEY (`keyBP_Data`) USING BTREE,
#     INDEX `fkBP_index` (`fkBeamPattern`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyBP_Data',
    'fkBeamPattern',
    'Pol',
    'Position_X',
    'Position_Y',
    'SourceAngle',
    'Power',
    'Phase',
    'TimeStamp'
)

class BPRawDatum(BaseModel):
    """A record in the DBBand6Cart.BP_Data table
    """
    key: int = 0                # keyBP_Data is assigned by the database on insert.
    fkBeamPattern: int
    Pol: int
    Position_X: float
    Position_Y: float
    SourceAngle: float
    Power: float
    Phase: float
    TimeStamp: datetime = datetime.now()
    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        return "{},{},{},{},{},{},{},'{}'".format(
                self.fkBeamPattern,
                self.Pol,
                self.Position_X,
                self.Position_Y,
                self.SourceAngle,
                self.Power,
                self.Phase,
                self.TimeStamp
        )
