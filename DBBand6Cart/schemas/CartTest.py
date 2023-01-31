from pydantic import BaseModel
from datetime import datetime

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

COLUMNS = ('keyCartTest',
           'fkCartAssembly',
           'fkSoftwareVersion',
           'fkTestType',
           'fkTestSystem',
           'Timestamp',
           'Description',
           'Operator',
           'DewarID')
            
# schema for a CartTests record
class CartTest(BaseModel):
    key: int = None     # keyCartTests
    configId: int       # fkCartAssembly
    isSelection: bool = False
    fkSoftwareVersion: int = 0
    fkTestType: int = 0
    fkTestSystem: int = 0
    timeStamp: datetime = datetime.now()
    description: str = ''
    operator: str = ''
    testSysName: str = '' # DewarID
    measSwName: str = ''
    measSwVersion: str = ''
    
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