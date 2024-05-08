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

        q = """SELECT WA.keyWCAs, WA.TS, WA.SN, WA.FloYIG, WA.FhiYIG, LA.VGP0, LA.VGP1 FROM WCAs AS WA
        LEFT JOIN WCAs AS WB ON WA.SN = WB.SN AND WB.keyWCAs > WA.keyWCAs
        LEFT JOIN LOParams AS LA ON LA.fkWCAs = WA.keyWCAs
        LEFT JOIN LOParams AS LB ON LA.fkWCAs = LB.fkWCAs AND LB.keyLOParams > LA.keyLOParams
        WHERE WB.keyWCAs IS NULL AND LB.keyLOParams IS NULL"""
        
        if keyWCAs:
            q += f" AND WA.keyWCAs = {keyWCAs}"

        if serialNum:
            q += f" AND WA.SN = '{serialNum}'"

        if serialNumLike:
            q += f" AND WA.SN LIKE '{serialNumLike}'"

        q += " ORDER BY WA.SN ASC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        
        return [WCA(
            key = row[0],
            timeStamp = makeTimeStamp(row[1]),
            serialNum = row[2],
            ytoLowGHz = row[3],
            ytoHighGHz = row[4],
            VGp0 = row[5] if row[5] else 0,
            VGp1 = row[6] if row[6] else 0
        ) for row in rows]
    