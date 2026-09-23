import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="AquaExpert V5", page_icon="💧", layout="wide")

st.title("💧 AquaExpert V5 - Assistant Hydraulique")
st.caption("Par Rony - Version avec traitement d'épreuves PDF")

tab1, tab2, tab3 = st.tabs(["💬 Chat Mondial", "📄 Solveur d'Épreuves", "🧮 Calculateurs"])

# --- TAB 1 : CHAT ---
with tab1:
    st.subheader("💬 Chat Mondial - Pose tes questions d'hydraulique")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"assistant","content":"Salut Rony ! Je suis AquaExpert. Pose-moi une question sur les réseaux d'eau, pompes, etc."}]
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    prompt = st.chat_input("Ta question...")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        low = prompt.lower()
        if "debit" in low or "flow" in low:
            rep = "**Débit** : Q = V x S. Q en m3/s, V vitesse (m/s), S section (m2). Ex: tuyau DN100 (0.0078m2) à 1m/s => 7.8 L/s."
        elif "perte" in low or "hazen" in low:
            rep = "**Perte de charge** : J = 10.67 x Q^1.852 / (C^1.852 x D^4.87). C=120 PVC, 100 fonte."
        elif "pompe" in low or "puissance" in low:
            rep = "**Puissance pompe** : P (kW) = (Rho x g x Q x HMT) / (rendement x 1000). HMT = Hauteur géo + pertes."
        elif "bernoulli" in low:
            rep = "**Bernoulli** : (P/ρg) + (V²/2g) + Z = constante."
        else:
            rep = f"Question : '{prompt}'. Analyse toujours : 1) Données (débit, longueur, dénivelé) 2) Pertes 3) HMT. Donne des valeurs chiffrées et je calcule !"
        st.session_state.messages.append({"role":"assistant","content":rep})
        st.rerun()

# --- TAB 2 : SOLVEUR PDF ---
with tab2:
    st.subheader("📄 Solveur d'Épreuves - Uploade ton épreuve en PDF")
    uploaded = st.file_uploader("Glisse ton épreuve ici (PDF)", type=["pdf"])
    
    if uploaded:
        with st.spinner("Lecture du PDF..."):
            doc = fitz.open(stream=uploaded.read(), filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n"
        
        st.success(f"PDF lu ! {len(doc)} pages, {len(full_text)} caractères")
        st.text_area("Texte extrait :", full_text[:8000], height=250)
        
        if st.button("🧠 Résoudre l'épreuve automatiquement"):
            st.subheader("✅ Correction AquaExpert")
            if "Q =" in full_text or "débit" in full_text.lower():
                st.write("**Type : Calcul de débit**")
                st.latex(r"Q = V \times S = V \times \frac{\pi D^2}{4}")
            if "HMT" in full_text or "pompe" in full_text.lower():
                st.write("**Type : Dimensionnement pompe**")
                st.latex(r"HMT = H_{geo} + \sum \Delta H")
                st.latex(r"P = \frac{\rho g Q HMT}{\eta}")
            st.info("Méthodologie : 1. Lister données 2. Calculer pertes 3. Bernoulli 4. Conclure")

# --- TAB 3 : CALCULATEURS ---
with tab3:
    st.subheader("🧮 Calculateurs Hydrauliques Pro")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Débit / Vitesse / Diamètre**")
        D = st.number_input("Diamètre (mm)", 50, 1000, 100)
        V = st.number_input("Vitesse (m/s)", 0.1, 5.0, 1.0)
        S = 3.1416*(D/1000)**2/4
        Q = S*V*1000
        st.metric("Débit Q", f"{Q:.2f} L/s", f"{Q*3.6:.2f} m3/h")
    with col2:
        st.markdown("**2. Puissance Pompe**")
        Qm3s = st.number_input("Débit Q (L/s) pour pompe", 1.0, 500.0, 20.0)/1000
        HMT = st.number_input("HMT (m)", 1.0, 200.0, 30.0)
        rend = st.number_input("Rendement (0-1)", 0.5, 0.95, 0.7)
        P = 1000*9.81*Qm3s*HMT / rend /1000
        st.metric("Puissance", f"{P:.2f} kW", f"{P*1.36:.2f} CV")