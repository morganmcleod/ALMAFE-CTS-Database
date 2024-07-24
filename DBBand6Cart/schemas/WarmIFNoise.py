from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from math import log10
import copy
from schemas.DUT_Type import DUT_Type

# CREATE TABLE `WarmIF_Noise_Data` (
# 	`keyWarmIF_Noise_Data` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartTest` INT(10) UNSIGNED NULL DEFAULT '0',
# 	`fkDUT_Type` INT(10) UNSIGNED NULL DEFAULT '0' COMMENT '2011-06-09 jee either Cart or AmpTest',
# 	`DataSet` INT(10) UNSIGNED NULL DEFAULT '0',
# 	`TS` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`YIG_Freq` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
# 	`Attn` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
# 	`Phot` FLOAT NOT NULL DEFAULT '0',
# 	`Pcold` FLOAT NOT NULL DEFAULT '0',
# 	`Ambient` FLOAT(7,3) NOT NULL DEFAULT '0.000',
# 	`TifCold` FLOAT(7,3) NOT NULL DEFAULT '0.000',
# 	`TifHot` FLOAT(7,3) NULL DEFAULT '0.000',
# 	`NoiseDiodeENR` FLOAT(7,3) NOT NULL DEFAULT '0.000',
# 	PRIMARY KEY (`keyWarmIF_Noise_Data`) USING BTREE
# )

# from WarmIF_Noise_Data:
COLUMNS = (
    'keyWarmIF_Noise_Data',
    'fkCartTest',
    'fkDUT_Type',
    'DataSet',
    'TS',
    'YIG_Freq',
    'Attn',
    'Phot',
    'Pcold',
    'Ambient',
    'NoiseDiodeENR' 
)

class WarmIFNoise(BaseModel):
    key: int = 0                  # keyWarmIF_Noise_Data normally assigned by the server on insert
    fkCartTest: int
    fkDUT_Type: DUT_Type
    dataSet: int = 1
    timeStamp: datetime = None
    freqYig: float
    atten: float
    pHot: float
    pCold: float
    tAmbient: float
    noiseDiodeENR: float
    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()        
        return "{},{},{},'{}',{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.fkDUT_Type.value, 
            self.dataSet, 
            self.timeStamp,
            self.freqYig, 
            self.atten,
            self.pHot, 
            self.pCold,
            self.tAmbient,
            self.noiseDiodeENR
        )

    def asDBM(self) -> WarmIFNoise:
        ret = copy.copy(self)
        ret.pHot = 10 * log10(self.pHot * 1000)
        ret.pCold = 10 * log10(self.pCold * 1000)
        return ret
