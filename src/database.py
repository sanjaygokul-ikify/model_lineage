def get_connection(backend='sqlite', **config):
    if backend == 'sqlite':
        import sqlite3
        path = config.get('path', 'model_lineage.db')
        conn = sqlite3.connect(path)
        return conn, conn.cursor()
    elif backend == 'mysql':
        import mysql.connector
        conn = mysql.connector.connect(
            host=config.get('host', 'localhost'),
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=config.get('port', 3306)
        )
        return conn, conn.cursor()
    else:
        raise ValueError(f"Unsupported backend: '{backend}'. Choose 'sqlite' or 'mysql'.")
