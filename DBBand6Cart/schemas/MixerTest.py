""" Schema for records of the DBBand6Cart.MxrTests table

Each record represents a measurement initiated by the MTS user.
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `MxrTests` (
# 	`keyMxrTest` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkMxrPreampAssys` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkSoftwareVersion` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkTestType` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`Timestamp` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`Description` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Operator` VARCHAR(30) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Validity` TINYINT(5) NOT NULL DEFAULT '1',
# 	PRIMARY KEY (`keyMxrTest`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyMxrTest',
    'fkMxrPreampAssys',
    'fkSoftwareVersion',
    'fkTestType',
    'Timestamp',
    'Description',
    'Operator'
)

class MixerTest(BaseModel):
    """A record in the DBBand6Cart.CartTests table
    """
    key: int = 0                            # keyMxrTest is assigned by the database on insert.
    configId: int                           # fkMxrPreampAssys
    fkSoftwareVersion: int = 0
    fkTestType: int
    timeStamp: datetime = None
    description: str = ''
    operator: str = ''
    measSwName: str = ''
    measSwVersion: str = ''
    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},{},'{}','{}','{}'".format(
           self.configId, 
           self.fkSoftwareVersion, 
           self.fkTestType,
           self.timeStamp,
           self.description, 
           self.operator
        )

    def makeSwVersionString(self):
        swVer = self.measSwName if self.measSwName else ''
        if self.measSwVersion:
            if swVer:
                swVer += ' '
            swVer += self.measSwVersion
        elif self.fkSoftwareVersion:
            if swVer:
                swVer += ' '
            swVer += 'fk:' + str(self.fkSoftwareVersion)
        return swVer   