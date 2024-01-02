from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `AmplitudeStability` (
# 	`keyAmplitudeStability` INT(11) NOT NULL AUTO_INCREMENT,
# 	`fkCartTest` INT(11) NULL DEFAULT NULL,
#   `fkRawData` INT(11) NULL DEFAULT NULL COMMENT 'References the raw data in SQLite on the measurement system',
# 	`TS` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
# 	`FreqLO` DOUBLE NULL DEFAULT NULL,
# 	`Pol` TINYINT(4) NULL DEFAULT NULL,
# 	`SB` TINYINT(4) NULL DEFAULT NULL,
# 	`Time` FLOAT NULL DEFAULT NULL,
# 	`AllanVar` FLOAT NULL DEFAULT NULL,
#   `ErrorBar` FLOAT NULL DEFAULT NULL,
# 	PRIMARY KEY (`keyAmplitudeStability`) USING BTREE,
# 	INDEX `fkCartTest` (`fkCartTest`) USING BTREE


COLUMNS = (
    'keyAmplitudeStability',
    'fkCartTest',
    'fkRawData',
    'TS',
    'FreqLO',
    'Pol',
    'SB',
    'Time',
    'AllanVar',
    'ErrorBar'
)

class AmplitudeStabilityRecord(BaseModel):
    key: int = None                 # keyAmplitudeStability assigned by the database on insert
    fkCartTest: int
    fkRawData: int                  # References the raw data in SQLite on the measurement system
    timeStamp: datetime = None
    freqLO: float
    pol: int
    sideband: int                   # 0=LSB, 1=USB
    time: float
    allanVar: float
    errorBar: float

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},'{}',{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.fkRawData,
            self.timeStamp,
            self.freqLO,
            self.pol,
            self.sideband,
            self.time,
            self.allanVar,
            self.errorBar
        )
