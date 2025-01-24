""" Schema for records of the DBBand6Cart.BP_Jobs table

During each raster scan, referenced by fkBeamPatterns, zero or more errors may be logged here.
"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# CREATE TABLE `BP_Jobs` (
# 	`keyPatternJobs` INT(10) NOT NULL AUTO_INCREMENT,
# 	`PatternNum` INT(10) NOT NULL DEFAULT '0',
# 	`FileName_FF_Data` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`FileName_NF_Amp_Plot` TEXT NULL DEFAULT NULL COMMENT 'Normalize the pattern by this in dB' COLLATE 'latin1_swedish_ci',
# 	`FileName_NF_Phase_Plot` TEXT NULL DEFAULT NULL COMMENT 'Normalize the pattern by this in dB' COLLATE 'latin1_swedish_ci',
# 	`FileName_FF_Amp_Plot` TEXT NULL DEFAULT NULL COMMENT 'Normalize the pattern by this in dB' COLLATE 'latin1_swedish_ci',
# 	`FileName_FF_Phase_Plot` TEXT NULL DEFAULT NULL COMMENT 'Normalize the pattern by this in dB' COLLATE 'latin1_swedish_ci',
# 	`NormalizeFactor` DOUBLE NULL DEFAULT '0' COMMENT 'Normalize the pattern by this in dB',
# 	`FileName_NF_Amp_Plot_NoNorm` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`FileName_NF_Phase_Plot_NoNorm` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`GainCalculated` DOUBLE NULL DEFAULT NULL,
# 	`PatternNumCoPol` INT(10) NULL DEFAULT NULL COMMENT 'Co-pol pattern number can be used for normalization',
# 	`EveryOtherScan` INT(8) NULL DEFAULT '0',
# 	`DateCompleted` DATETIME NULL DEFAULT NULL,
# 	`Notes` TEXT NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`TS` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyPatternJobs',
    'PatternNum',
    'FileName_NF_Amp_Plot',
    'FileName_NF_Phase_Plot',
    'FileName_FF_Amp_Plot',
    'FileName_FF_Phase_Plot',
    'TS',
    'DateCompleted'
)

class BPJob(BaseModel):
    key: int = 0
    fkBeamPattern: int = 0
    NFAmpPlot: str = ""
    NFPhasePlot: str = ""
    FFAmpPlot: str = ""
    FFPhasePlot: str = ""
    timeStamp: datetime = None    # measured
    timeStampProcessed: datetime = None

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        return "{},'{}','{}','{}','{}',{},{}".format(
            self.fkBeamPattern,
            self.NFAmpPlot,
            self.NFPhasePlot,
            self.FFAmpPlot,
            self.FFPhasePlot,
            f"'{self.timeStamp}'" if self.timeStamp is not None else "NULL",
            f"'{self.timeStampProcessed}'" if self.timeStampProcessed is not None else "NULL"
        )
