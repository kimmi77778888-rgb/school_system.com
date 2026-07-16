"""
Fix the parent registration database constraint.
This script removes the UNIQUE constraint on UserProfile.student_id
to allow multiple parents (mom and dad) to register for the same child.

Run this script BEFORE trying to register a second parent for a child.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db import connection

def fix_parent_constraint():
    """Remove the unique constraint on student_id in UserProfile"""
    
    with connection.cursor() as cursor:
        print("🔧 Fixing parent registration database constraint...")
        
        # Check what constraints exist
        cursor.execute("""
            SELECT constraint_name, constraint_type 
            FROM information_schema.table_constraints 
            WHERE table_name = 'school_userprofile'
            AND constraint_type = 'UNIQUE';
        """)
        
        constraints = cursor.fetchall()
        print(f"\n📋 Found {len(constraints)} unique constraints:")
        for constraint_name, constraint_type in constraints:
            print(f"   - {constraint_name} ({constraint_type})")
        
        # Drop the unique constraint on student_id
        try:
            cursor.execute("""
                ALTER TABLE school_userprofile 
                DROP CONSTRAINT IF EXISTS school_userprofile_student_id_key;
            """)
            print("\n✅ Successfully removed unique constraint on student_id")
        except Exception as e:
            print(f"\n❌ Error removing constraint: {e}")
            return False
        
        # Create a regular index for performance (optional)
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS school_userprofile_student_id_idx 
                ON school_userprofile(student_id);
            """)
            print("✅ Created performance index on student_id")
        except Exception as e:
            print(f"⚠️  Warning creating index: {e}")
        
        # Verify the change
        cursor.execute("""
            SELECT constraint_name, constraint_type 
            FROM information_schema.table_constraints 
            WHERE table_name = 'school_userprofile'
            AND constraint_type = 'UNIQUE';
        """)
        
        remaining = cursor.fetchall()
        print(f"\n📋 Remaining unique constraints: {len(remaining)}")
        for constraint_name, constraint_type in remaining:
            print(f"   - {constraint_name} ({constraint_type})")
        
        print("\n🎉 Database fix complete! Multiple parents can now register for the same child.")
        return True

if __name__ == '__main__':
    try:
        fix_parent_constraint()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you're running this with the correct Python environment")
        print("and that the database is accessible.")
