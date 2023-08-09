""" Schema for records of the DBBand6Cart.CartTests table

Each record represents a measurement initiated by the CTS user.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# CREATE TABLE `CartTests` (
# 	`keyCartTest` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartAssembly` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkSoftwareVersion` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkTestType` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkTestSystem` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`Timestamp` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`Description` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Operator` VARCHAR(30) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`DewarID` VARCHAR(30) NULL DEFAULT '1' COMMENT '1=CTS1, 2=CTS2' COLLATE 'latin1_swedish_ci',
# 	`Validity` SMALLINT(5) NOT NULL DEFAULT '1',
# 	PRIMARY KEY (`keyCartTest`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyCartTest',
    'fkCartAssembly',
    'fkColdCarts',
    'fkSoftwareVersion',
    'fkTestType',
    'fkTestSystem',
    'Timestamp',
    'Description',
    'Operator',
    'DewarID'
)
            
# schema for a CartTests record
class CartTest(BaseModel):
    """A record in the DBBand6Cart.CartTests table
    """
    key: int = 0                        # keyCartTests is assigned by the database on insert.
    configId: int                       # fkColdCart
    cartAssyId: Optional[int] = None    # fkCartAssembly, vestigial
    isSelection: bool = False           # for making "virtual" CartTests, to combine data from multiple runs
    fkSoftwareVersion: int = 0
    fkTestType: int = 0
    fkTestSystem: int = 0
    timeStamp: datetime = datetime.now()
    description: str = ''
    operator: str = ''
    testSysName: str = ''               # DewarID
    measSwName: str = ''
    measSwVersion: str = ''
    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        return "{},{},{},{},{},'{}','{}','{}','{}'".format(
            self.cartAssyId if self.cartAssyId else 0,
            self.configId, 
            self.fkSoftwareVersion, 
            self.fkTestType,
            self.fkTestSystem, 
            self.timeStamp,
            self.description, 
            self.operator,
            self.testSysName
        )

    def makeSwVersionString(self) -> str:
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