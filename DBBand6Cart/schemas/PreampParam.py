"""Schema for records of the DBBand6Cart.PreampParams table

For each Preamps record there are a collection of PreampParams records, each having a different FreqLO.
"""
from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE 'PreampParams' (
# 	'keyPreampParams' INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	'fkPreamps' INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	'Temperature' FLOAT(5,2) NULL DEFAULT NULL COMMENT 'temperature at which bias values apply Kelvin',
# 	'FreqLO' DECIMAL(10,6) NOT NULL DEFAULT '0.000000' COMMENT 'LO frequency GHz',
# 	'TS' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
# 	'VD1' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain voltage HFET stage1 V',
# 	'VD2' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain voltage HFET stage2 V',
# 	'VD3' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain voltage HFET stage3 V',
# 	'ID1' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain current HFET stage1 mA',
# 	'ID2' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain current HFET stage2 mA',
# 	'ID3' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Drain current HFET stage3 mA',
# 	'VG1' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Gate voltage HFET stage1 V',
# 	'VG2' FLOAT(4,2) NULL DEFAULT NULL COMMENT 'Gate voltage HFET stage2 V',
# 	'VG3' FLOAT(4,2) NULL DEFAULT NULL,
# 	'WarmData_By' VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'TS_WarmData' TIMESTAMP NULL DEFAULT NULL,
# 	'lnk_WSP' VARCHAR(4095) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'ColdData_By' VARCHAR(20) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'TS_ColdData' TIMESTAMP NULL DEFAULT NULL,
# 	'lnk_CSP' VARCHAR(4095) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	'lnk_SParams' VARCHAR(4095) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY ('keyPreampParams') USING BTREE,
# 	INDEX 'Preamp' ('fkPreamps') USING BTREE
# )

# The subset of columns to read/write:
COLUMNS = (
    'keyPreampParams', 
    'fkPreamps',
    'FreqLO',
    'TS',
    'VD1',
    'VD2',
    'VD3',
    'ID1',
    'ID2',
    'ID3',
)

class PreampParam(BaseModel):
    """A record in the DBBand6Cart.PreampParams table
    """
    key:int = None              # keyPreampParams is assigned by the database on insert.
    fkPreamps:int = None
    FreqLO:float = None
    timeStamp: datetime = None
    VD1:float = None
    VD2:float = None
    VD3:float = None
    ID1:float = None
    ID2:float = None
    ID3:float = None

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()        
        return "{},{},'{}',{},{},{},{},{},{}".format(
            self.fkPreamps,
            self.FreqLO,
            self.timeStamp,
            self.VD1,
            self.VD2,
            self.VD3,
            self.ID1,
            self.ID2,
            self.ID3
        )
