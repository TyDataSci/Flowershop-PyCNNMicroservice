import psycopg2
import os

host = 'foreveryours-db.cie6oavuia6e.us-east-2.rds.amazonaws.com'
dbname = 'initial_db'
port = '5432'
password = os.environ.get('DB_PASS')
user = 'root'


def connect():
    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()
    print("Opened connection successfully")
    return conn, cur


def close(conn, cur):
    try:
        cur.close()
        conn.close()
    finally:
        if conn:
            conn.close()
    print("Closed connection successfully")


def create_stock_id():
    try:
        conn, cur = connect()
        stock_id = 0
        statement = 'INSERT INTO stock (id) values ((SELECT MAX(id)+1 FROM stock)) RETURNING id;'
        print(statement)
        cur.execute(statement)
        stock_id = cur.fetchone()[0]
        print(f'Stock ID {stock_id} created successful')
    except Exception as e:
        print(f'Error {e}')
    finally:
        close(conn, cur)
        return stock_id


def insert_stock_type_status(response):
    try:
        conn, cur = connect()
        stock_id = create_stock_id()
        if stock_id != 0:
            for stock in response:
                statement = f'''INSERT INTO stock_type_status (stockid, typeid, status, image) values '''
                f_type = stock.get('type')
                status = stock.get('status')
                image = stock.get('image')
                value = '\n(%s, (SELECT id FROM types WHERE name =%s),%s,%s)'
                statement = statement + value
                cur.execute(statement, [stock_id, f_type, status, image])
                print(statement)
            print('Insert Successful')
    except Exception as e:
        print(f'Error {e}')
    finally:
        close(conn, cur)


def get_last_stock():
    try:
        response = []
        conn, cur = connect()
        query = '''SELECT t.name, ss.status, ss.image
                FROM stock_type_status ss
                JOIN types t ON t.id = ss.typeid
                WHERE ss.stockid = (SELECT MAX(id) from stock)'''
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            row_dict = {'type': row[0], 'status': row[1], 'image': row[2]}
            response.append(row_dict)

        print('Returned last stock successfully')
    except Exception as e:
        print(f'Error {e}')
    finally:
        close(conn, cur)
        return response
