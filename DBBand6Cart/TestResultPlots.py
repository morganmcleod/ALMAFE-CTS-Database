from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List, Union, Optional

class TestResultPlot(BaseModel):
    id: int = 0
    plotBinary: Optional[bytes] = None
    contentType: str = "image/png"
    description: str = None
    timeStamp: datetime = None

COLUMNS = (
    'keyTestResultPlot',
    'ContentType',
    'Description',
    'Timestamp',
    'PlotBinary'
)

class TestResultPlots(object):
    """
    Create, Read, Update, Delete table dbBand6Cart.TestResultPlots records
    """

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, record:TestResultPlot):
        """
        Create a new record in the TestResultPlots table
        :param plotBinary: to store
        :return int keyTestResultPlot of new record or None if failed
        """
        q = "INSERT INTO TestResultPlots(PlotBinary, ContentType, Description) VALUES (%s, %s, %s);"
        
        params = (record.plotBinary, record.contentType, record.description)
        if not self.DB.execute(q, params):
            return None
        
        self.DB.execute("SELECT LAST_INSERT_ID()")
        row = self.DB.fetchone()
        if not row:
            return None
        
        self.DB.commit()
        return row[0]
    
    def read(self, keys:Union[int, List[int]], noBinary = False):
        """
        Read one or more records from TestResultPlots
        :param keys: key or list of keys of records to read
        :param noBinary: if true don't load the binary data from the database
        :return list of TestResultPlot or None if not found
        """
        if not keys:
            return None;
        
        if not isinstance(keys, list):
            keys = [keys]
        
        cols = COLUMNS[:-1] if noBinary else COLUMNS 
        
        q = "SELECT {} FROM TestResultPlots WHERE keyTestResultPlot in ({});"\
            .format(",".join(cols), ",".join([str(key) for key in keys]))
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [TestResultPlot(id = row[0],
                                   contentType = row[1],
                                   description = row[2],
                                   timeStamp = makeTimeStamp(row[3]),
                                   plotBinary = None if noBinary else row[4]) 
                                   for row in rows]
        
    def update(self, record:TestResultPlot):
        """
        Update the specified TestResultPlots record
        :param keyTestResultPlot of record to update
        :param imageData to store
        :return True if successful
        """
        q = """UPDATE TestResultPlots SET PlotBinary = %s, Timestamp = %s, Description = %s, ContentType = %s
               WHERE keyTestResultPlot = {};""".format(record.id)
        params = (record.plotBinary, record.timeStamp, record.description, record.contentType)
        
        if self.DB.execute(q, params, commit = True):
            return True
        else:
            return False

    def delete(self, keys:Union[int, List[int]]):
        """
        Delete the specified record(s) from TestResultPlots
        :param keys int or list of ints of keyTestResultPlots to delete
        :return True if successful
        """
        if not isinstance(keys, list):
            keys = [keys]
        keys = [str(key) for key in keys]
        
        q = "DELETE FROM TestResultPlots WHERE keyTestResultPlot in ({});".format(",".join(keys))
        if self.DB.execute(q, commit = True):
            return True
        else:
            return False
        