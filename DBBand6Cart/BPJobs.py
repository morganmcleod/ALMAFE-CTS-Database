from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.BPJob import BPJob, COLUMNS

class BPJobs():
    """
    Beam pattern jobs table in dbBand6Cart
    """
    
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, records: list[BPJob]) -> int:
        """ Insert records

        :param List[BPJob] records: to insert
        :return int: number of rows inserted
        """
        q = f"INSERT INTO BP_Jobs({','.join(COLUMNS[1:])}) VALUES "
        values = ""
        for rec in records:
            if values:
                values += ","
            values += "(" + rec.getInsertVals() + ")"
        
        q += values + ";"
        if self.DB.execute(q, commit = True):
            # TODO: use cursor.rowcount, move function to DriverMySQL
            return len(records)
        else:
            return 0
        
    def read(self, 
            fkCartTest: int = None, 
            fkBeamPattern: int = None,
            limit: int = None
        ) -> list[BPJob]:
        """ Read all records associated with a given cart test or scan

        :param int fkCartTest: cart test ID, optional
        :param int fkBeamPattern: individual scan, optional
        :param int limit: only the latest this many records
        :return list[BPJob]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM BP_Jobs as BJ"
        where = ""
        if fkCartTest is not None:
            q += " JOIN BeamPatterns AS BP ON BP.keyBeamPattern = BJ.PatternNum"
            where += f" BP.fkCartTest = {fkCartTest}"
        if fkBeamPattern is not None:            
            if where:
                where += " AND "
            where += f"BJ.PatternNum = {fkBeamPattern}"
        q += where + " ORDER BY BJ.PatternNum DESC"
        if limit:
            q += f" LIMIT {limit}"
        q += ";"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BPJob(
            key = row[0],
            fkBeamPattern = row[1],
            NFAmpPlot = row[2] if row[2] else "",
            NFPhasePlot = row[3] if row[3] else "",
            FFAmpPlot = row[4] if row[4] else "",
            FFPhasePlot = row[5] if row[5] else "",
            timeStamp = makeTimeStamp(row[6]) if row[6] else None,
            timeStampProcessed = makeTimeStamp(row[7]) if row[7] else None
        ) for row in rows]
    
    def update(self, record: BPJob) -> bool:
        """Update a record in the BP_Jobs table

        :param BPJob record: to be updated
        :return True if successful
        """
        ts = f"'{record.timeStamp}'" if record.timeStamp else "NULL"
        tsp = f"'{record.timeStampProcessed}'" if record.timeStampProcessed else "NULL"

        q = "UPDATE BP_Jobs SET "
        q += f"PatternNum = {record.fkBeamPattern}"
        q += f", FileName_NF_Amp_Plot = '{record.NFAmpPlot}'"
        q += f", FileName_NF_Phase_Plot = '{record.NFPhasePlot}'"
        q += f", FileName_FF_Amp_Plot = '{record.FFAmpPlot}'"
        q += f", FileName_FF_Phase_Plot = '{record.FFPhasePlot}'"
        q += f", TS={ts}"
        q += f", DateCompleted={tsp}"
        q += f" WHERE keyPatternJobs={record.key};"
        return self.DB.execute(q, commit = True)
