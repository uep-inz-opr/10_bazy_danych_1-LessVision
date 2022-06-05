import csv, sqlite3
sqlite_con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) 
cur = sqlite_con.cursor()

cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
                  to_subscriber data_type INTEGER, 
                  datetime data_type timestamp, 
                  duration data_type INTEGER , 
                  celltower data_type INTEGER);''') 

with open('polaczenia_duze.csv','r') as fin: 
    reader = csv.reader(fin, delimiter = ";")
    next(reader, None)  
    rows = [x for x in reader]
    cur.executemany("INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration , celltower) VALUES (?, ?, ?, ?, ?);", rows)
    sqlite_con.commit()

class ReportGenerator:
  def __init__(self,connection, escape_string = "(%s)"):
    self.connection = connection
    self.report_text = None
    self.escape_string = escape_string

  def generate_report(self, user_id):
    cursor = self.connection.cursor()
    sql_query = f"Select sum(duration) from polaczenia where from_subscriber ={self.escape_string}"
    args = (user_id,)
    cursor.execute(sql_query, args)
    result = cursor.fetchone()[0]
    self.report_text = f"Łączny czas trwania dla użytkownika {user_id} to {result}"

  def get_report(self):	
    return self.report_text

suma = 0

if __name__ == '__main__':
    cursor = sqlite_con.cursor()
    cursor.execute("Select sum(duration) from polaczenia;")
    result = cursor.fetchall()
    #print(result[0])
    for row in result:
        print(row[0])
