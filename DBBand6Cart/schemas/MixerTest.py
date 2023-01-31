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

COLUMNS = (
    'keyMxrTest',
    'fkMxrPreampAssys',
    'fkSoftwareVersion',
    'fkTestType',
    'Timestamp',
    'Description',
    'Operator'
)

# schema for a MixerTests record
class MixerTest(BaseModel):
    key: int = None     # keyMxrTest
    configId: int       # fkMxrPreampAssys
    fkSoftwareVersion: int = 0
    fkTestType: int
    timeStamp: datetime = datetime.now()
    description: str = ''
    operator: str = ''
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