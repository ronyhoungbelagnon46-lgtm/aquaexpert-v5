import streamlit as st
import os

st.set_page_config(page_title="AquaExpert V5", page_icon="💧", layout="wide")
st.title("💧 AquaExpert V5 - Assistant Hydraulique")
st.caption("Par Rony - Version avec traitement d'épreuves PDF")

tab1, tab2, tab3 = st.tabs(["💬 Chat Mondial", "📄 Solveur d'Épreuves", "🧮 Calculateurs"])

# --- ONGLET 1 : CHAT INTELLIGENT ---
with tab1:
    st.subheader("💬 Chat Mondial - Pose tes questions d'hydraulique")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salut Rony ! Je suis AquaExpert. Pose-moi une question sur l'hydraulique 💧"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def get_reponse_intelligente(question):
        q = question.lower()
        # Cas simple : plomberie maison
        if any(x in q for x in ["robinet", "déboucher", "fuite", "evier", "wc", "toilette"]):
            return f"""**Pour ton problème : '{question}'**

Voici la solution pratique en 4 étapes :
1.  **Ferme l'eau** : Coupe le robinet d'arrêt général.
2.  **Nettoie** : Démonte le mousseur du robinet (le petit filtre au bout) et nettoie le calcaire avec du vinaigre blanc.
3.  **Débouche** : Si c'est bouché, utilise une ventouse ou du bicarbonate + vinaigre, pas de produits chimiques agressifs.
4.  **Vérifie le joint** : 90% des fuites viennent d'un joint usé (coûte 500F au marché).

Si c'est plus complexe (pression, calcul de débit), dis-le moi et je passe en mode ingénieur !"""
        
        # Cas calcul hydraulique
        else:
            return f"""**Analyse Hydraulique pour : '{question}'**

1.  **Données** : On identifie Q, V, S, H
2.  **Pertes de charge** : Linéaires (J = λ*L/D * V²/2g) et singulières
3.  **HMT** : HMT = Hg + Pc + 10% marge
4.  **Calcul** : 
    - Débit : Q = V x S (Q en m³/s, V en m/s, S en m²)
    - Si tu me donnes les chiffres (ex: tuyau 50m, diamètre 100mm, débit 10L/s), je te calcule tout de suite la HMT et la pompe nécessaire !

Donne-moi les valeurs chiffrées pour un calcul exact."""

    if prompt := st.chat_input("Ta question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            reponse = get_reponse_intelligente(prompt)
            st.markdown(reponse)
        st.session_state.messages.append({"role": "assistant", "content": reponse})

with tab2:
    st.subheader("📄 Solveur d'Épreuves PDF")
    uploaded = st.file_uploader("Upload ton épreuve hydraulique (PDF)", type="pdf")
    if uploaded:
        st.success(f"Fichier {uploaded.name} reçu ! Fonction d'analyse à connecter à l'IA.")
        st.info("Pour l'instant, copie-colle les questions du PDF dans le Chat Mondial.")

with tab3:
    st.subheader("🧮 Calculateurs Rapides")
    col1, col2 = st.columns(2)
    with col1:
        debit = st.number_input("Débit Q (L/s)", value=10.0)
        diametre = st.number_input("Diamètre (mm)", value=100.0)
        if st.button("Calculer Vitesse"):
            import math
            s = math.pi * (diametre/1000)**2 / 4
            v = (debit/1000) / s
            st.success(f"Vitesse V = {v:.2f} m/s | Section S = {s*10000:.2f} cm²")
    with col2:
        hg = st.number_input("Hauteur géométrique Hg (m)", value=10.0)
        pc = st.number_input("Pertes de charge Pc (m)", value=3.0)
        if st.button("Calculer HMT"):
            hmt = hg + pc
            st.success(f"HMT = {hmt:.2f} m (+10% = {hmt*1.1:.2f} m)")
