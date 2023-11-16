"""Schema for records of the DBBand6Cart.SelectTests table

One or more SelectTests records are associated with a "virtual" CartTests or MxrTests record.
These contain references to keys and frequencies of data stored in other CartTests or MxrTests.
"""
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

# CREATE TABLE `SelectTests` (
# 	`keySelectTests` INT(11) NOT NULL AUTO_INCREMENT,
# 	`fkParentTest` INT(11) NOT NULL COMMENT 'CartTest or MxrTest which owns this selection',
#	`fkDUT_Type` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'Band6_Cartridge = 0, Band6_MxrPreampAssys = 1',
# 	`fkChildTest` INT(11) NOT NULL COMMENT 'CartTests or MxrTests which are referenced by this selection',
# 	`fkSubHeader` INT(11) NULL DEFAULT NULL COMMENT 'Test steps which are referenced by this selecion e.g. keyBeamPatterns'
# 	`frequency` DOUBLE NULL DEFAULT NULL COMMENT 'frequencies from the referenced fkChildTest',
# 	`Timestamp` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	PRIMARY KEY (`keySelectTests`) USING BTREE,
# 	INDEX `Index 2` (`fkParentTest`) USING BTREE
# )

COLUMNS = (
    'keySelectTests',
    'fkParentTest',
    'fkDUT_Type',
    'fkChildTest',
    'fkSubHeader',
    'frequency',
    'Timestamp'
)

class SelectTestsRecord(BaseModel):
    """ A record in the DBBand6Cart.CartTestsSelection table
    """
    key: int = None                     # keySelectTests assigned by the database on insert.
    fkParentTest: int                   # CartTest or MxrTest which owns this selection
    fkDutType: int                      # value from DUT_Type enum
    fkChildTest: int                    # CartTests or MxrTests which are referenced by this selection
    fkSubHeader: Optional[int] = None   # Test steps which are referenced by this selecion e.g. keyBeamPatterns
    frequency: Optional[float] = None   # frequencies from the referenced fkChildTest
    timeStamp: datetime = None
    text: str = ''

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()   
        return "{},{},{},{},{},'{}'".format(
            self.fkParentTest, 
            self.fkDutType, 
            self.fkChildTest,
            "'" + self.fkSubHeader + "'" if self.fkSubHeader else "NULL",
            self.frequency if self.frequency else "NULL",
            self.timeStamp
        )

        def __eq__(self, other):
            if this.fkParentTest != other.fkParentTest:
                return False
            if this.fkDutType != other.fkDutType:
                return False
            if this.fkChildTest != other.fkChildTest:
                return False
            if this.fkSubHeader is not null and this.fkSubHeader != other.fkSubHeader:
                return False
            if this.frequency != other.frequency:
                return False
            return True
 
