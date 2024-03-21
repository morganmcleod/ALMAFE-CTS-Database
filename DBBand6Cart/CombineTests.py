""" Create, Read, Update, Delete table dbBand6Cart.CombineTests records
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .schemas.CombineTestsRecord import CombineTestsRecord, COLUMNS
from .schemas.DUT_Type import DUT_Type

class CombineTests(object):
    """ Create, Read, Update, Delete table dbBand6Cart.CombineTests records

    This table creates a one-to-many mapping from table CartTests or MxrTests
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
        
    def create(self, rows: List[CombineTestsRecord]) -> bool:
        """ Create records in the CombineTests table.
        
        :param rows: list[CombineTestsRecord]
        :return True if successful        
        """
        q = f"INSERT INTO CombineTests({','.join(COLUMNS[1:])}) VALUES "
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
            
    def read(self, fkParentTest:int) -> Optional[List[CombineTestsRecord]]:
        """ Read records from the CombineTests table having the given fkCartTest

        :param fkParentTest: int selector
        :return list[SelectTestsRecord] or None if not found
        """
        q = f"SELECT {','.join(COLUMNS)} FROM CombineTests WHERE fkParentTest = {fkParentTest};"        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        result = []
        for row in rows:
            
            text = f"{row[4]}"
            if row[5]:
                text += f": {float(row[5])}"

            result.append(CombineTestsRecord(
                key = row[0],
                fkParentTest = row[1],
                fkDutType = row[2],
                timeStamp = makeTimeStamp(row[3]),
                path0_TestId = row[4],
                path1 = row[5] if row[5] else None,
                path2 = row[6] if row[6] else None,
                description = row[7] if row[7] else None,
                text = text
            ))
        return result
            
    def update(self, fkParentTest: int, rows: List[CombineTestsRecord]) -> bool:
        """ Update records in the CombineTests table.

        Because this table creates a one-to-many mapping, update is eqivalent 
        to delete for the referenced fkParentTest then insert the given records.
        :param fkParentTest the ID of the combination to update
        :param rows: list[CombineTestsRecord] new referenced records
        :return True if successful
        """
        if self.delete(fkParentTest):
            if not rows:
                return True
        for row in rows:
            row.fkParentTest = fkParentTest
        return self.create(rows)
        
    def delete(self, fkParentTest: int) -> bool:
        """
        Delete records from CombineTests tables
        :param selection: list[SelectTestsRecord]
        :return True if successful
        """
        q = f"DELETE FROM CombineTests WHERE fkParentTest={fkParentTest};"
        return self.DB.execute(q, commit = True)
