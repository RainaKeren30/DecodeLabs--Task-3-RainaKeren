"""
Title / Splash Page — full-screen, no sidebar.
Palette: Ghost White #F8F7FF · Antique White #FFEEDD · Peach Fuzz #FFD8BE
         Periwinkle #B8B8FF · Soft Periwinkle #9381FF
"""
import streamlit as st

TITLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=Poppins:wght@600;700;800;900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],section.main>div{background:#F8F7FF !important;}
#MainMenu,footer,header{visibility:hidden}
[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none}
[data-testid="stSidebar"]{display:none !important}
.block-container{padding:0 !important;max-width:100% !important}

.title-canvas{
  min-height:100vh;width:100%;position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:60px 32px 80px;background:#F8F7FF;
}
.mesh-layer{position:absolute;inset:0;z-index:0;pointer-events:none}
.mesh-layer::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse 70% 60% at 15% 20%, rgba(184,184,255,0.55) 0%,transparent 65%),
    radial-gradient(ellipse 60% 55% at 85% 15%, rgba(147,129,255,0.40) 0%,transparent 60%),
    radial-gradient(ellipse 80% 50% at 50% 100%,rgba(255,216,190,0.60) 0%,transparent 65%),
    radial-gradient(ellipse 55% 45% at 90% 80%, rgba(255,238,221,0.50) 0%,transparent 60%),
    radial-gradient(ellipse 65% 55% at 5%  85%, rgba(184,184,255,0.35) 0%,transparent 60%),
    radial-gradient(ellipse 45% 40% at 55% 45%,rgba(147,129,255,0.18) 0%,transparent 55%);
  animation:meshShift 10s ease-in-out infinite alternate;
}
@keyframes meshShift{0%{opacity:1;transform:scale(1) rotate(0deg)}50%{opacity:.85;transform:scale(1.03) rotate(.5deg)}100%{opacity:1;transform:scale(1) rotate(0deg)}}

.orb{position:absolute;border-radius:50%;pointer-events:none;animation:floatOrb 9s ease-in-out infinite alternate}
.orb-1{width:420px;height:420px;top:-120px;left:-120px;background:radial-gradient(circle at 35% 35%,rgba(184,184,255,.80) 0%,rgba(147,129,255,.45) 45%,transparent 70%);filter:blur(40px);animation-duration:11s;animation-delay:0s}
.orb-2{width:360px;height:360px;bottom:-100px;right:-80px;background:radial-gradient(circle at 60% 60%,rgba(255,216,190,.85) 0%,rgba(255,238,221,.50) 50%,transparent 70%);filter:blur(36px);animation-duration:13s;animation-delay:-5s}
.orb-3{width:260px;height:260px;top:40%;right:5%;background:radial-gradient(circle at 40% 40%,rgba(147,129,255,.60) 0%,rgba(184,184,255,.30) 55%,transparent 70%);filter:blur(32px);animation-duration:15s;animation-delay:-3s}
.orb-4{width:180px;height:180px;top:10%;right:20%;background:radial-gradient(circle at 50% 50%,rgba(255,238,221,.70) 0%,rgba(255,216,190,.35) 55%,transparent 70%);filter:blur(24px);animation-duration:9s;animation-delay:-7s}
@keyframes floatOrb{from{transform:translate(0,0) scale(1)}to{transform:translate(18px,-22px) scale(1.04)}}

.glass-card{
  position:relative;z-index:10;
  background:rgba(248,247,255,0.52);
  backdrop-filter:blur(28px) saturate(160%);-webkit-backdrop-filter:blur(28px) saturate(160%);
  border:1.5px solid rgba(255,255,255,0.72);border-radius:32px;
  padding:52px 60px 48px;max-width:820px;width:100%;
  box-shadow:0 2px 0 rgba(255,255,255,.90) inset,0 -1px 0 rgba(147,129,255,.18) inset,0 32px 80px rgba(147,129,255,.18),0 8px 24px rgba(184,184,255,.14);
  display:flex;flex-direction:column;align-items:center;text-align:center;
  animation:cardRise 0.9s cubic-bezier(.22,1,.36,1) both;
}
@keyframes cardRise{from{opacity:0;transform:translateY(32px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}

.eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(147,129,255,.12);border:1.5px solid rgba(147,129,255,.30);
  border-radius:99px;padding:6px 20px;
  font-family:'Space Grotesk',sans-serif;font-size:0.70rem;font-weight:700;
  color:#5B48CC;letter-spacing:.12em;text-transform:uppercase;margin-bottom:28px;
  animation:fadeUp .6s .4s both;
}
.eyebrow-dot{width:6px;height:6px;background:#9381FF;border-radius:50%;animation:pulse 2.2s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(.6);opacity:.45}}

.main-title{
  font-family:'Poppins',sans-serif;font-size:clamp(2.8rem,6.5vw,4.8rem);font-weight:900;
  line-height:1.04;letter-spacing:-2px;color:#2A235A;margin-bottom:8px;
  animation:fadeUp .7s .5s both;
}
.main-title .grad{background:linear-gradient(135deg,#9381FF 0%,#B8B8FF 45%,#FFD8BE 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}

.subtitle{
  font-family:'Inter',sans-serif;font-size:clamp(.92rem,1.8vw,1.1rem);font-weight:400;
  color:#6B5FA6;line-height:1.7;max-width:560px;margin:16px auto 38px;
  animation:fadeUp .7s .65s both;
}
.pill-row{display:flex;flex-wrap:wrap;gap:9px;justify-content:center;margin-bottom:44px;animation:fadeUp .7s .75s both}
.pill{background:rgba(255,255,255,.60);border:1.5px solid rgba(147,129,255,.22);border-radius:99px;padding:6px 16px;font-family:'Space Grotesk',sans-serif;font-size:.74rem;font-weight:600;color:#5B48CC;letter-spacing:.02em}

.stat-strip{display:flex;gap:0;border:1.5px solid rgba(147,129,255,.18);border-radius:20px;overflow:hidden;background:rgba(255,255,255,.45);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);width:100%;max-width:620px;animation:fadeUp .7s .9s both}
.stat-item{flex:1;padding:18px 16px;text-align:center;border-right:1.5px solid rgba(147,129,255,.14)}
.stat-item:last-child{border-right:none}
.stat-num{font-family:'Poppins',sans-serif;font-size:1.7rem;font-weight:800;color:#2A235A;line-height:1;margin-bottom:4px}
.stat-lbl{font-family:'Space Grotesk',sans-serif;font-size:.67rem;font-weight:700;color:#8B7FCC;text-transform:uppercase;letter-spacing:.08em}

@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}

.stButton>button{
  background:linear-gradient(135deg,#9381FF 0%,#B8B8FF 60%,#FFD8BE 100%) !important;
  color:#2A235A !important;border:none !important;border-radius:16px !important;
  font-family:'Space Grotesk',sans-serif !important;font-size:1rem !important;font-weight:700 !important;
  padding:15px 44px !important;
  box-shadow:0 8px 32px rgba(147,129,255,.38),0 2px 0 rgba(255,255,255,.6) inset !important;
  transition:all .28s cubic-bezier(.22,1,.36,1) !important;letter-spacing:.01em !important;
}
.stButton>button:hover{box-shadow:0 14px 44px rgba(147,129,255,.50),0 2px 0 rgba(255,255,255,.6) inset !important;transform:translateY(-3px) scale(1.02) !important}
</style>
"""

def render():
    st.markdown(TITLE_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="title-canvas">
        <div class="mesh-layer"></div>
        <div class="orb orb-1"></div><div class="orb orb-2"></div>
        <div class="orb orb-3"></div><div class="orb orb-4"></div>
        <div class="glass-card">
            <div class="eyebrow"><div class="eyebrow-dot"></div>Content-Based Filtering &nbsp;·&nbsp; Python &nbsp;·&nbsp; Streamlit</div>
            <div class="main-title">Cine<span class="grad">Match</span> AI</div>
            <div class="subtitle">A production-quality movie recommendation engine powered by TF-IDF vectorisation and Cosine Similarity — built from scratch in Python with Scikit-learn and Streamlit.</div>
            <div class="pill-row">
                <div class="pill">Python 3.10+</div><div class="pill">Pandas</div>
                <div class="pill">Scikit-learn</div><div class="pill">TF-IDF</div>
                <div class="pill">Cosine Similarity</div><div class="pill">Streamlit</div><div class="pill">Plotly</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("Enter Dashboard", use_container_width=True):
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    st.markdown("""
    <div style="display:flex;justify-content:center;margin-top:32px;padding:0 24px;">
    <div class="stat-strip">
        <div class="stat-item"><div class="stat-num">50</div><div class="stat-lbl">Movies</div></div>
        <div class="stat-item"><div class="stat-num">11</div><div class="stat-lbl">Features</div></div>
        <div class="stat-item"><div class="stat-num">5K</div><div class="stat-lbl">Vocab Size</div></div>
        <div class="stat-item"><div class="stat-num">6</div><div class="stat-lbl">Pages</div></div>
    </div></div>
    """, unsafe_allow_html=True)
