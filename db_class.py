import json
import pymysql
import sys

# Open database connection

class db:

    def __init__(self,config):
        
        self.host = config["db_host"]
        self.user = config["db_user"]
        self.password = config["db_password"]
        self.name = config["db_name"]
        self.conn = None

        self.open_connection()

    def open_connection(self):
        
        # Connect to MySQL Database

        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host,
                    user=self.user,
                    passwd=self.password,
                    connect_timeout=5,
                    cursorclass=pymysql.cursors.DictCursor # allow to access the rows using the column names as index
                )

        except pymysql.MySQLError as e:
            print(e)
            sys.exit()

        finally:
            print('Connection opened successfully.')

    def start(self):

        try:
            self.create_db()
            self.connect_db()
            #self.drop_tables()
            self.create_tables()
            #self.show_tables()
            #self.add_job("mi primer snippet")
            self.read_in()
            #self.read_out()
            return

        except Exception as e:
            print("Exeception occured:{}".format(e))
            sys.exit()

        #finally:
        #    self.conn.close()
    
    def add_job(self,snippet):

        cursor = self.conn.cursor()
        sql = "INSERT INTO `in` (snippet) VALUES (%s)"
        val = (snippet)
        cursor.execute(sql, val)

        self.conn.commit()

    def add_output(self,params):

        cursor = self.conn.cursor()
        sql = "INSERT INTO `out` (code,error_message,snippet,output_data) VALUES (%s,%s,%s,%s)"
        val = (params["code"],params["error_message"],params["snippet"],params["output_data"])
        cursor.execute(sql, val)

        self.conn.commit()

    def get_next_job(self):

        # Read IN jobs
        cursor = self.conn.cursor()
        sql = "SELECT * FROM `in` limit 1"
        cursor.execute(sql)

        row = cursor.fetchone()

        self.conn.commit()

        if row == None:
            return {"meta":{"code":200}}
        

        return {"meta":{"code":200},"job":row}
    
    def remove_job(self,id):
        
        # Remove IN job
        cursor = self.conn.cursor()
        sql = "DELETE FROM `in` where id = {}".format(id)
        cursor.execute(sql)

        self.conn.commit()

    def read_in(self):

        # Read IN jobs
        cursor = self.conn.cursor()
        sql = "SELECT * FROM `in`"
        cursor.execute(sql)

        rows = cursor.fetchall()       # return data from last query

        for row in rows:
            print(row)

    def read_out(self):

        # Read IN jobs
        cursor = self.conn.cursor()
        sql = "SELECT * FROM `out`"
        cursor.execute(sql)

        rows = cursor.fetchall()       # return data from last query

        for row in rows:
            print(row)

    def create_db(self):

        # Create a cursor object
        cursor = self.conn.cursor()                  
        cursor.execute("SET sql_notes = 0;") # Hide exists warning                
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.name))
    
    def connect_db(self):

        # Create a cursor object
        cursor = self.conn.cursor()                  
        cursor.execute("USE {}".format(self.name)) # select db
    
    def drop_tables(self):

        # Create a cursor object
        cursor = self.conn.cursor()  
        cursor.execute("SET sql_notes = 0; ")

        print("delete in")
        cursor.execute("DROP TABLE IF EXISTS `in`")

        print("delete out")
        cursor.execute("DROP TABLE IF EXISTS `out`")
        
        cursor.execute("SET sql_notes = 1; ")

    def create_tables(self):

        # Create a cursor object
        cursor = self.conn.cursor()  
        cursor.execute("SET sql_notes = 0; ")

        cursor.execute("""CREATE TABLE IF NOT EXISTS `in` (
            `id` int NOT NULL AUTO_INCREMENT,
            `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `snippet` TEXT,
            `input_data` TEXT,

            PRIMARY KEY (`id`)
            )
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS `out` (
            `id` int NOT NULL AUTO_INCREMENT,
            `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `code` int,
            `error_message` TEXT,
            `snippet` TEXT,
            `input_data` TEXT,

            `output_data` TEXT,
            PRIMARY KEY (`id`)
            )
        """)

        cursor.execute("SET sql_notes = 1; ")
    
    def show_tables(self):

        # Show tables
        cursor = self.conn.cursor()  
        
        cursor.execute("SHOW TABLES")

        tables = cursor.fetchall()

        for table, in tables:
            print("Table: {}".format(table))


