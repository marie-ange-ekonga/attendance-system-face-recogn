import sqlite3
import json
import os

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

tables = [
    'recognition_program',
    'recognition_course',
    'recognition_student',
    'recognition_courseenrollment',
    'recognition_session',
    'recognition_attendance',
    'recognition_justification',
    'recognition_log',
    'recognition_unknownface',
    'recognition_attendancechallenge',
]

data = {}
for table in tables:
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data[table] = [dict(row) for row in rows]
        print(f"Exported {len(rows)} rows from {table}")
    except sqlite3.OperationalError as e:
        print(f"Skipping {table}: {e}")

conn.close()

with open('exported_data.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print("Export complete. File: exported_data.json")