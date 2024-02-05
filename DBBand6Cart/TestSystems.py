""" Read records in DBBand6Cart.TestSystems and TestSystemNames
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.TestSystem import TestSystem
from typing import List

class TestSystems():
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyTestSystem: int = None, matchName: str = None) -> List[TestSystem]:
        """ Read one or more test system records

        :param int keyTestSystem: exactly this system, defaults to None
        :param str matchName: substring to match to TestSystemNames.Name, defaults to None
        :return List[TestSystem]: matching items        
        """
        q = """SELECT S1.keyTestSystems, N.Name, S1.TS FROM TestSystems AS S1
            LEFT JOIN TestSystems AS S2
            ON S1.fkTestSystemName = S2.fkTestSystemName AND S2.keyTestSystems > S1.keyTestSystems
            JOIN TestSystemNames AS N ON S1.fkTestSystemName = N.keyTestSystemNames
            WHERE S2.keyTestSystems IS NULL"""
        
        if keyTestSystem is not None:
            q += f" AND S1.keyTestSystems = {keyTestSystem}"

        if matchName is not None:
            q += f" AND N.Name LIKE '%{matchName}%'"

        q += " ORDER BY N.Name;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        return [TestSystem(
            key = row[0],
            name = row[1],
            timeStamp = makeTimeStamp(row[2])
        ) for row in rows]
