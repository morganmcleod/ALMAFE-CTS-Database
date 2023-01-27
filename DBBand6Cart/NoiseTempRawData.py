from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from DBBand6Cart.CartTestSelection import Selection
from pandas import DataFrame
from typing import List

class NoiseTempRawData(object):
    '''
    Create, Read, Update, Delete records in dbBand6Cart.NT_Raw_Data
    We use pandas.DataFrame to convey records in and out.
    '''    
    # columns from NT_Raw_Data:
    columns = ( 'keyNT_Raw_Data',
                'TS',
                'FreqLO',
                'CenterIF',
                'BWIF',
                'Pol',
                'PwrUSB_SrcLSB',
                'PwrLSB_SrcLSB',
                'PwrUSB_SrcUSB',
                'PwrLSB_SrcUSB',
                'Phot_LSB',
                'Pcold_LSB',
                'Phot_LSB_StdErr',
                'Pcold_LSB_StdErr',
                'LSB_Pass',
                'Phot_USB',
                'Pcold_USB',
                'Phot_USB_StdErr',
                'Pcold_USB_StdErr',
                'USB_Pass',
                'TRF_Hot',
                'IF_Attn',
                'Vj1',
                'Ij1',
                'Vj2',
                'Ij2',
                'Imag',
                'Tmixer',
                'PLL_Lock_V',
                'PLL_Corr_V',
                'PLL_Assm_T',
                'PA_A_Drain_V',
                'PA_B_Drain_V',
                'Source_Power' )

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, data:DataFrame):
        '''
        Create records in NT_RawData
        :param data: pandas.DataFrame
        '''
        #TODO: implement NoiseTempRawData.create when needed
        raise(NotImplementedError)
        
    def read(self, fkCartTest:int):
        '''
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        '''
        q = "SELECT {} FROM NT_Raw_Data WHERE fkCartTest = {} ORDER BY keyNT_Raw_Data;"\
            .format(','.join(self.columns), fkCartTest)

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = self.columns)
    
    def readCartTests(self):
        '''
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return dict { fkCartTest: (numMeas, minTS, maxTS) } 
        '''
        q = '''SELECT fkCartTest, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS 
            FROM NT_Raw_Data GROUP BY fkCartTest;'''
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return {row[0] : (row[1], makeTimeStamp(row[2]), makeTimeStamp(row[3])) for row in rows}
        
    def readLOFreqs(self, fkCartTest:int):
        '''
        Read the available LO frequencies for a CartTest
        :param cartTests: schema object list of int
        :return list [Selection] or None if not found
        '''
        q = '''SELECT MIN(TS), FreqLO FROM NT_Raw_Data WHERE fkCartTest = {}
            GROUP BY FreqLO'''.format(fkCartTest)
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [Selection(fkCartTests = fkCartTest,
                              selCartTests = fkCartTest,
                              timeStamp = makeTimeStamp(row[0]),
                              frequency = row[1])
                              for row in rows]

    def readForSelection(self, selection:List[Selection]):
        '''
        Read noise temperature raw data specific cartTestIds and LO frequencies
        :param selection: list[Selection] to retrieve
        :return pandas DataFrame or None if not found
        '''
        q = "SELECT {} FROM NT_Raw_Data WHERE ".format(",".join(self.columns)) 
        
        where = ""
        for item in selection:
            if where:
                where += " OR "
            where += "(fkCartTest = {} AND FreqLO  = {})".format(item.selCartTests, item.frequency)
        q += where + " ORDER BY keyNT_Raw_Data;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = self.columns)       

    def update(self, data:DataFrame):
        '''
        Update is equivalent to delete all records referencing fkCartTes in the provided data
        folowed by create()
        :param data: pandas.DataFrame
        '''
        #TODO: implement NoiseTempRawData.update when needed
        raise(NotImplementedError)
    
    def delete(self, fkCartTest:int):
        '''
        Delete records referencing fkCartTest 
        :param fkCartTest: selector
        '''
        #TODO: implement NoiseTempRawData.delete when needed
        raise(NotImplementedError)
        
        
    