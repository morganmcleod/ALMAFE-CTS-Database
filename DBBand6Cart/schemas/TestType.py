from pydantic import BaseModel
from enum import Enum

class TestTypeIds(Enum):
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
    id: int
    name: str
    description: str = ''
