from ALMAFE.database.DriverMySQL import DriverMySQL
from pandas import DataFrame

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
    'TifCold',
    'TifHot',
    'NoiseDiodeENR' 
)

class WarmIFNoiseData(object):
    """
    Create, Read, Update, Delete records in dbBand6Cart.WarmIF_Noise_Data
    We use pandas.DataFrame to convey records in and out.
    """    

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, data:DataFrame):
        """
        Create records in WarmIF_Noise_Data
        :param data: pandas.DataFrame
        """
        #TODO: implement WarmIFNoiseData.create when needed
        raise(NotImplementedError)
    
    def read(self, fkCartTest:int):
        """
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        """
        q = "SELECT {} FROM WarmIF_Noise_Data WHERE fkCartTest = {} ORDER BY keyWarmIF_Noise_Data;"\
            .format(','.join(COLUMNS), fkCartTest)

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = COLUMNS)
    
    def readCartTests(self):
        """
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return list[int]
        """
        q = 'SELECT DISTINCT fkCartTest FROM WarmIF_Noise_Data ORDER BY fkCartTest;'
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [row[0] for row in rows]
    
    def update(self, data:DataFrame):
        """
        Update is equivalent to delete all records referencing fkCartTes in the provided data
        folowed by create()
        :param data: pandas.DataFrame
        """
        #TODO: implement WarmIFNoiseData.update when needed
        raise(NotImplementedError)
    
    def delete(self, fkCartTest:int):
        """
        Delete records referencing fkCartTest 
        :param fkCartTest: selector
        """
        #TODO: implement WarmIFNoiseData.delete when needed
        raise(NotImplementedError)
