""" Create, Read, Update, Delete table dbBand6Cart.CartTestsSelection records
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# CREATE TABLE `CartTestsSelection` (
# 	`keyCartTestsSelection` INT(11) NOT NULL AUTO_INCREMENT,
# 	`fkCartTests` INT(11) NOT NULL COMMENT 'reference to the CartTests record which owns this selection',
# 	`selCartTests` INT(11) NOT NULL COMMENT 'references to one or more CartTests having the original data',
# 	`frequency` DOUBLE NOT NULL DEFAULT '0' COMMENT 'frequencies (LO or RF) from selCartTests to include in this selection',
# 	`Timestamp` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	PRIMARY KEY (`keyCartTestsSelection`) USING BTREE,
# 	INDEX `Index 2` (`fkCartTests`) USING BTREE
# )

class Selection(BaseModel):
    """ A record in the DBBand6Cart.CartTestsSelection table
    """
    fkCartTests: int    # what 'virtual' CartTest this is a child record of
    selCartTests: int   # what original CartTest this references
    frequency: float    # and the frequency (LO/RF) to reference
    timeStamp: datetime = datetime.now()

    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        return "{},{},{},'{}'".format(
            self.fkCartTests, 
            self.selCartTests, 
            self.frequency,
            self.timeStamp
        )
    
COLUMNS = (
    'fkCartTests',
    'selCartTests',
    'frequency',
    'Timestamp'
)

class CartTestSelection(object):
    """ Create, Read, Update, Delete table dbBand6Cart.CartTestsSelection records

    This table creates a one-to-many self-mapping for table CartTests, 
    where each record calls out a CartTest and one frequency (LO/RF) of measurement data.
    This allows 'virtual' CartTests to be created by combining existing measurements.
    """

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor

        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, selection:List[Selection]) -> bool:
        """ Create records in the CartTestsSelection table.
        
        :param selection: list[Selection]
        :return True if successful        
        """
        q = f"INSERT INTO CartTestsSelection({','.join(COLUMNS)}) VALUES "
        values = ""
        for sel in selection:
            if values:
                values += ","
            values += f"({sel.getInsertVals()})"

        q += values + ";"
        return self.DB.execute(q, commit = True)
            
    def read(self, fkCartTest:int) -> Optional[List[Selection]]:
        """ Read records from the CartTestsSelection table having the given fkCartTest

        :param fkCartTest: int selector
        :return list[Selection] or None if not found
        """
        q = f"SELECT {','.join(COLUMNS)} FROM CartTestsSelection WHERE fkCartTests = {fkCartTest};"        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None

        return [Selection(
            fkCartTests = row[0], 
            selCartTests = row[1], 
            frequency = row[2],
            timeStamp = makeTimeStamp(row[3])
        ) for row in rows]
            
    def update(self, selection:List[Selection]) -> bool:
        """ Update records in the CartTestsSelection table.

        Because this table creates a one-to-many self-mapping, update is eqivalent 
        to delete for the referenced fkCartTests then insert the given records.
        :param selection: list[Selection]
        :return True if successful        
        """
        if (self.delete(selection)):
            return self.create(selection)
        else:
            return False
        
    def delete(self, selection:List[Selection]) -> bool:
        """
        Delete records from CartTests and CartTestsSelection tables
        :param selection: list[Selection]
        :return True if successful
        """
        where = ""
        for sel in selection:
            if where:
                where += " OR "
            where += f"(fkCartTests={sel.fkCartTests}"
            if sel.frequency > 0.0:
                where += f" AND frequency={sel.frequency}"
            where += ")"
                
        q = "DELETE FROM CartTestsSelection WHERE " + where + ";"
        return self.DB.execute(q, commit = True)      
