#!/usr/bin/env python3
"""
Test script to verify UUID serialization works correctly.
"""

import sys
import os
import asyncio
import json
import uuid

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgresql_db import serialize_db_row, serialize_db_rows
from database.json_encoder import PostgreSQLJSONEncoder, serialize_for_json, safe_json_response

def test_uuid_serialization():
    """Test UUID serialization functions"""
    print("Testing UUID serialization...")
    
    # Test data with UUIDs
    test_uuid = uuid.uuid4()
    test_data = {
        'id': test_uuid,
        'name': 'Test User',
        'metadata': {'role': 'user', 'active': True},
        'userId': uuid.uuid4()
    }
    
    print(f"Original data: {test_data}")
    print(f"UUID type: {type(test_data['id'])}")
    
    # Test serialize_db_row function
    serialized = serialize_db_row(test_data)
    print(f"Serialized data: {serialized}")
    print(f"Serialized UUID type: {type(serialized['id'])}")
    
    # Test JSON encoding
    try:
        json_str = json.dumps(serialized)
        print(f"JSON string: {json_str}")
        print("✅ JSON serialization successful!")
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
    
    # Test custom encoder
    try:
        json_str = json.dumps(test_data, cls=PostgreSQLJSONEncoder)
        print(f"Custom encoder JSON: {json_str}")
        print("✅ Custom encoder successful!")
    except Exception as e:
        print(f"❌ Custom encoder failed: {e}")
    
    # Test serialize_for_json function
    try:
        safe_data = serialize_for_json(test_data)
        json_str = json.dumps(safe_data)
        print(f"serialize_for_json result: {json_str}")
        print("✅ serialize_for_json successful!")
    except Exception as e:
        print(f"❌ serialize_for_json failed: {e}")
    
    # Test safe_json_response function
    try:
        safe_data = safe_json_response(test_data)
        json_str = json.dumps(safe_data)
        print(f"safe_json_response result: {json_str}")
        print("✅ safe_json_response successful!")
    except Exception as e:
        print(f"❌ safe_json_response failed: {e}")

def test_list_serialization():
    """Test serialization of lists with UUIDs"""
    print("\nTesting list serialization...")
    
    test_list = [
        {'id': uuid.uuid4(), 'name': 'User 1'},
        {'id': uuid.uuid4(), 'name': 'User 2'},
        {'id': uuid.uuid4(), 'name': 'User 3'}
    ]
    
    print(f"Original list: {test_list}")
    
    # Test serialize_db_rows function
    serialized_list = serialize_db_rows(test_list)
    print(f"Serialized list: {serialized_list}")
    
    # Test JSON encoding
    try:
        json_str = json.dumps(serialized_list)
        print(f"JSON string: {json_str}")
        print("✅ List JSON serialization successful!")
    except Exception as e:
        print(f"❌ List JSON serialization failed: {e}")

async def test_database_connection():
    """Test actual database connection if available"""
    print("\nTesting database connection...")
    
    try:
        from database.postgresql_db import db
        
        await db.connect()
        print("✅ Database connection successful!")
        
        # Test _all_users method
        users = await db._all_users()
        print(f"Retrieved {len(users)} users")
        
        if users:
            print("Sample user:", users[0])
            # Test JSON serialization of actual data
            json_str = json.dumps(users[0])
            print("✅ User data JSON serialization successful!")
        
        await db.disconnect()
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("This is expected if database is not running or configured")

if __name__ == "__main__":
    print("UUID Serialization Test")
    print("=" * 40)
    
    # Test basic serialization
    test_uuid_serialization()
    test_list_serialization()
    
    # Test database connection
    try:
        asyncio.run(test_database_connection())
    except Exception as e:
        print(f"Database test skipped: {e}")
    
    print("\n" + "=" * 40)
    print("Test completed!")
