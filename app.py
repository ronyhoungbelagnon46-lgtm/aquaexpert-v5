import streamlit as st
from groq import Groq

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AquaExpert Bénin",
    page_icon="💧",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.aqua-header {
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #006994, #00a6a6);
    color: white;
}

.aqua-header h1 {
    margin-bottom: 5px;
}

.mode-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f1f5f9;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="aqua-header">

<h1>💧 AquaExpert Bénin</h1>

<p>
L'assistant intelligent spécialisé dans les domaines de l'eau,
de l'hydraulique et de l'assainissement.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# CONNEXION GROQ
# =========================================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(api_key=api_key)

    model_name = "llama-3.1-8b-instant"

except Exception:

    st.error(
        "❌ La clé GROQ_API_KEY est introuvable. "
        "Ajoute-la dans les Secrets de ton application Streamlit."
    )

    st.stop()


# =========================================================
# DOMAINES
# =========================================================

modes = {

    "💧 Hydraulique":
        "hydraulique générale, écoulement, conduites, caniveaux, dalots, pompes, pertes de charge, pression, débit",

    "🌧️ Hydrologie":
        "pluviométrie, ruissellement, bassin versant, crues, débits de pointe, hydrologie urbaine",

    "🚰 Eau potable":
        "adduction d'eau potable, besoins en eau, réseaux, réservoirs, pompage, traitement et distribution",

    "🚽 Assainissement":
        "eaux usées, eaux pluviales, drainage, fosses, réseaux d'assainissement et ouvrages",

    "🧪 Qualité de l'eau":
        "pH, turbidité, conductivité, matières en suspension, analyses et traitement de l'eau",

    "🐟 Aquaculture":
        "pisciculture, Tilapia, Clarias, alimentation, bassins, qualité de l'eau et production",

    "🏗️ Ouvrages hydrauliques":
        "dalots, caniveaux, buses, regards, ouvrages de drainage, contrôle qualité et chantier",

    "📐 Calcul technique":
        "calculs hydrauliques, débit, section, vitesse, pente, Manning, Strickler, volumes et dimensions"
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    selected_mode = st.selectbox(
        "Choisis un domaine",
        list(modes.keys())
    )

    st.divider()

    st.subheader("🎯 Niveau")

    level = st.selectbox(
        "Niveau de réponse",
        [
            "Débutant",
            "Étudiant",
            "Technicien",
            "Ingénieur"
        ]
    )

    st.divider()

    st.subheader("🇧🇯 Contexte")

    benin_context = st.checkbox(
        "Adapter au contexte béninois",
        value=True
    )

    st.divider()

    if st.button("🗑️ Nouvelle conversation"):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# SYSTEM PROMPT
# =========================================================

context_benin = ""

if benin_context:

    context_benin = """
    Lorsque cela est pertinent, adapte les explications au contexte du Bénin :
    climat tropical, pluies intenses, urbanisation de Cotonou et des autres villes,
    problèmes de drainage, assainissement, accès à l'eau potable,
    pratiques de chantier et unités utilisées localement.

    Ne jamais inventer une norme béninoise.
    Si une norme ou réglementation précise est nécessaire,
    indique qu'une vérification de la référence officielle est nécessaire.
    """


system_prompt = f"""

Tu es AquaExpert Bénin, un assistant technique spécialisé dans les domaines
de l'eau, de l'hydraulique, de l'hydrologie, de l'assainissement,
de l'eau potable, de la qualité de l'eau, des ouvrages hydrauliques
et de l'aquaculture.

DOMAINE ACTUEL :
{selected_mode}

SPÉCIALITÉS DU DOMAINE :
{modes[selected_mode]}

NIVEAU DE L'UTILISATEUR :
{level}

{context_benin}

RÈGLES DE RÉPONSE :

1. Réponds en français simple et professionnel.

2. Donne une réponse structurée avec des titres et des listes
   lorsque cela améliore la compréhension.

3. Pour un calcul :
   - donne les données connues ;
   - identifie les hypothèses ;
   - donne la formule ;
   - remplace les valeurs ;
   - donne le résultat avec l'unité ;
   - explique brièvement ce que signifie le résultat.

4. N'invente jamais une donnée technique, une norme,
   une réglementation ou une valeur expérimentale.

5. Si une donnée importante manque pour effectuer un calcul,
   demande-la ou indique clairement l'hypothèse utilisée.

6. Utilise les unités SI :
   m, m², m³, m³/s, L/s, Pa, kPa, mm, etc.

7. Lorsque plusieurs méthodes sont possibles,
   présente les principales et explique brièvement leur différence.

8. Pour les travaux de chantier, distingue clairement :
   - conception ;
   - exécution ;
   - contrôle ;
   - sécurité.

9. Pour les questions concernant le Bénin,
   ne prétends pas connaître une réglementation spécifique
   si tu n'en as pas la référence.

10. Si tu n'es pas certain d'une information,
    dis-le clairement plutôt que d'inventer.

11. Termine par une courte section :
    "👉 À faire maintenant"

12. Ton objectif est d'aider l'utilisateur à comprendre,
    calculer et prendre de bonnes décisions techniques,
    pas simplement de produire une réponse vague.
"""


# =========================================================
# INITIALISATION MÉMOIRE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

else:

    # Mise à jour du domaine si l'utilisateur change de mode
    st.session_state.messages[0]["content"] = system_prompt


# =========================================================
# INFORMATIONS DU MODE
# =========================================================

st.subheader(selected_mode)

st.caption(
    f"Mode spécialisé : {modes[selected_mode]}"
)


# =========================================================
# QUESTIONS RAPIDES
# =========================================================

st.markdown("### 💡 Questions rapides")

questions = {

    "💧 Hydraulique": [
        "Comment calculer le débit dans un canal ?",
        "Explique-moi la formule de Manning.",
        "Comment dimensionner un caniveau ?"
    ],

    "🌧️ Hydrologie": [
        "Comment calculer le débit de pointe ?",
        "Qu'est-ce qu'un bassin versant ?",
        "Comment analyser une pluie ?"
    ],

    "🚰 Eau potable": [
        "Comment calculer les besoins en eau d'une population ?",
        "Comment dimensionner un réservoir ?",
        "Quelles sont les étapes d'un réseau AEP ?"
    ],

    "🚽 Assainissement": [
        "Comment dimensionner une fosse septique ?",
        "Comment fonctionne un réseau d'eaux pluviales ?",
        "Comment choisir la pente d'un réseau ?"
    ],

    "🧪 Qualité de l'eau": [
        "Quels paramètres analyser pour une eau potable ?",
        "Que signifie un pH de 6,5 ?",
        "Comment interpréter la turbidité ?"
    ],

    "🐟 Aquaculture": [
        "Comment élever le Tilapia ?",
        "Quelle qualité d'eau pour le Clarias ?",
        "Comment calculer la quantité d'aliment ?"
    ],

    "🏗️ Ouvrages hydrauliques": [
        "Comment contrôler la pose d'un dalot ?",
        "Quels contrôles effectuer sur le béton ?",
        "Comment contrôler un caniveau ?"
    ],

    "📐 Calcul technique": [
        "Calcule le débit avec Manning.",
        "Comment calculer la vitesse d'écoulement ?",
        "Comment calculer une section hydraulique ?"
    ]
}


cols = st.columns(3)

for i, question in enumerate(questions[selected_mode]):

    with cols[i]:

        if st.button(
            question,
            use_container_width=True
        ):

            st.session_state.pending_question = question


# =========================================================
# HISTORIQUE
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# MESSAGE UTILISATEUR
# =========================================================

prompt = st.chat_input(
    "Pose ta question sur l'eau..."
)


# Gestion question rapide

if "pending_question" in st.session_state:

    prompt = st.session_state.pending_question

    del st.session_state.pending_question


# =========================================================
# TRAITEMENT
# =========================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    with st.chat_message("assistant"):

        with st.spinner("💧 AquaExpert analyse ta question..."):

            try:

                completion = client.chat.completions.create(

                    messages=st.session_state.messages,

                    model=model_name,

                    temperature=0.3,

                    max_tokens=1500
                )

                response = (
                    completion
                    .choices[0]
                    .message
                    .content
                )

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Une erreur est survenue : {e}"
                )
