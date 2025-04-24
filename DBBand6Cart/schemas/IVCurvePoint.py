"""Schema for records of the DBBand6Cart.MxrIVcurves table
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE `MxrIVcurves` (
# 	`keyMxrIVsweep` INT(11) NOT NULL AUTO_INCREMENT,
# 	`fkMxrPreampAssys` INT(11) NULL DEFAULT NULL COMMENT 'FK to mixer chip',
# 	`fkMxrTests` INT(11) NULL DEFAULT NULL COMMENT 'FK to test ID',
# 	`FreqLO` FLOAT NULL DEFAULT NULL COMMENT 'Local Oscillator Frequency, GHz',
# 	`MixerChip` CHAR(50) NULL DEFAULT NULL COMMENT '1R or 2L' COLLATE 'latin1_swedish_ci',
# 	`Imag` FLOAT NULL DEFAULT NULL COMMENT 'Magnetic field current, mA',
# 	`Vj` FLOAT NULL DEFAULT NULL COMMENT 'Junction voltage, mV',
# 	`Ij` FLOAT NULL DEFAULT NULL COMMENT 'Junction current, uA',
# 	`IFPower` FLOAT NULL DEFAULT NULL COMMENT 'IF power, dBm.  BW varies by test system.',
# 	`isPCold` TINYINT NULL DEFAULT NULL COMMENT 'Is IFPower measured on the cold load? (1 = true)',
# 	`isOperatingPoint` TINYINT NULL DEFAULT NULL COMMENT 'Is this an operating point? (0 = true)',
# 	`isPumped` TINYINT NULL DEFAULT NULL COMMENT 'Is this pumped IV data? (0 = true)',
# 	`PumpPwr` FLOAT NULL DEFAULT NULL COMMENT 'LO pump power as percent of maximum LO PA control.',
# 	`DateMeas` DATETIME NULL DEFAULT NULL COMMENT 'Measurement date',
# 	`TS` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when record created',
# 	PRIMARY KEY (`keyMxrIVsweep`) USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyMxrIVsweep', 
    'fkMxrPreampAssys',
    'fkMxrTests',
    'FreqLO',
    'MixerChip',
    'Imag',
    'Vj',
    'Ij',
    'IFPower',
    'isPCold',
    'PumpPwr',
    'DateMeas'
)

class IVCurvePoint(BaseModel):
    """A record in the DBBand6Cart.MxrIVcurves table
    """
    key: int = 0        # keyMxrIVsweep is assigned by the database on insert.
    fkMxrPreampAssys: int
    fkMixerTest: int
    FreqLO: float
    MixerChip: str
    Imag: float
    Vj: float
    Ij: float
    IFPower: float | None = None
    isPCold: bool = False
    PumpPwr: float
    timeStamp: datetime = None

    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()        
        return "{},{},{},'{}',{},{},{},{},{},{},'{}'".format(
            self.fkMxrPreampAssys,
            self.fkMixerTest,
            self.FreqLO,
            self.MixerChip,
            self.Imag,
            self.Vj,
            self.Ij,
            self.IFPower if self.IFPower is not None else 'NULL',
            self.isPCold,
            self.PumpPwr,
            self.timeStamp
        )




