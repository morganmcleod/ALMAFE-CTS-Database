"""Schema for records of the DBBand6Cart.CombineTests table

One or more CombineTests records are associated with a "virtual" CartTests or MxrTests record.
These contain references to keys, frequencies, and subheaders of data stored in other CartTests or MxrTests and their subheader tables.
"""
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

# CREATE TABLE `CombineTests` (
# 	`keyCombineTests` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
# 	`fkParentTest` INT(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'CartTest or MxrTest which owns this combination',
# 	`fkDUT_Type` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'Band6_Cartridge = 0, Band6_MxrPreampAssys = 1',
# 	`Timestamp` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`fkPath0_TestId` INT(11) NOT NULL COMMENT 'The first part of the path to the referenced test.  An fk to CartTests or MixerTests.',
# 	`fkPath1` TINYTEXT NULL DEFAULT NULL COMMENT 'The second part of the path' COLLATE 'latin1_swedish_ci',
# 	`fkPath2` TINYTEXT NULL DEFAULT NULL COMMENT 'The third part fo the path' COLLATE 'latin1_swedish_ci',
# 	`Description` TINYINT(4) NULL DEFAULT NULL,
	

COLUMNS = (
    'keyCombineTests',
    'fkParentTest',
    'fkDUT_Type',
    'Timestamp',
    'fkPath0_TestId',
    'Path1',
    'Path2',
    'Description'
)

class CombineTestsRecord(BaseModel):
    """ A record in the DBBand6Cart.CombineTests table    
    """
    key: int = None                     # keyCombineTests assigned by the database on insert.
    fkParentTest: int                   # CartTest or MxrTest which owns this selection
    fkDutType: int                      # value from DUT_Type enum
    timeStamp: datetime = None
    path0_TestId: int                   # the referenced CartTest or MxrTest
    path1: Optional[str] = None         # frequency
    path2: Optional[str] = None         # fkBeamPatterns
    description: Optional[str] = None   # text from table to show in description column
    text: Optional[str] = None          # syntesized text to show in ID/frequency column

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()   
        return "{},{},'{}',{},{},{},{}".format(
            self.fkParentTest,
            self.fkDutType,
            self.timeStamp,
            self.path0_TestId,
            f"'{self.path1}'" if self.path1 else 'NULL',
            f"'{self.path2}'" if self.path2 else 'NULL',
            f"'{self.description}'" if self.description else 'NULL'
        )
    
    def __eq__(self, other):
        if self.fkParentTest != other.fkParentTest:
            return False
        if self.fkDutType != other.fkDutType:
            return False
        if self.path0_TestId != other.path0_TestId:
            return False
        if self.path1 is not None and self.path1 != other.path1:
            return False
        if self.path2 is not None and self.path2 != other.path2:
            return False
        return True