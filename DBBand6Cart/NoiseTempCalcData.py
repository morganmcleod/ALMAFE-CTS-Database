from ALMAFE.database.DriverMySQL import DriverMySQL
from pandas import DataFrame
from typing import List

# from NT_Raw_Data:
COLUMNS = ( 
    'keyNT_Calc_Data',
    'fkCartTest',
    'TS',
    'Pol',
    'FreqLO',
    'CenterIF',
    'USB_Signal_Frequency',
    'LSB_Signal_Frequency',
    'Y_USB',
    'Y_LSB',
    'M_USB',
    'M_LSB',
    'M_DSB',
    'ImgRej_USB',
    'ImgRej_LSB',
    'Tsys_Uncorrected_USB',
    'Tsys_Uncorrected_LSB',
    'Tsys_Corrected_USB',
    'Tsys_Corrected_LSB',
    'PifHot',
    'PifCold',
    'yIFAvg',
    'Ambient',
    'TifHot',
    'ENR',
    'IFSysNoiseTemp',
    'G_Uncorrected_USB',
    'G_Uncorrected_LSB',
    'G_Corrected_USB',
    'G_Corrected_LSB',
    'Treceiver_USB',
    'Treceiver_LSB',
    'PwrDens_USB',
    'PwrDens_LSB',
    'DataMod'
)

class NoiseTempCalcData(object):
    """
    Create, Read, Update, Delete records in dbBand6Cart.NT_Calc_Data
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
        
    def create(self, ntCalculated:DataFrame):
        """
        Create records in NT_RawData
        :param data: pandas.DataFrame
        """
        q = "INSERT INTO NT_Calc_Data({}) VALUES ".format(",".join(COLUMNS[1:]))
        vals = ""
        
        for row in ntCalculated.itertuples(index = False):
            if vals:
                vals += ","
            vals += "({},'{}',{})".format(
                row[1], 
                row[2].strftime(self.DB.TIMESTAMP_FORMAT) if row[1] else '',
                ",".join([str(x) for x in row[3:]]))
        q += vals
        self.DB.execute(q, commit = True)
        
    def read(self, fkCartTest:int):
        """
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        """
        q = "SELECT {} FROM NT_Calc_Data WHERE fkCartTest = {} ORDER BY keyNT_Raw_Data;"\
            .format(','.join(COLUMNS), fkCartTest)

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = COLUMNS)
 
    def update(self, fkCartTest:int, ntCalculated:DataFrame):
        """
        Update is equivalent to delete all records referencing fkCartTes in the provided data
        folowed by create()
        :param data: pandas.DataFrame
        """
        self.delete(fkCartTest)
        self.create(ntCalculated)
    
    def delete(self, fkCartTest:int):
        """
        Delete records referencing fkCartTest 
        :param fkCartTest: selector
        """
        q = "DELETE FROM NT_Calc_Data WHERE fkCartTest = {};".format(fkCartTest)
        self.DB.execute(q, commit = True)
        
    