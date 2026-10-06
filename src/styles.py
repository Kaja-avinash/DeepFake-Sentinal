import streamlit as st


def inject_custom_css():
    st.markdown(
        """
    <style>
        /* --- FONTS & VARS --- */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Oswald:wght@400;600&display=swap');
        
        :root {
            --bg-void: #000000;
            --hex-blue: #00f3ff;
            --hex-purple: #bc13fe;
            --glass-panel: rgba(10, 15, 20, 0.7);
            --text-primary: #e0f7fa;
        }

        /* --- GLOBAL --- */
        .stApp {
            background-color: var(--bg-void);
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 { 
            font-family: 'Oswald', sans-serif !important; 
            text-transform: uppercase; 
            color: var(--text-primary) !important; 
            letter-spacing: 2px; 
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
        }
        p, div, label, span { 
            font-family: 'JetBrains Mono', monospace !important; 
            color: #b0bec5; 
        }

        /* --- STELLAR VORTEX BACKGROUND --- */
        .stellar-vortex-container {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 100vw; height: 100vh; z-index: 0; pointer-events: none; background: #000;
        }
        .vortex-cloud {
            position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: conic-gradient(from 0deg at 50% 50%, #000000 0%, #001a2c 15%, #004e92 30%, #000000 50%, #001a2c 65%, #00f3ff 85%, #000000 100%);
            filter: blur(40px); animation: nebulaSpin 30s linear infinite; opacity: 0.6;
        }
        .vortex-stars {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(white 1px, transparent 1px), radial-gradient(rgba(255,255,255,0.5) 1px, transparent 1px);
            background-size: 50px 50px, 100px 100px; opacity: 0.2; animation: starDrift 60s linear infinite;
        }
        .vortex-core {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 600px; height: 600px; background: radial-gradient(circle, rgba(0,243,255,0.1) 0%, rgba(0,0,0,0) 70%);
            border-radius: 50%; animation: corePulse 4s ease-in-out infinite alternate;
        }

        @keyframes nebulaSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes corePulse { from { transform: translate(-50%, -50%) scale(1); opacity: 0.5; } to { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; } }
        @keyframes starDrift { from { transform: scale(1); } to { transform: scale(1.5); } }

        /* --- UI CARDS --- */
        .neon-card {
            background: rgba(10, 15, 20, 0.75); border: 1px solid rgba(0, 243, 255, 0.2); border-left: 4px solid var(--hex-blue);
            padding: 25px; margin-bottom: 20px; border-radius: 2px; backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); position: relative; z-index: 10;
        }

        /* --- NAV BAR --- */
        div[role="radiogroup"] {
            background: transparent; border-bottom: 1px solid rgba(0, 243, 255, 0.2); padding: 15px;
            display: flex; justify-content: center; gap: 40px; margin-bottom: 50px; position: relative; z-index: 10;
        }
        div[role="radiogroup"] label {
            background: transparent; color: #546e7a; border: none; padding: 10px 0;
            font-family: 'Oswald', sans-serif; text-transform: uppercase; cursor: pointer; transition: all 0.3s; font-size: 1.1rem;
        }
        div[role="radiogroup"] label:hover { color: var(--hex-blue); text-shadow: 0 0 8px rgba(0, 243, 255, 0.6); }
        div[role="radiogroup"] label[data-checked="true"] {
            color: var(--hex-blue); text-shadow: 0 0 15px rgba(0, 243, 255, 0.8); border-bottom: 2px solid var(--hex-blue);
        }
        div[role="radiogroup"] > label > div:first-child { display: none !important; }

        /* --- BUTTONS --- */
        div.stButton > button {
            background: rgba(0, 243, 255, 0.05); border: 1px solid var(--hex-blue); color: var(--hex-blue);
            font-family: 'JetBrains Mono', monospace; font-weight: 700; transition: 0.3s; border-radius: 2px;
        }
        div.stButton > button:hover { background: var(--hex-blue); color: #000; box-shadow: 0 0 20px var(--hex-blue); }

        /* --- LOADER OVERLAY --- */
        .loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000000; z-index: 999999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            animation: fadeOut 0.5s ease-out 2.5s forwards;
        }
        .loader-box {
            position: relative; z-index: 20; background: rgba(10, 15, 20, 0.8); border: 1px solid var(--hex-blue);
            padding: 50px 70px; border-radius: 8px; display: flex; flex-direction: column; align-items: center;
            box-shadow: 0 0 60px rgba(0, 243, 255, 0.15); backdrop-filter: blur(8px);
        }
        .loading-text {
            font-family: 'Oswald', sans-serif; font-size: 20px; letter-spacing: 5px; color: var(--hex-blue);
            text-transform: uppercase; margin-top: 30px;
        }
        .loading-bar { width: 100%; height: 3px; background: #333; margin-top: 20px; }
        .loading-bar-fill {
            height: 100%; background: var(--hex-blue); width: 0%;
            animation: fillBar 2s ease-in-out forwards; box-shadow: 0 0 10px var(--hex-blue);
        }
        @keyframes fillBar { 0% { width: 0%; } 100% { width: 100%; } }
        @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }
    </style>
    """,
        unsafe_allow_html=True,
    )
