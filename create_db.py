import sqlite3
import os

print("Running create_db.py!")

# Define file paths relative to the script's directory
fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# Paths for SQLite database and SQL files
sqliteDbPath = getPath("gym.db")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("insert_data.sql")

# Function to reset the database
def resetDatabase():
    # Erase previous database
    if os.path.exists(sqliteDbPath):
        os.remove(sqliteDbPath)
        print("Old database removed.")
    else:
        print("No existing database found.")

    # Create a new database
    conn = sqlite3.connect(sqliteDbPath)
    cursor = conn.cursor()

    # Load and execute schema and data scripts
    with (
        open(setupSqlPath, "r") as schema_file,
        open(setupSqlDataPath, "r") as seed_file
    ):
        setupSqlScript = schema_file.read()
        setupSqlDataScript = seed_file.read()

    cursor.executescript(setupSqlScript)  # Create tables and keys
    print("Schema setup complete.")

    cursor.executescript(setupSqlDataScript)  # Insert initial data
    print("Data insertion complete.")

    conn.commit()
    conn.close()
    print("Database setup complete!")


if __name__ == "__main__":
    resetDatabase()  # Initialize/reset the database
