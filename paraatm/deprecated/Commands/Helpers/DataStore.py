import psycopg2
from psycopg2 import sql
import pandas as pd
from sqlalchemy import create_engine

try:
    import centaur
except ImportError:
    # Allow centaur to be optional
    pass

class dbError(Exception):
    def __init__(self):
        Exception.__init__(self,'empty query')

class Access:
    
    def __init__(self):
        self.connection = psycopg2.connect(database="paraatm", user="paraatm_user", password="paraatm_user", host="localhost", port="5432")
        # See pyscopg documentation: autocommit is recommended for "long lived scripts"
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        
    def getAirportLocation(self, airportCode):
        self.cursor.execute("SELECT * FROM airports WHERE iata = %s", ("" + airportCode,))
        results = self.cursor.fetchall()
        latitude = results[0][1]
        longitude = results[0][2]
        return latitude, longitude
        
    def getFlightHistory(self, callsign):
        self.cursor.execute("SELECT * FROM flight_data WHERE callsign = %s", ("" + callsign,))
        results = self.cursor.fetchall()
        return results

    def tableExists(self, table_name):
        """Check whether a table exists in the database"""
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = %s)", (table_name,))
        return self.cursor.fetchone()[0]
    
    def addTable(self, name, data, **kwargs):
        if not self.tableExists(name):
            engine = create_engine('postgresql://paraatm_user:paraatm_user@localhost:5432/paraatm')
            data.to_sql(name, engine, **kwargs)

    def readTable(self, table, **kwargs):
        engine = create_engine('postgresql://paraatm_user:paraatm_user@localhost:5432/paraatm')
        return pd.read_sql_table(table, engine, **kwargs)

    def dropTable(self, table):
        self.cursor.execute(sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table)))

    def getIFFdata(self, filename, **kwargs):
        query = "SELECT * FROM \"%s\""%filename
        conditions = []
        for k,v in kwargs.items():
            conditions.append("%s='%s'"%(k,v))
        if kwargs:
            query += " WHERE "
            query += " AND ".join(conditions)
        self.cursor.execute(query)
        if bool(self.cursor.rowcount):
            results = pd.DataFrame(self.cursor.fetchall())
            results.columns = ['id','time','callsign','origin','destination','latitude','longitude','altitude','rocd','tas','heading','status']
            del results['id']
            results[['latitude','longitude','altitude','heading']] = results[['latitude','longitude','altitude','heading']].replace(r'[^0-9,.,-]+','0',regex=True)
            results[['latitude','longitude','altitude','heading']] = results[['latitude','longitude','altitude','heading']].astype(float)
            results['status'] = results['status'].fillna('TAKEOFF/LANDING')
            results = results[results['latitude'] != -100]
            return ['readIFF', results, filename]
        else: raise dbError

    def getNATSdata(self, filename, **kwargs):
        query = "SELECT * FROM \"%s\""%filename
        conditions = []
        for k,v in kwargs.items():
            conditions.append("%s='%s'"%(k,v))
        if kwargs:
            query += " WHERE "
            query += " AND ".join(conditions)
        self.cursor.execute(query)
        if bool(self.cursor.rowcount):
            results = pd.DataFrame(self.cursor.fetchall())
            results.columns = ['id','time','callsign','origin','destination','latitude','longitude','altitude','rocd','tas','heading','sector','status']
            del results['id']
            del results['sector']
            return ['readNATS',results,filename]
        else: raise dbError

    def getSMESData(self, airport):
        self.cursor.execute("SELECT * FROM smes WHERE airport = %s" %airport)
        if bool(self.cursor.rowcount):
            results = self.cursor.fetchall()
            return results
        else: raise dbError

    def getCentaurDist(self,table='distributionDB',key=''):
        """
        get the distribution of reaction times for a given subject
        args:
            table (str): table name
            key (str): the primary key of the table
        returns:
            dist_type (str),
            loc (float),
            scale (float),
            args (list)
        """

        self.cursor.execute("SELECT * FROM %s WHERE variable='%s'"%(table,key))
        #self.cursor.execute("SELECT * FROM %s_uncertainty WHERE state='%s'"
        #        %(table.lower(),key.lower()))
        results = self.cursor.fetchall()[0]
        index,dist_type,params = results
        params = params.split(',')
        args = [float(p) for p in params[:-2]]
        scale = float(params[-1])
        loc = float(params[-2])

        rv=centaur.Distribution()

        getattr(rv,'new_%s'%dist_type)(loc,scale,*args)
        return rv
