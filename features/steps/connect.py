import pypyodbc

class connection(object):
    def __init__(self):
        self.fn = None

    def makeconnection(self,query):
        connect = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                           "Server=ATLANTA1040-02\SQLEXPRESS;"
                                           "Database=sample;"
                                           "Trusted_Connection=yes;")

        cursor = connect.cursor()
        cursor.execute(query)
        result=cursor.fetchone()
        while result:
            #print(result[0])
            return result[0]
        result=cursor.fetchone()
        connect.commit()
        connect.close()

        return connect

    """" if __name__=="__main__":
        makeconnection(self)"""
