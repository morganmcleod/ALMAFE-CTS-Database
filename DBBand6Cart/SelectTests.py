""" Create, Read, Update, Delete table dbBand6Cart.SelectTests records
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schemas.SelectTestsRecord import SelectTestsRecord, COLUMNS
from .schemas.DUT_Type import DUT_Type

class SelectTests(object):
    """ Create, Read, Update, Delete table dbBand6Cart.SelectTests records

    This table creates a one-to-many self-mapping from table CartTests or MxrTests
    where each record calls out another CartTests or MxrTests.
    For the child test table there is also associated a frequency or another subheader key.
    Examples:
        Parent: a MxrTest, child: a MxrTest and an LO frequency.
        Parent: a CartTest, child: a key from the BeamPatterns table.
    This allows 'virtual' test sets to be created by combining existing measurements.
    """

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, rows: List[SelectTestsRecord]) -> bool:
        """ Create records in the SelectTests table.
        
        :param rows: list[SelectTestsRecord]
        :return True if successful        
        """
        q = f"INSERT INTO SelectTests({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for row in rows:
            try:
                dutType = DUT_Type(row.fkDutType)
            except:
                raise ValueError(f"SelectTests.create: fkDutType '{row.fkDutType}' not supported")

            if values:
                values += ","
            values += f"({row.getInsertVals()})"

        q += values + ";"
        return self.DB.execute(q, commit = True)
            
    def read(self, fkParentTest:int) -> Optional[List[SelectTestsRecord]]:
        """ Read records from the SelectTests table having the given fkCartTest

        :param fkParentTest: int selector
        :return list[SelectTestsRecord] or None if not found
        """
        q = f"SELECT {','.join(COLUMNS)} FROM SelectTests WHERE fkParentTest = {fkParentTest};"        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        return [SelectTestsRecord(
            key = row[0],
            fkParentTest = row[1],
            fkDutType = row[2],
            fkChildTest = row[3],
            fkSubHeader = row[4] if row[4] else None,
            frequency = row[5] if row[5] else None,
            timeStamp = makeTimeStamp(row[6])
        ) for row in rows]
            
    def update(self, rows:List[SelectTestsRecord]) -> bool:
        """ Update records in the SelectTests table.

        Because this table creates a one-to-many self-mapping, update is eqivalent 
        to delete for the referenced fkParentTest then insert the given records.
        :param rows: list[SelectTestsRecord] to delete
        :return True if successful
        """
        if rows:
            if (self.delete(rows[0].fkParentTest)):
                return self.create(rows)
            else:
                return False
        
    def delete(self, fkParentTest: int) -> bool:
        """
        Delete records from SelectTests tables
        :param selection: list[SelectTestsRecord]
        :return True if successful
        """
        q = f"DELETE FROM SelectTests WHERE fkParentTest={fkParentTest};"
        return self.DB.execute(q, commit = True)
