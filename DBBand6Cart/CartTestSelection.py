from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from typing import List
from datetime import datetime

class Selection(BaseModel):
    fkCartTests: int    # what 'virtual' CartTest this is a child record of
    selCartTests: int   # what original CartTest this references
    frequency: float    # and the frequency (LO/RF) to reference
    timeStamp: datetime = None
    
class CartTestSelection(object):
    '''
    Create, Read, Update, Delete table dbBand6Cart.CartTestsSelection records.
    This table creates a one-to-many self-mapping for table CartTests, 
    where each record calls out a CartTest and one frequency (LO/RF) of measurement data.
    This allows 'virtual' CartTests to be created by combining existing measurements.
    '''
    
    columns = ('fkCartTests',
               'selCartTests',
               'frequency',
               'Timestamp')

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, selection:List[Selection]):
        '''
        Create records in the CartTestsSelection table.
        :param selection: list[Selection]
        :return True if successful        
        '''
        q = "INSERT INTO CartTestsSelection({}) VALUES ".format(','.join(self.columns))
        firstTime = True
        for sel in selection:
            if firstTime:
                firstTime = False
            else:
                q += ','
            q += "({},{},{},'{}')".format(sel.fkCartTests, sel.selCartTests, sel.frequency, 
                                          sel.timeStamp if sel.timeStamp else datetime.now())
        q += ";"
        return self.DB.execute(q, commit = True)
            
    def read(self, fkCartTest:int):
        '''
        Read records from the CartTestsSelection table having the given fkCartTest
        :param fkCartTest: int selector
        :return list[Selection]
        '''
        q = "SELECT {} FROM CartTestsSelection WHERE fkCartTests = {};" \
            .format(','.join(self.columns), fkCartTest)
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            # return list of Selection:            
            return [Selection(fkCartTests = row[0], 
                              selCartTests = row[1], 
                              frequency = row[2],
                              timeStamp = makeTimeStamp(row[3])
                              ) for row in rows]
            
    def update(self, selection:List[Selection]):
        '''
        Update records in the CartTestsSelection table.
        Because this table creates a one-to-many self-mapping, update is eqivalent 
        to delete for the referenced fkCartTests then insert the given records.
        :param selection: list[Selection]
        :return True if successful        
        '''
        if (self.delete(selection)):
            return self.create(selection)
        else:
            return False
        
    def delete(self, selection:List[Selection]):
        '''
        Delete records from CartTests and CartTestsSelection tables
        :param selection: list[Selection]
        :return True if successful
        '''
        where = ""
        for sel in selection:
            if where:
                where += " OR "
            if sel.frequency > 0.0:
                where += "(fkCartTests={} AND frequency={})".format(sel.fkCartTests, sel.frequency)
            else:    
                where += "fkCartTests={}".format(sel.fkCartTests)
        q = "DELETE FROM CartTestsSelection WHERE " + where + ";"
        return self.DB.execute(q, commit = True)      

        