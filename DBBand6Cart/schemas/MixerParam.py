from pydantic import BaseModel
from datetime import datetime

# CREATE TABLE 'MixerParams' (
# 	'keyMixerParams' INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	'fkMixerChips' INT(10) UNSIGNED NULL DEFAULT '0',
# 	'Temperature' FLOAT(5,2) NULL DEFAULT NULL COMMENT 'temperature at which bias values apply Kelvin',
# 	'FreqLO' DECIMAL(10,6) NOT NULL DEFAULT '0.000000' COMMENT 'LO frequency GHz',
# 	'TS' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	'VJ' FLOAT(4,2) NOT NULL DEFAULT '0.00' COMMENT 'Mixer junction bias voltage mV',
# 	'IJ' FLOAT(5,1) NOT NULL DEFAULT '0.0' COMMENT 'Mixer junction bias current uA',
# 	'IMAG' FLOAT(4,1) NOT NULL DEFAULT '0.0' COMMENT 'Mixer magnet current mA',
# 	'lnk_Data' VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY ('keyMixerParams') USING BTREE,
# 	INDEX 'Mixer' ('fkMixerChips') USING BTREE
# )

COLUMNS = (
    'keyMixerParams',
    'fkMixerChips',
    'FreqLO',
    'TS',
    'VJ',
    'IJ',
    'IMAG'
)

class MixerParam(BaseModel):
    key:int = None  # keyMixerParams
    fkMixerChips: int = None
    FreqLO: float = None
    timeStamp: datetime = None
    VJ:float = None
    IJ:float = None
    IMAG:float = None