import streamlit as st
import random
import time

# Set page config
st.set_page_config(
    page_title="Retro Chat",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "transition_effect" not in st.session_state:
    st.session_state.transition_effect = True

# Enhanced styling with inline CSS - no external files needed
st.markdown("""
<style>
/* Base Styling */
body {
    background-color: #120458;
    background-image: linear-gradient(180deg, #120458 0%, #000000 100%);
    color: #fff;
    font-family: monospace;
}

/* CRT Screen Effect */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 2px, 3px 100%;
    pointer-events: none;
    z-index: 999;
}

/* Random Glitch Effect */
@keyframes random-glitch {
    0%, 100% { 
        clip-path: inset(80% 0 0 0);
        transform: translate(-2px, 0);
    }
    20% { 
        clip-path: inset(10% 0 60% 0); 
        transform: translate(2px, 0);
    }
    40% { 
        clip-path: inset(30% 0 20% 0); 
        transform: translate(0, 2px);
    }
    60% { 
        clip-path: inset(10% 0 70% 0); 
        transform: translate(-2px, -2px);
    }
    80% { 
        clip-path: inset(50% 0 30% 0); 
        transform: translate(2px, -2px);
    }
}

/* Scanline Effect */
@keyframes scanline {
    0% {
        transform: translateY(-100%);
    }
    100% {
        transform: translateY(100%);
    }
}

.scanline {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: rgba(255, 255, 255, 0.1);
    z-index: 998;
    opacity: 0.3;
    animation: scanline 8s linear infinite;
}

/* VHS Tracking Lines */
@keyframes tracking {
    0% {
        transform: translateY(-100%);
    }
    100% {
        transform: translateY(200%);
    }
}

.tracking-line {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 15px;
    background: rgba(0, 255, 249, 0.03);
    z-index: 997;
    animation: tracking 15s linear infinite;
}

/* Power On Animation */
@keyframes power-on {
    0% {
        opacity: 0;
        transform: scale(0.8);
        filter: brightness(0);
    }
    10% {
        opacity: 0.5;
        transform: scale(0.9);
        filter: brightness(0.5) blur(10px);
    }
    30% {
        opacity: 0.8;
        filter: brightness(1.2) blur(5px);
    }
    40% {
        filter: brightness(0.8) blur(0);
    }
    50% {
        filter: brightness(1.2);
    }
    60% {
        filter: brightness(0.9);
    }
    70% {
        filter: brightness(1.1);
    }
    80%, 100% {
        opacity: 1;
        transform: scale(1);
        filter: brightness(1);
    }
}

.power-on {
    animation: power-on 2s forwards;
}

/* Page Transition Effect */
@keyframes crt-off {
    0% {
        opacity: 1;
        transform: scale(1);
        filter: brightness(1);
    }
    10% {
        filter: brightness(1.5);
    }
    30% {
        transform: scale(1.02, 0.8);
        filter: brightness(10);
    }
    40% {
        transform: scale(1, 0.1);
        filter: brightness(10);
    }
    50%, 100% {
        transform: scale(0, 0.1);
        filter: brightness(0);
        opacity: 0;
    }
}

@keyframes crt-on {
    0% {
        opacity: 0;
        transform: scale(1, 0.01);
        filter: brightness(0);
    }
    10% {
        opacity: 1;
        transform: scale(1, 0.03);
        filter: brightness(5);
    }
    30% {
        transform: scale(1.02, 0.5);
        filter: brightness(2);
    }
    50% {
        transform: scale(1.02, 1.02);
        filter: brightness(1.5);
    }
    70% {
        transform: scale(0.99, 0.99);
    }
    100% {
        transform: scale(1);
        filter: brightness(1);
    }
}

.crt-off {
    animation: crt-off 0.8s forwards;
}

.crt-on {
    animation: crt-on 1s forwards;
}

/* Neon Text */
.neon-text {
    color: #fff;
    text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #0073e6, 0 0 20px #0073e6, 0 0 25px #0073e6, 0 0 30px #0073e6, 0 0 35px #0073e6;
}

.hot-pink-text {
    color: #ff00c1;
    text-shadow: 0 0 5px #ff00c1, 0 0 10px #ff00c1, 0 0 15px #ff00c1, 0 0 20px #ff00c1;
}

.cyan-text {
    color: #00fff9;
    text-shadow: 0 0 5px #00fff9, 0 0 10px #00fff9, 0 0 15px #00fff9, 0 0 20px #00fff9;
}

.lime-text {
    color: #adff2f;
    text-shadow: 0 0 5px #adff2f, 0 0 10px #adff2f, 0 0 15px #adff2f, 0 0 20px #adff2f;
}

/* Pulsing Neon */
@keyframes neon-pulse {
    0%, 100% {
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #0073e6, 0 0 20px #0073e6, 0 0 25px #0073e6;
    }
    50% {
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #0073e6, 0 0 20px #0073e6, 0 0 25px #0073e6, 0 0 30px #0073e6, 0 0 35px #0073e6, 0 0 40px #0073e6;
    }
}

@keyframes pink-pulse {
    0%, 100% {
        text-shadow: 0 0 5px #ff00c1, 0 0 10px #ff00c1;
    }
    50% {
        text-shadow: 0 0 10px #ff00c1, 0 0 20px #ff00c1, 0 0 30px #ff00c1;
    }
}

@keyframes cyan-pulse {
    0%, 100% {
        text-shadow: 0 0 5px #00fff9, 0 0 10px #00fff9;
    }
    50% {
        text-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9, 0 0 30px #00fff9;
    }
}

@keyframes lime-pulse {
    0%, 100% {
        text-shadow: 0 0 5px #adff2f, 0 0 10px #adff2f;
    }
    50% {
        text-shadow: 0 0 10px #adff2f, 0 0 20px #adff2f, 0 0 30px #adff2f;
    }
}

.neon-pulse {
    animation: neon-pulse 2s infinite;
}

.pink-pulse {
    animation: pink-pulse 2s infinite;
}

.cyan-pulse {
    animation: cyan-pulse 1.5s infinite;
}

.lime-pulse {
    animation: lime-pulse 2.5s infinite;
}

/* Retro Header */
h1 {
    font-size: 3rem;
    background: linear-gradient(90deg, #ff00c1, #00fff9, #adff2f);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 0.75rem #ff00c1);
    margin: 1rem 0;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
}

@keyframes rainbow-shift {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.rainbow-text {
    background: linear-gradient(90deg, #ff00c1, #00fff9, #adff2f, #ff00c1);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow-shift 4s ease infinite;
}

h2 {
    text-transform: uppercase;
    letter-spacing: 2px;
    text-align: center;
}

/* Flicker Text Animation */
@keyframes text-flicker {
    0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100% {
        opacity: 1;
    }
    20%, 21.999%, 63%, 63.999%, 65%, 69.999% {
        opacity: 0.4;
    }
}

.text-flicker {
    animation: text-flicker 4s linear infinite;
}

/* Glitch Text Animation */
@keyframes glitch-text {
    0%, 100% { 
        text-shadow: -2px 0 #ff00c1, 2px 0 #00fff9;
        transform: translate(0);
    }
    25% {
        text-shadow: -2px 0 #00fff9, 2px 0 #ff00c1;
        transform: translate(1px, 1px);
    }
    50% {
        text-shadow: 2px 0 #ff00c1, -2px 0 #adff2f;
        transform: translate(-1px, -1px);
    }
    75% {
        text-shadow: 2px 0 #adff2f, -2px 0 #00fff9;
        transform: translate(1px, -1px);
    }
}

.glitch-text {
    animation: glitch-text 3s infinite;
}

/* Button Styles */
.stButton button {
    background: black !important;
    color: #00fff9 !important;
    border: 3px solid #00fff9 !important;
    border-radius: 0 !important;
    box-shadow: 0 0 5px #00fff9, 0 0 10px #00fff9 !important;
    padding: 10px 24px !important;
    transition: all 0.3s !important;
    text-transform: uppercase !important;
    margin: 10px 0 !important;
    position: relative;
    overflow: hidden;
}

.stButton button:hover {
    background: #00fff9 !important;
    color: black !important;
    box-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9, 0 0 30px #00fff9 !important;
    transform: scale(1.05) !important;
}

/* Button Hover Effect */
.stButton button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 249, 0.4), transparent);
    transition: 0.5s;
    pointer-events: none;
}

.stButton button:hover::before {
    left: 100%;
}

/* Input Fields */
div[data-baseweb="input"] {
    background: #000 !important;
    border: 2px solid #ff00c1 !important;
    box-shadow: 0 0 5px #ff00c1 !important;
    transition: all 0.3s ease;
}

div[data-baseweb="input"]:focus-within {
    border: 2px solid #ff00c1 !important;
    box-shadow: 0 0 10px #ff00c1, 0 0 20px #ff00c1 !important;
}

input[type="text"] {
    color: #adff2f !important;
    font-size: 18px !important;
}

/* Room Code Display */
.room-code {
    letter-spacing: 5px;
    font-size: 2rem;
    color: #adff2f;
    text-shadow: 0 0 5px #adff2f, 0 0 10px #adff2f;
    background-color: rgba(0, 0, 0, 0.8);
    padding: 15px;
    border: 3px solid #adff2f;
    text-align: center;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
}

@keyframes glow {
    0%, 100% {
        box-shadow: 0 0 5px #adff2f, 0 0 10px #adff2f;
    }
    50% {
        box-shadow: 0 0 10px #adff2f, 0 0 20px #adff2f, 0 0 30px #adff2f;
    }
}

.room-code {
    animation: glow 2s infinite;
}

/* Overlay for scan lines in containers */
.container-scan {
    position: relative;
}

.container-scan::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%);
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 1;
}

/* Blinking cursor */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.blinking-cursor::after {
    content: "_";
    animation: blink 1s infinite;
}

/* Loading animation */
@keyframes loading {
    0% { content: ""; }
    25% { content: "."; }
    50% { content: ".."; }
    75% { content: "..."; }
    100% { content: "...."; }
}

.loading::after {
    content: "";
    animation: loading 1s infinite;
    display: inline-block;
    width: 20px;
    text-align: left;
}

/* Random Static Flash */
@keyframes static-flash {
    0%, 100% { opacity: 0; }
    5%, 10% { opacity: 0.1; }
    7% { opacity: 0.3; }
}

.static-flash {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAUVBMVEWFhYWDg4N3d3dtbW17e3t1dXWBgYGHh4d5eXlzc3OLi4ubm5uVlZWPj4+NjY19fX2JiYl/f39ra2uRkZGZmZlpaWmXl5dvb29xcXGTk5NnZ2c8TV1mAAAAG3RSTlNAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAvEOwtAAAFVklEQVR4XpWWB67c2BUFb3g557T/hRo9/WUMZHlgr4Bg8Z4qQgQJlHI4A8SzFVrapvmTF9O7dmYRFZ60YiBhJRCgh1FYhiLAmdvX0CzTOpNE77ME0Zty/nWWzchDtiqrmQDeuv3powQ5ta2eN0FY0InkqDD73lT9c9lEzwUNqgFHs9VQce3TVClFCQrSTfOiYkVJQBmpbq2L6iZavPnAPcoU0dSw0SUTqz/GtrGuXfbyyBniKykOWQWGqwwMA7QiYAxi+IlPdqo+hYHnUt5ZPfnsHJyNiDtnpJyayNBkF6cWoYGAMY92U2hXHF/C1M8uP/ZtYdiuj26UdAdQQSXQErwSOMzt/XWRWAz5GuSBIkwG1H3FabJ2OsUOUhGC6tK4EMtJO0ttC6IBD3kM0ve0tJwMdSfjZo+EEISaeTr9P3wYrGjXqyC1krcKdhMpxEnt5JetoulscpyzhXN5FRpuPHvbeQaKxFAEB6EN+cYN6xD7RYGpXpNndMmZgM5Dcs3YSNFDHUo2LGfZuukSWyUYirJAdYbF3MfqEKmjM+I2EfhA94iG3L7uKrR+GdWD73ydlIB+6hgref1QTlmgmbM3/LeX5GI1Ux1RWpgxpLuZ2+I+IjzZ8wqE4nilvQdkUdfhzI5QDWy+kw5");
    pointer-events: none;
    z-index: 998;
    opacity: 0;
    animation: static-flash 8s linear infinite;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(0,0,0,0.7);
    padding: 5px;
    border-top: 2px solid #ff00c1;
    text-align: center;
    font-size: 14px;
    color: #adff2f;
}

/* Chat Container */
.chat-container {
    background-color: rgba(0, 0, 0, 0.7);
    border: 3px solid #ff00c1;
    border-radius: 0;
    box-shadow: 0 0 10px #ff00c1;
    padding: 20px;
    margin: 20px 0;
    height: 300px;
    overflow-y: auto;
    position: relative;
}

/* Text typing animation */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

.typing-animation {
    overflow: hidden;
    white-space: nowrap;
    animation: typing 3s steps(40, end);
}

/* Background power lines effect */
.power-grid {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        linear-gradient(90deg, rgba(173, 255, 47, 0.03) 1px, transparent 1px),
        linear-gradient(0deg, rgba(0, 255, 249, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: -1;
}

@keyframes grid-movement {
    0% {
        background-position: 0 0;
    }
    100% {
        background-position: 20px 20px;
    }
}

.power-grid {
    animation: grid-movement 10s linear infinite;
}
</style>

<!-- Dynamic background effects -->
<div class="scanline"></div>
<div class="tracking-line" style="top: 30%;"></div>
<div class="tracking-line" style="top: 60%;"></div>
<div class="static-flash"></div>
<div class="power-grid"></div>

<script>
// Function to add CRT on/off effect when changing pages
function addPageTransitionEffects() {
    // Create container for our transition
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

    // Remove after animation completes
    setTimeout(() => {
        document.body.removeChild(container);
    }, 800);
}

// Add random glitch effects occasionally
function randomGlitchEffect() {
    if (Math.random() < 0.05) {  // 5% chance per interval
        let glitchElement = document.createElement('div');
        glitchElement.style.position = 'fixed';
        glitchElement.style.top = '0';
        glitchElement.style.left = '0';
        glitchElement.style.width = '100%';
        glitchElement.style.height = '100%';
        glitchElement.style.backgroundColor = 'rgba(0, 255, 249, 0.1)';
        glitchElement.style.zIndex = '9998';
        glitchElement.style.animation = 'random-glitch 0.2s forwards';
        document.body.appendChild(glitchElement);

        setTimeout(() => {
            document.body.removeChild(glitchElement);
        }, 200);
    }
}

// Add this for initial loading effect
window.addEventListener('load', function() {
    document.body.classList.add('power-on');
    
    // Set interval for random glitch effects
    setInterval(randomGlitchEffect, 2000);
});
</script>
""", unsafe_allow_html=True)

# Create footer
st.markdown(
    """
    <div class="footer">
        <span class="lime-pulse">RETRO-CHAT v1.0</span> | <span class="cyan-text">© 2025</span> | <span class="text-flicker">PRESS ESC TO EXIT</span>
    </div>
    """,
    unsafe_allow_html=True
)

def home_page():
    """Home page with options to host or join"""
    # Title with enhanced animation
    st.markdown("<h1 class='rainbow-text'>RETRO CHAT</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style="text-align: center; color: #00fff9; font-size: 1.5rem; letter-spacing: 2px;" class="cyan-pulse">
            A BLAST FROM THE PAST
        </p>
        """, 
        unsafe_allow_html=True
    )
    
    # Description with typing animation
    st.markdown(
        """
        <div style="text-align: center; margin: 30px 0;">
            <p style="font-size: 1.2rem; color: #adff2f;" class="typing-animation">
                Create or join a retro-styled temporary chatroom with your friends.
            </p>
            <p style="font-size: 1.2rem; color: #adff2f;" class="blinking-cursor">
                No accounts, no history, just pure nostalgic vibes
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Options
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="background-color: rgba(0, 0, 0, 0.7); border: 3px solid #ff00c1; padding: 30px; margin: 20px 0; box-shadow: 0 0 15px #ff00c1;" class="container-scan">
                <h2 style="color: #00fff9;" class="glitch-text">CHOOSE YOUR PATH</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("HOST CHATROOM", key="host_btn"):
                # Add page transition effect
                if st.session_state.transition_effect:
                    st.markdown(
                        """
                        <script>
                        addPageTransitionEffects();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                st.session_state.page = "host"
                st.experimental_rerun()
        
        with col_b:
            if st.button("JOIN CHATROOM", key="join_btn"):
                # Add page transition effect
                if st.session_state.transition_effect:
                    st.markdown(
                        """
                        <script>
                        addPageTransitionEffects();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                st.session_state.page = "join"
                st.experimental_rerun()

def host_chatroom():
    """Host a new chatroom interface"""
    st.markdown("<h1 class='rainbow-text'>HOST A CHATROOM</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style="text-align: center; color: #00fff9; font-size: 1.2rem; letter-spacing: 1px;" class="cyan-pulse">
            Create your own retro chat space
        </p>
        """, 
        unsafe_allow_html=True
    )
    
    # Input fields for chatroom name and host username
    st.markdown('<p class="cyan-text text-flicker" style="margin-top: 30px;">ENTER CHATROOM INFO:</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            room_name = st.text_input("ROOM NAME", key="room_name", placeholder="MY RADICAL CHATROOM")
        with col2:
            host_name = st.text_input("YOUR NAME", key="host_name", placeholder="NEON_RIDER")
    
    # Create chatroom button
    if st.button("CREATE CHATROOM", key="create_room_btn"):
        if not room_name or not host_name:
            st.error("Please enter both room name and your name")
            return
        
        with st.spinner(""):
            # Show retro loading animation
            st.markdown(
                """
                <div style="text-align: center;">
                    <p class="hot-pink-text pink-pulse">INITIALIZING CHATROOM</p>
                    <div style="color: #00fff9;">
                        <span class="glitch-text loading">CONNECTING</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Generate a random 5-digit code
            room_code = str(random.randint(10000, 99999))
            
            # Add some delay for effect
            time.sleep(1.5)
            
            # Store chatroom info in session state
            st.session_state.room_code = room_code
            st.session_state.username = host_name
            st.session_state.room_name = room_name
            st.session_state.is_host = True
            st.session_state.page = "chat"
            
            # Add page transition effect
            if st.session_state.transition_effect:
                st.markdown(
                    """
                    <script>
                    addPageTransitionEffects();
                    </script>
                    """,
                    unsafe_allow_html=True
                )
            
            st.experimental_rerun()
    
    # Back button
    if st.button("BACK", key="back_btn"):
        # Add page transition effect
        if st.session_state.transition_effect:
            st.markdown(
                """
                <script>
                addPageTransitionEffects();
                </script>
                """,
                unsafe_allow_html=True
            )
        st.session_state.page = "home"
        st.experimental_rerun()

def join_chatroom():
    """Interface for joining an existing chatroom"""
    st.markdown("<h1 class='rainbow-text'>JOIN A CHATROOM</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style="text-align: center; color: #00fff9; font-size: 1.2rem; letter-spacing: 1px;" class="cyan-pulse">
            Enter the access code
        </p>
        """, 
        unsafe_allow_html=True
    )
    
    # Input fields for room code and username
    st.markdown('<p class="cyan-text text-flicker" style="margin-top: 30px;">ENTER ACCESS CREDENTIALS:</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            room_code = st.text_input("ROOM CODE", key="join_room_code", placeholder="12345")
        with col2:
            username = st.text_input("YOUR NAME", key="join_username", placeholder="PIXEL_PUNK")
    
    # Join button
    if st.button("JOIN CHATROOM", key="join_room_btn"):
        if not room_code or not username:
            st.error("Please enter both room code and your name")
            return
        
        # For demonstration, we'll just simulate a successful join
        # In the full app, you'd validate the code with Supabase
        
        # Show loading animation
        st.markdown(
            """
            <div style="text-align: center;">
                <p class="hot-pink-text pink-pulse">VALIDATING CODE</p>
                <div style="color: #00fff9;">
                    <span class="glitch-text loading">CONNECTING</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add some delay for effect
        time.sleep(1.5)
        
        # Store info in session state
        st.session_state.room_code = room_code
        st.session_state.username = username
        st.session_state.room_name = "DEMO ROOM"  # This would come from DB lookup
        st.session_state.is_host = False
        st.session_state.page = "chat"
        
        # Add page transition effect
        if st.session_state.transition_effect:
            st.markdown(
                """
                <script>
                addPageTransitionEffects();
                </script>
                """,
                unsafe_allow_html=True
            )
        
        st.experimental_rerun()
    
    # Back button
    if st.button("BACK", key="back_btn_join"):
        # Add page transition effect
        if st.session_state.transition_effect:
            st.markdown(
                """
                <script>
                addPageTransitionEffects();
                </script>
                """,
                unsafe_allow_html=True
            )
        st.session_state.page = "home"
        st.experimental_rerun()

def chat_interface():
    """Enhanced chat interface with more motion effects"""
    # Display chat header
    room_name = st.session_state.room_name
    username = st.session_state.username
    is_host = st.session_state.get("is_host", False)
    
    header_suffix = " (HOST)" if is_host else ""
    st.markdown(f"<h1 class='rainbow-text'>CHATROOM: {room_name}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <p style="text-align: center; color: #00fff9; font-size: 1.2rem;" class="cyan-pulse">
            Logged in as: <span class="hot-pink-text">{username}{header_suffix}</span>
        </p>
        """, 
        unsafe_allow_html=True
    )
    
    # If host, display the room code for sharing
    if is_host:
        st.markdown(
            f"""
            <div class="room-code">{st.session_state.room_code}</div>
            <p class="lime-text lime-pulse" style="text-align: center;">SHARE THIS CODE WITH OTHERS TO JOIN</p>
            """, 
            unsafe_allow_html=True
        )
    
    # Simple chat display with enhanced effects
    st.markdown(
        """
        <div class="chat-container container-scan">
            <div style="color: #adff2f; margin-bottom: 10px; text-align: center;" class="text-flicker">
                Messages will appear here in the full version
            </div>
            <div style="color: #00fff9; margin-bottom: 10px; text-align: center;" class="typing-animation">
                This is a placeholder chat interface with enhanced motion graphics
            </div>
            <div style="color: #ff00c1; margin-bottom: 10px; text-align: center;" class="glitch-text">
                Customize text effects for different message types
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Message input with blinking cursor indicator
    col1, col2 = st.columns([4, 1])
    
    with col1:
        message = st.text_input("", key="message_input", placeholder="TYPE YOUR MESSAGE HERE...")
    
    with col2:
        if st.button("SEND", key="send_btn"):
            if message:
                st.success(f"Message sent! In the full version, this would be saved to the database.")
                st.session_state.message_input = ""
    
    # Show simulated message typing effect
    if message:
        st.markdown(
            f"""
            <div style="background-color: rgba(173, 255, 47, 0.1); border-left: 3px solid #adff2f; padding: 10px; margin-top: 10px;" class="typing-animation">
                <span class="hot-pink-text">{username}:</span> {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Exit button
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
        
        st.session_state.page = "home"
        st.experimental_rerun()

# Main application logic
def main():
    # Handle different pages
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "host":
        host_chatroom()
    elif st.session_state.page == "join":
        join_chatroom()
    elif st.session_state.page == "chat":
        chat_interface()

# Run the main application
if __name__ == "__main__":
    main()
    