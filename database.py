import sqlite3
import pandas as pd

# Database file name
DB_NAME = "nafas.db"

# CSV files and their corresponding table names
csv_files = {
    "aqi_yearly_state.csv": "aqi_yearly_state",
    "combined_aqi_data.csv": "combined_aqi_data",
    "combined_weather_data.csv": "combined_weather_data",
    "prevalence_incidence_asthma.csv": "prevalence_incidence_asthma"
}

# Define table schemas
table_schemas = {
    "aqi_yearly_state": """
        CREATE TABLE IF NOT EXISTS aqi_yearly_state (
            state_id INTEGER,
            year INTEGER,
            state TEXT,
            aqi REAL
        );
    """,
    "combined_aqi_data": """
        CREATE TABLE IF NOT EXISTS combined_aqi_data (
            state_id INTEGER,
            state TEXT,
            city TEXT,
            date TEXT,
            aqi REAL
        );
    """,
    "combined_weather_data": """
        CREATE TABLE IF NOT EXISTS combined_weather_data (
            state_id INTEGER,
            state TEXT,
            city TEXT,
            date TEXT,
            temp REAL
        );
    """,
    "prevalence_incidence_asthma": """
        CREATE TABLE IF NOT EXISTS prevalence_incidence_asthma (
            measure_id INTEGER,
            measure_name TEXT,
            location_id INTEGER,
            location_name TEXT,
            sex_id INTEGER,
            sex_name TEXT,
            age_id INTEGER,
            age_name TEXT,
            cause_id INTEGER,
            cause_name TEXT,
            metric_id INTEGER,
            metric_name TEXT,
            year INTEGER,
            val REAL,
            upper REAL,
            lower REAL
        );
    """
}

def create_database():
    """Creates the SQLite database and tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for table_name, schema in table_schemas.items():
        cursor.execute(schema)
        print(f"Table '{table_name}' created (if not exists).")
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

def import_csv_to_db():
    """Imports CSV files into the SQLite database."""
    conn = sqlite3.connect(DB_NAME)

    for csv_file, table_name in csv_files.items():
        try:
            # Load CSV into DataFrame
            df = pd.read_csv(csv_file)

            # Insert into the database
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Imported {csv_file} into '{table_name}' table.")

        except Exception as e:
            print(f"Error importing {csv_file}: {e}")

    conn.close()
    print("All CSV files imported successfully.")

if __name__ == "__main__":
    create_database()
    import_csv_to_db()
