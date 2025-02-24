#!/usr/bin/env python3

import csv
import sqlite3
import sys
import os

def csv_to_sqlite(db_name, csv_file):
    # Get the table name from the CSV filename (without extension)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Read the CSV file to get headers and data
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader)  # Get the header row
        
        # Create the database and table
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create table with columns from CSV headers
        # Assuming all columns are TEXT for simplicity
        columns = ','.join([f'{header} TEXT' for header in headers])
        cursor.execute(f'CREATE TABLE {table_name} ({columns})')
        
        # Prepare the INSERT statement
        placeholders = ','.join(['?' for _ in headers])
        insert_query = f'INSERT INTO {table_name} VALUES ({placeholders})'
        
        # Insert all rows
        cursor.executemany(insert_query, csv_reader)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_sqlite.py <database_name> <csv_file>")
        sys.exit(1)
        
    db_name = sys.argv[1]
    csv_file = sys.argv[2]
    
    try:
        csv_to_sqlite(db_name, csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find CSV file '{csv_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
