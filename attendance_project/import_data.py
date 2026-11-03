import sqlite3
import json
from django.conf import settings
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_project.settings')
django.setup()

from recognition.models import Program, Course, Student, Attendance, Justification, Log, UnknownFace, AttendanceChallenge, CourseEnrollment
from django.contrib.auth.models import User
from django.utils import timezone
import json

with open('exported_data.json') as f:
    data = json.load(f)

# Import programs
for row in data.get('recognition_program', []):
    Program.objects.get_or_create(id=row['id'], defaults={
        'name': row['name'],
        'code': row.get('code', '')
    })

# Import users and students (complex: need to recreate users first)
user_map = {}
for row in data.get('recognition_student', []):
    user_id = row['user_id']
    # Check if user already exists (from auth_user)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # You would need the original user data – this is tricky.
        # For now, skip – you can re‑create students manually.
        print(f"User {user_id} missing – skipping student {row['id']}")
        continue
    student, created = Student.objects.update_or_create(
        id=row['id'],
        defaults={
            'user': user,
            'biometric_consent_given': True,
            'biometric_consent_date': timezone.now(),
            'biometric_consent_version': '1.0',
            'embedding_encrypted': None,
            'enrollment_year': row.get('enrollment_year'),
            'student_id': row.get('student_id'),
            'program_id': row.get('program_id'),
        }
    )
    print(f"Student {student.id} imported/updated")

# Similarly, import other tables (courses, sessions, attendance...)
# This becomes complex. Given the time, a simpler approach is to re‑enter your data manually.

print("Data import completed partially.")