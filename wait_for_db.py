import sys
import time
import psycopg2


def wait_for_postgres(
        host,
        port,
        user,
        password,
        database,
        max_attempts=30,
        delay_seconds=2
):
    attempts = 0
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            conn.close()
            print("PostgreSQL is ready.")
            return
        except psycopg2.OperationalError:
            attempts += 1
            print(f"PostgreSQL connection attempt {attempts}/{max_attempts} failed. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)

    print("Max connection attempts reached. Exiting...")
    sys.exit(1)


if __name__ == "__main__":
    host = "db"
    port = 5432
    user = "postgres"
    password = "postgres"
    database = "cars"

    wait_for_postgres(host, port, user, password, database)
