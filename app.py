import streamlit as st
from groq import Groq
import os

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="AquaExpert Bénin V7", page_icon="🐟", layout="centered")

# --- STYLE CHATGPT ---
st.markdown("""
<style>
.stChatMessage { border-radius: 15px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🐟 AquaExpert Bénin V7")
st.caption("Ton ingénieur aquacole personnel - Spécialiste Tilapia & Clarias - Bénin")

# --- CONNEXION CERVEAU GROQ ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
    model_name = "llama-3.3-70b-versatile"
except Exception as e:
    st.error("❌ Clé GROQ_API_KEY non trouvée dans les Secrets. Vérifie tes Secrets Streamlit.")
    st.stop()

# --- MEMOIRE DE CONVERSATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """Tu es AquaExpert Bénin V7, le meilleur ingénieur aquacole du Bénin.
        Tu es un expert pratique, direct, pas vague.
        Ton objectif: aider les pisciculteurs béninois à GAGNER DE L'ARGENT.
        Règles:
        1. Parle en français simple, avec un peu de langage béninois si besoin.
        2. Donne TOUJOURS des chiffres concrets: doses en grammes, densités en poissons/m3, prix en FCFA, dimensions en mètres.
        3. Ne sois JAMAIS vague. Si on te demande nourrissage, donne formule, quantité, heure.
        4. Adapte tout au contexte Bénin: climat, aliments locaux (son de riz, tourteau de palmiste, farine de poisson), prix Abomey-Calavi.
        5. Tu es spécialiste Tilapia, Clarias (poisson-chat), et étangs, bacs hors-sol, cages.
        6. Termine toujours par une action concrète à faire.
        7. Si tu ne sais pas, dis-le et propose une solution.
        """}
    ]

# --- AFFICHER HISTORIQUE ---
for msg in st.session_state.messages:
    if msg["role"]!= "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- MESSAGE D'ACCUEIL ---
if len(st.session_state.messages) == 1:
    with st.chat_message("assistant"):
        st.markdown("Salut Rony! 👋 Je suis **AquaExpert V7**. Pose-moi ta question : nourrissage, maladie, dimension bac, business plan, je te réponds direct avec les vrais chiffres du Bénin. C'est quoi ton problème aujourd'hui?")

# --- INPUT UTILISATEUR ---
if prompt := st.chat_input("Pose ta question aquacole ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- REPONSE IA ---
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis comme un ingénieur..."):
            try:
                completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=model_name,
                    temperature=0.6,
                    max_tokens=1024,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur Groq: {e}")
                st.info("Vérifie ta connexion ou que tu n'as pas dépassé le quota gratuit.")
