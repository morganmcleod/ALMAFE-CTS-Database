""" Schema for records of the DBBand6Cart.Preamps table

Each record in PreampPairs references one or two records in Preamps.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# CREATE TABLE `Preamps` (
# 	`keyPreamps` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`TS` TIMESTAMP NULL DEFAULT NULL,
# 	`TS_Removed` DATETIME NULL DEFAULT NULL COMMENT 'timestamp removed',
# 	`SN` VARCHAR(20) NULL DEFAULT NULL COMMENT 'assigned serial number' COLLATE 'latin1_swedish_ci',
# 	`ILED` FLOAT(4,1) NULL DEFAULT NULL,
# 	`Notes` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`DataHyperlink` VARCHAR(255) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`WarmData_By` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`TS_WarmData` TIMESTAMP NULL DEFAULT NULL,
# 	`lnk_WSP` VARCHAR(4095) NULL DEFAULT NULL COMMENT 'Link to warm test data' COLLATE 'latin1_swedish_ci',
# 	`ColdData_By` VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`TS_ColdData` TIMESTAMP NULL DEFAULT NULL,
#   ... other stuff ...
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyPreamps', 
    'TS', 
    'SN', 
    'Notes', 
    'ColdData_By', 
    'TS_ColdData'
)

class Preamp(BaseModel):
    """A record in the DBBand6Cart.Preamps table
    """
    key: int = 0                    # keyPreamps is assigned by the database on insert.
    timeStamp: datetime = None
    serialNum: Optional[str] = None
    notes: Optional[str] = None
    coldDataBy: Optional[str] = None
    coldDataTS: Optional[datetime] = None

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "'{}','{}',{},{},{}".format(
            self.timeStamp,
            self.serialNum,
            f"'{self.notes}'" if self.notes else "NULL",
            f"'{self.coldDataBy}'" if self.coldDataBy else "NULL",
            f"'{self.coldDataTS}'" if self.coldDataTS else "NULL"
        )
