""" Schema for records of the DBBand6Cart.BP_Center_Pwrs table

For each raster scan, referenced by fkBeamPatterns, there are a collection of records here
giving the amplitude and phase at the center of the co-polar beam.  A new record is added
every five minutes by default.  The final record for a scan will have ScanComplete = 1.
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `BP_Center_Pwrs` (
# 	`keyBP_Center_Pwrs` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkBeamPatterns` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`Amplitude` FLOAT NULL DEFAULT NULL,
# 	`Phase` FLOAT NULL DEFAULT NULL,
# 	`TS` DATETIME NULL DEFAULT NULL,
# 	`ScanComplete` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT '1 Indicates Scan Complete',
# 	PRIMARY KEY (`keyBP_Center_Pwrs`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = ('keyBP_Center_Pwrs',
           'fkBeamPatterns',
           'Amplitude',
           'Phase',
           'TS',
           'ScanComplete')

class BPCenterPower(BaseModel):
    """A record in the DBBand6Cart.BP_Center_Pwrs table
    """
    key: int = 0                    # keyBP_Center_Pwrs is assigned by the database on insert.
    fkBeamPatterns: int
    Amplitude: float
    Phase: float
    timeStamp: datetime = None
    ScanComplete: bool

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},{},'{}',{}".format(
            self.fkBeamPatterns,
            self.Amplitude,
            self.Phase,
            self.timeStamp,
            1 if self.ScanComplete else 0
        )
