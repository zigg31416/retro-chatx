import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize and return Supabase client"""
    # First try to get from environment variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # If not found, try to get from Streamlit secrets
    if not url or not key:
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except:
            st.error("Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in your secrets or environment variables.")
            st.stop()
    
    return create_client(url, key)

# Create a function to get a singleton Supabase client
@st.cache_resource
def get_supabase_client():
    return init_supabase()

# Database interaction functions
def create_chatroom(name, host_name):
    """Create a new chatroom and return its code and ID"""
    client = get_supabase_client()
    import random
    
    # Generate a random 5-digit code
    code = str(random.randint(10000, 99999))
    
    # Insert into database
    data = {
        "name": name,
        "code": code,
        "host_name": host_name,
        "is_active": True
    }
    
    response = client.table("chatrooms").insert(data).execute()
    
    # Return the code and id if successful
    if response.data:
        return {
            "success": True,
            "code": code,
            "id": response.data[0]["id"]
        }
    else:
        return {
            "success": False,
            "error": "Failed to create chatroom"
        }

def get_chatroom_by_code(code):
    """Retrieve a chatroom by its code"""
    client = get_supabase_client()
    
    response = client.table("chatrooms").select("*").eq("code", code).eq("is_active", True).execute()
    
    if response.data and len(response.data) > 0:
        return {
            "success": True,
            "chatroom": response.data[0]
        }
    else:
        return {
            "success": False,
            "error": "Chatroom not found or inactive"
        }

def join_request(chatroom_id, username):
    """Create a join request for a user"""
    client = get_supabase_client()
    
    data = {
        "chatroom_id": chatroom_id,
        "username": username,
        "status": "pending"  # pending, approved, rejected
    }
    
    response = client.table("join_requests").insert(data).execute()
    
    if response.data:
        return {
            "success": True,
            "request_id": response.data[0]["id"]
        }
    else:
        return {
            "success": False,
            "error": "Failed to create join request"
        }

def get_pending_requests(chatroom_id):
    """Get all pending join requests for a chatroom"""
    client = get_supabase_client()
    
    response = client.table("join_requests").select("*").eq("chatroom_id", chatroom_id).eq("status", "pending").execute()
    
    return response.data if response.data else []

def update_request_status(request_id, status):
    """Update the status of a join request"""
    client = get_supabase_client()
    
    response = client.table("join_requests").update({"status": status}).eq("id", request_id).execute()
    
    return response.data if response.data else None

def send_message(chatroom_id, username, content, message_type="user"):
    """Send a message to a chatroom"""
    client = get_supabase_client()
    
    data = {
        "chatroom_id": chatroom_id,
        "username": username,
        "content": content,
        "type": message_type  # user, system
    }
    
    response = client.table("messages").insert(data).execute()
    
    return response.data if response.data else None

def get_messages(chatroom_id, limit=50):
    """Get messages for a chatroom"""
    client = get_supabase_client()
    
    response = client.table("messages").select("*").eq("chatroom_id", chatroom_id).order("created_at", desc=False).limit(limit).execute()
    
    return response.data if response.data else []

def close_chatroom(chatroom_id):
    """Mark a chatroom as inactive"""
    client = get_supabase_client()
    
    response = client.table("chatrooms").update({"is_active": False}).eq("id", chatroom_id).execute()
    
    return response.data if response.data else None

def subscribe_to_messages(chatroom_id, callback):
    """Subscribe to new messages in a chatroom"""
    client = get_supabase_client()
    
    # Set up a subscription channel
    channel = client.channel(f'chatroom-{chatroom_id}')
    
    # Listen for INSERT events on the messages table
    channel.on(
        'postgres_changes',
        {
            'event': 'INSERT',
            'schema': 'public',
            'table': 'messages',
            'filter': f'chatroom_id=eq.{chatroom_id}'
        },
        callback
    )
    
    # Subscribe to the channel
    channel.subscribe()
    
    return channel

def subscribe_to_join_requests(chatroom_id, callback):
    """Subscribe to new join requests for a chatroom"""
    client = get_supabase_client()
    
    # Set up a subscription channel
    channel = client.channel(f'join-requests-{chatroom_id}')
    
    # Listen for INSERT events on the join_requests table
    channel.on(
        'postgres_changes',
        {
            'event': 'INSERT',
            'schema': 'public',
            'table': 'join_requests',
            'filter': f'chatroom_id=eq.{chatroom_id} AND status=eq.pending'
        },
        callback
    )
    
    # Subscribe to the channel
    channel.subscribe()
    
    return channel
