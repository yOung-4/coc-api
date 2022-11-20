import psycopg2

class db():
    conn = psycopg2.connect('dbname=api user=web password=kokodayo host=192.168.1.10 port=5432')

    def create(self,):
        cur = self.conn.cursor()
        return cur

    def commit(self, cur):
        cur.close
        self.conn.commit()

    def close(self, ):
        self.conn.close()