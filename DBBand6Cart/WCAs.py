from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.WCA import WCA, COLUMNS

class WCAs():
    """
    WCAs table in dbBand6Cart
    """

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyWCAs: int = None, serialNum: str = None, serialNumLike: str = None):
        '''Read the latest record for each WCA SN
        '''

        q = """SELECT A.keyWCAs,A.TS,A.SN,A.FloYIG,A.FhiYIG FROM WCAs AS A
            LEFT JOIN WCAs AS B ON A.SN = B.SN AND B.TS > A.TS
            WHERE B.TS IS NULL"""
        
        if keyWCAs:
            q += f" AND A.keyWCAs = {keyWCAs}"

        if serialNum:
            q += f" AND A.SN = '{serialNum}'"

        if serialNumLike:
            q += f" AND A.SN LIKE '{serialNumLike}'"

        q += " ORDER BY A.SN ASC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        
        return [WCA(
            key = row[0],
            timeStamp = makeTimeStamp(row[1]),
            serialNum = row[2],
            ytoLowGHz = row[3],
            ytoHighGHz = row[4]
        ) for row in rows]
    