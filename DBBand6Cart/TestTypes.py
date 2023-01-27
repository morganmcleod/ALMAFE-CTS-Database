from ALMAFE.database.DriverMySQL import DriverMySQL
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

class TestTypes(object):
    '''
    Read the dbBand6Cart.TestTypes table
    '''

    # Show only these test types in wildcard query (for combobox):
    SUPPORTED_TESTTYPES = (
        TestTypeIds.NOISE_TEMP,
        TestTypeIds.BEAM_PATTERN,
        TestTypeIds.PHASE_STABILITY,
        TestTypeIds.AMP_STABILITY,
        TestTypeIds.LO_WG_INTEGRITY
    )

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        self.supportedTypes = "(" + ",".join([str(t.value) for t in self.SUPPORTED_TESTTYPES]) + ")"
    
    def read(self, keyTestType:int = None):
        '''
        Get the test type corresponding to keyTestType, or all test types.
        :param keyTestType: int optional
        :return list of TestType or None if not found
        '''
        q = "SELECT keyTestType, Name, Description FROM TestTypes"
        if keyTestType:
            q += " WHERE keyTestType = {}".format(keyTestType)
        else:
            q += " WHERE keyTestType IN " + self.supportedTypes
        q += " ORDER BY keyTestType;"
       
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of TestType:            
            return [TestType(id = row[0], 
                             name = row[1], 
                             description = row[2]
                    ) for row in rows]
