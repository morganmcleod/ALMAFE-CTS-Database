"""Schema for records of the DBBand6Cart.TestTypes table

Each CartTest and MxrTest record has an fkTestType field referencing this table.
"""
from pydantic import BaseModel
from enum import Enum

# CREATE TABLE `TestTypes` (
# 	`keyTestType` TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`Name` VARCHAR(30) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	`Description` VARCHAR(60) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# 	PRIMARY KEY (`keyTestType`) USING BTREE
# )

class TestTypeIds(Enum):
    """ Test types we know about.  
    
    These are copied here from the table to make useful constants available.
    """
    UNDEFINED = 0
    NOISE_TEMP = 1
    BEAM_PATTERN = 2
    GAIN_COMPRESSION = 3
    PHASE_STABILITY = 4
    IF_PLATE_NOISE = 5
    POL_ACCURACY = 6
    AMP_STABILITY = 7
    WARM_BENCH_TEST = 8
    OSCILLATION = 11
    OPTIMUM_BIAS = 12
    TOTAL_POWER = 13
    LO_WG_INTEGRITY = 14
    
# schema for cartridge test types:
class TestType(BaseModel):
    """A record in the DBBand6Cart.TestTypes table
    """
    id: int
    name: str
    description: str = ''
