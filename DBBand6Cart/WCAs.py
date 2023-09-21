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
        q = f"SELECT {','.join(COLUMNS)} FROM WCAs"
        where = ""
        
        if keyWCAs:
            if where:
                where += " AND "
            where += f"keyWCAs = {keyWCAs}"

        if serialNum:
            if where:
                where += " AND "
            where += f"SN = '{serialNum}'"

        if serialNumLike:
            if where:
                where += " AND "
            where += f"SN LIKE '{serialNumLike}'"

        if where:
            q += " WHERE " + where
        q += " ORDER BY SN ASC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        
        unique = {}
        for row in rows:
            if row[2] not in unique.keys():
                unique[row[2]] = WCA(
                    key = row[0],
                    timeStamp = makeTimeStamp(row[1]),
                    serialNum = row[2],
                    ytoLowGHz = row[3],
                    ytoHighGHz = row[4]
                )
        return [unique[sn] for sn in unique.keys()]
    