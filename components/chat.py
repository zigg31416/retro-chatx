import streamlit as st
import time
from utils.supabase_client import send_message, get_messages, close_chatroom, subscribe_to_messages
from utils.ui_elements import (
    display_title, 
    display_room_code, 
    display_chat_message, 
    play_sound, 
    add_dynamic_effects,
    create_animated_typing,
    add_random_visual_glitches
)
from components.host import handle_join_requests

def chat_interface():
    """Enhanced chat interface with motion graphics"""
    # Add dynamic background effects
    add_dynamic_effects()
    add_random_visual_glitches()
    
    # Check if user is in a room
    if "room_id" not in st.session_state:
        st.session_state.page = "home"
        st.experimental_rerun()
        return
    
    # Display chat header with enhanced animations
    room_name = st.session_state.room_name
    username = st.session_state.username
    is_host = st.session_state.get("is_host", False)
    
    header_suffix = " (HOST)" if is_host else ""
    display_title(f"CHATROOM: {room_name}", f"Logged in as: {username}{header_suffix}", animation_type="rainbow")
    
    # If host, display the room code for sharing with enhanced effect
    if is_host:
        display_room_code(st.session_state.room_code)
    
    # Handle join requests if host with animated notification
    if is_host:
        handle_join_requests()
    
    # Layout chat area and input with improved visuals
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        # Enhanced buttons with hover effects
        st.markdown("""
        <style>
        .control-panel {
            background-color: rgba(0, 0, 0, 0.7);
            border: 2px solid #ff00c1;
            padding: 15px;
            margin: 10px 0;
        }
        
        .control-title {
            color: #00fff9;
            text-align: center;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.8rem;
            margin-bottom: 10px;
            text-shadow: 0 0 5px #00fff9;
        }
        </style>
        
        <div class="control-panel container-scan">
            <div class="control-title cyan-pulse">CONTROLS</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("REFRESH", key="refresh_btn"):
            # Add visual feedback
            st.markdown(
                """
                <script>
                // Create flash effect for refresh
                let flash = document.createElement('div');
                flash.style.position = 'fixed';
                flash.style.top = '0';
                flash.style.left = '0';
                flash.style.width = '100%';
                flash.style.height = '100%';
                flash.style.backgroundColor = 'rgba(0, 255, 249, 0.1)';
                flash.style.zIndex = '9999';
                flash.style.pointerEvents = 'none';
                document.body.appendChild(flash);
                
                // Remove flash effect
                setTimeout(() => {
                    document.body.removeChild(flash);
                }, 100);
                </script>
                """,
                unsafe_allow_html=True
            )
            st.experimental_rerun()
        
        if st.button("EXIT CHATROOM", key="exit_btn"):
            # Add exit effect
            st.markdown(
                """
                <script>
                // More dramatic transition for exit
                let container = document.createElement('div');
                container.style.position = 'fixed';
                container.style.top = '0';
                container.style.left = '0';
                container.style.width = '100%';
                container.style.height = '100%';
                container.style.backgroundColor = 'black';
                container.style.zIndex = '9999';
                container.classList.add('crt-off');
                document.body.appendChild(container);
                </script>
                """,
                unsafe_allow_html=True
            )
            exit_chat()
            st.experimental_rerun()
        
        if is_host:
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            if st.button("CLOSE CHATROOM", key="close_btn", help="This will end the chat for all users"):
                # Add dramatic shutdown effect
                st.markdown(
                    """
                    <script>
                    // Create static noise effect
                    function createStaticNoise() {
                        let container = document.createElement('div');
                        container.style.position = 'fixed';
                        container.style.top = '0';
                        container.style.left = '0';
                        container.style.width = '100%';
                        container.style.height = '100%';
                        container.style.backgroundColor = 'black';
                        container.style.zIndex = '9999';
                        container.style.opacity = '0';
                        document.body.appendChild(container);
                        
                        // Fade in with static
                        let opacity = 0;
                        let fadeIn = setInterval(() => {
                            opacity += 0.05;
                            container.style.opacity = opacity;
                            
                            // Add random static pixels
                            let pixels = '';
                            for (let i = 0; i < 100; i++) {
                                const x = Math.floor(Math.random() * 100);
                                const y = Math.floor(Math.random() * 100);
                                const color = Math.random() > 0.5 ? '#fff' : '#000';
                                pixels += `<div style="position:absolute;left:${x}%;top:${y}%;width:3px;height:3px;background:${color};"></div>`;
                            }
                            container.innerHTML = pixels;
                            
                            if (opacity >= 1) {
                                clearInterval(fadeIn);
                            }
                        }, 50);
                    }
                    
                    createStaticNoise();
                    </script>
                    """,
                    unsafe_allow_html=True
                )
                close_chat()
                st.experimental_rerun()
        
        # Add chat stats with animation
        st.markdown(
            """
            <div class="control-panel container-scan">
                <div class="control-title lime-pulse">STATS</div>
                <div style="font-family: 'VT323', monospace; color: #adff2f; text-shadow: 0 0 5px #adff2f;">
                    <div>USERS: <span id="users-count">1</span></div>
                    <div>UPTIME: <span id="uptime">00:00</span></div>
                </div>
            </div>
            
            <script>
            // Simulate uptime counter
            let seconds = 0;
            setInterval(() => {
                seconds++;
                const mins = Math.floor(seconds / 60);
                const secs = seconds % 60;
                document.getElementById('uptime').innerText = 
                    String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
            }, 1000);
            </script>
            """,
            unsafe_allow_html=True
        )
    
    with col1:
        # Enhanced chat container with visual effects
        st.markdown(
            """
            <style>
            .retro-chat-container {
                background-color: rgba(0, 0, 0, 0.8);
                border: 3px solid #ff00c1;
                border-radius: 0;
                box-shadow: 0 0 10px #ff00c1, 0 0 20px #ff00c1;
                padding: 20px;
                margin: 20px 0;
                height: 400px;
                overflow-y: auto;
                position: relative;
            }
            
            .scanline {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: rgba(255, 255, 255, 0.05);
                animation: scanline 8s linear infinite;
                pointer-events: none;
            }
            
            .message-typing-indicator {
                color: #00fff9;
                font-family: 'VT323', monospace;
                font-size: 1rem;
                animation: blink 1s infinite;
                padding: 5px;
            }
            
            .message-input-container {
                background-color: rgba(0, 0, 0, 0.7);
                border: 2px solid #00fff9;
                padding: 10px;
                position: relative;
                display: flex;
                align-items: center;
            }
            
            .message-send-button {
                font-family: 'Press Start 2P', cursive !important;
                background: black !important;
                color: #adff2f !important;
                border: 2px solid #adff2f !important;
                border-radius: 0 !important;
                box-shadow: 0 0 5px #adff2f !important;
                padding: 8px 16px !important;
                transition: all 0.3s !important;
                text-transform: uppercase !important;
                margin-left: 10px !important;
            }
            
            .message-send-button:hover {
                background: #adff2f !important;
                color: black !important;
                box-shadow: 0 0 10px #adff2f, 0 0 20px #adff2f !important;
            }
            </style>
            
            <div class="retro-chat-container container-scan" id="chat-container">
                <div class="scanline"></div>
            """,
            unsafe_allow_html=True
        )
        
        # Get messages from Supabase
        messages = get_messages(st.session_state.room_id) if "room_id" in st.session_state else []
        
        # For demo purposes, create some sample messages if none exist
        if not messages:
            messages = [
                {"username": "SYSTEM", "content": "Welcome to RETRO CHAT", "type": "system"},
                {"username": username, "content": "Hello, this is a sample message from me!", "type": "user"},
                {"username": "PIXEL_PUNK", "content": "Hey there! Nice retro vibes in here!", "type": "user"},
                {"username": "SYSTEM", "content": "PIXEL_PUNK has joined the chatroom", "type": "system"}
            ]
        
        # Initialize message count for notification
        if "message_count" not in st.session_state:
            st.session_state.message_count = len(messages)
        
        # Display messages with animation
        for i, msg in enumerate(messages):
            display_chat_message(
                msg["username"], 
                msg["content"], 
                msg["type"], 
                st.session_state.username,
                animate=(i >= st.session_state.message_count)  # Only animate new messages
            )
        
        # Check for new messages and play sound
        if len(messages) > st.session_state.message_count:
            play_sound("message")
        
        st.session_state.message_count = len(messages)
        
        # Close the chat container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Message input with typing animation
        st.markdown(
            """
            <div class="message-input-container container-scan">
                <div class="scanline"></div>
                <div style="flex-grow: 1;">
            """, 
            unsafe_allow_html=True
        )
        
        # Create columns for input and send button
        input_col, button_col = st.columns([5, 1])
        
        with input_col:
            message = st.text_input("", key="message_input", placeholder="TYPE YOUR MESSAGE HERE...")
        
        with button_col:
            send_button = st.button("SEND", key="send_btn")
        
        # Close the message input container
        st.markdown(
            """
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # If send button clicked or Enter pressed
        if send_button or message:
            if message:
                # Send message to Supabase in production
                # For demo, just show typing animation
                st.markdown(
                    f"""
                    <div class="message-typing-indicator">
                        Sending message...
                    </div>
                    
                    <script>
                    // Scroll to bottom of chat
                    function scrollToBottom() {{
                        const chatContainer = document.getElementById('chat-container');
                        if (chatContainer) {{
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }}
                    }}
                    
                    // Call on load and set interval to check for new content
                    window.addEventListener('load', scrollToBottom);
                    setInterval(scrollToBottom, 500);
                    </script>
                    """,
                    unsafe_allow_html=True
                )
                
                # In production, you'd do:
                # send_message(st.session_state.room_id, st.session_state.username, message)
                
                # Clear input
                st.session_state.message_input = ""
                
                # In production, rerun to update chat
                # st.experimental_rerun()
    
    # Add automatic scrolling for chat container
    st.markdown(
        """
        <script>
        // Auto-scroll chat to bottom
        function scrollChatToBottom() {
            const chatContainer = document.getElementById('chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
        
        // Call on load and set interval to check for new content
        window.addEventListener('load', scrollChatToBottom);
        setInterval(scrollChatToBottom, 500);
        
        // Add keyboard shortcut (Enter to send)
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                const sendButton = document.querySelector('button[data-testid="stButton"]:contains("SEND")');
                if (sendButton) {
                    sendButton.click();
                }
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )

def exit_chat():
    """Exit the current chatroom with animation effects"""
    room_id = st.session_state.get("room_id")
    username = st.session_state.get("username")
    
    if room_id and username:
        # Send exit message
        # send_message(room_id, "SYSTEM", f"{username} has left the chatroom", "system")
        pass
    
    # Clear chatroom data from session
    if "room_id" in st.session_state:
        del st.session_state.room_id
    if "room_name" in st.session_state:
        del st.session_state.room_name
    if "room_code" in st.session_state:
        del st.session_state.room_code
    if "username" in st.session_state:
        del st.session_state.username
    if "is_host" in st.session_state:
        del st.session_state.is_host
    if "message_count" in st.session_state:
        del st.session_state.message_count
    
    # Go back to home
    st.session_state.page = "home"

def close_chat():
    """Close the chatroom (host only) with shutdown animation"""
    if not st.session_state.get("is_host", False):
        return
    
    # Send closing message
    room_id = st.session_state.get("room_id")
    if room_id:
        # send_message(room_id, "SYSTEM", "The host has closed the chatroom", "system")
        
        # Close chatroom in Supabase
        # close_chatroom(room_id)
        pass
    
    # Clear chatroom data from session
    if "room_id" in st.session_state:
        del st.session_state.room_id
    if "room_name" in st.session_state:
        del st.session_state.room_name
    if "room_code" in st.session_state:
        del st.session_state.room_code
    if "username" in st.session_state:
        del st.session_state.username
    if "is_host" in st.session_state:
        del st.session_state.is_host
    if "message_count" in st.session_state:
        del st.session_state.message_count
    
    # Go back to home
    st.session_state.page = "home"
    