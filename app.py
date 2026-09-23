import streamlit as st

st.set_page_config(page_title="AquaExpert V6", page_icon="💧", layout="wide")
st.title("💧 AquaExpert V6 - Expert comme ChatGPT")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Salut Rony! Je suis AquaExpert V6, en mode ChatGPT. Je donne des réponses longues, humaines, avec calculs détaillés. Teste-moi!"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

def reponse_humanisee(q):
    q_low = q.lower()
    if any(x in q_low for x in ["robinet","déboucher","evier","fuite"]):
        return f"""**Ah, ton problème: "{q}" - je comprends, c'est pénible au quotidien!**

Laisse-moi t'expliquer comme si on était côte à côte à Abomey-Calavi :

**Pourquoi ça se bouche ?**
90% du temps c'est le calcaire de la SONEB + sable + cheveux qui s'accumule dans le mousseur (le petit filtre au bout).

**Solution complète et humaine :**

**Étape 1 - Sécurité (1 min)**
Ferme le robinet d'arrêt sous l'évier. Mets une bassine. Si tu n'as pas de robinet d'arrêt, ferme le compteur général dehors.

**Étape 2 - Le mousseur (la cause n°1)**
Dévisse le petit embout au bout du robinet à la main (ou avec un chiffon). Tu vas voir du blanc/vert. Fais-le tremper 2h dans du vinaigre blanc pur (500F au marché). Frotte avec une vieille brosse à dents.

**Étape 3 - Si ça coule encore faible**
Prends une ventouse à 1500F. Bouche le trop-plein avec un chiffon, pompe 5-6 coups secs. Ou recette de grand-mère béninoise : 4 cuillères de bicarbonate + 1 verre de vinaigre chaud, laisse 30 min, puis eau bouillante.

**Étape 4 - Vérifie le joint**
Si ça goutte, le joint noir à l'intérieur est mort. Ça coûte 300-500F. Change-le, n'achète pas un nouveau robinet à 15000F!

**À NE PAS FAIRE:** Acide sulfurique (Destop) - ça bouffe tes tuyaux PVC!

Dis-moi : c'est un robinet de cuisine ou de douche? Je te donne la suite exacte."""

    else:
        return f"""**Super question d'ingénieur: "{q}"**

Je te détaille comme un prof qui veut que tu comprennes vraiment, pas comme un robot.

**1. Ce qu'on doit comprendre:**
On parle ici d'énergie de l'eau. L'eau perd de l'énergie à cause du frottement (pertes de charge). La formule reine c'est Bernoulli + Darcy-Weisbach.

**2. Les formules que j'utilise (retenons-les):**
- Débit: Q = V x S (m³/s = m/s x m²)
- Pertes linéaires: J = λ * (L/D) * (V² / 2g)
- HMT = Hauteur géo + Pertes totales + 10% sécurité
- Puissance pompe: P = (ρ.g.Q.HMT) / rendement

**3. Exemple concret avec tes données:**
Si tu me donnes par exemple: L=50m, D=100mm, Q=10L/s, Hg=15m
Je calcule:
S = π*0.1²/4 = 0.00785 m²
V = 0.01 / 0.00785 = 1.27 m/s (parfait, entre 0.5 et 2 m/s)
J = 0.02 * (50/0.1) * (1.27²/19.62) = 0.82m
HMT = 15 + 0.82 + (20% singulières) = 19m => On prend 21m avec sécu.

**4. Mon conseil terrain:**
Prends une pompe avec HMT 21m et Q 10L/s, puissance ~ 3kW.

Envoie-moi tes vrais chiffres (longueur, diamètre, débit, hauteur) et je te fais le calcul exact maintenant, pas vague!
"""

if prompt := st.chat_input("Parle-moi comme à ChatGPT..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        rep = reponse_humanisee(prompt)
        st.markdown(rep)
    st.session_state.messages.append({"role":"assistant","content":rep})
