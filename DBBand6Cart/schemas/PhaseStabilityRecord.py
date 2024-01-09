from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `PhaseDrift_Calc_Data` (
# 	`keyPhaseDrift_Calc_Data` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartTest` INT(11) NULL DEFAULT NULL,
# 	`fkRawData` INT(11) NULL DEFAULT NULL,
# 	`TS` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
# 	`FreqLO` DOUBLE NULL DEFAULT NULL,
# 	`FreqCarrier` DOUBLE NULL DEFAULT NULL,
# 	`Pol` TINYINT(4) NULL DEFAULT NULL,
# 	`SB` TINYINT(4) NULL DEFAULT NULL,
# 	`time_sec` FLOAT NULL DEFAULT NULL,
# 	`AllanDev` FLOAT NULL DEFAULT NULL,
# 	`ErrorBar` FLOAT NULL DEFAULT NULL,
# 	PRIMARY KEY (`keyPhaseDrift_Calc_Data`) USING BTREE,
# 	INDEX `fkCartTest` (`fkCartTest`) USING BTREE,
# 	INDEX `fkRawData` (`fkRawData`) USING BTREE

COLUMNS = (
    'keyPhaseDrift_Calc_Data',
    'fkCartTest',
    'fkRawData',
    'TS',
    'FreqLO',
    'FreqCarrier',
    'Pol',
    'SB',
    'time_sec',
    'AllanDev',
    'ErrorBar'
)

class PhaseStabilityRecord(BaseModel):
    key: int = None                 # keyPhaseDrift_Calc_Data assigned by the database on insert
    fkCartTest: int
    fkRawData: int                  # References the raw data in SQLite on the measurement system
    timeStamp: datetime = None
    freqLO: float
    freqCarrier: float
    pol: int
    sideband: int                   # 0=LSB, 1=USB
    time: float
    allanDev: float
    errorBar: float

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},'{}',{},{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.fkRawData,
            self.timeStamp,
            self.freqLO,
            self.freqCarrier,
            self.pol,
            self.sideband,
            self.time,
            self.allanDev,
            self.errorBar
        )
