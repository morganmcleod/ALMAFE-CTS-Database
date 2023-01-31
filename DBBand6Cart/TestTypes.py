from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.TestType import TestTypeIds, TestType

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
