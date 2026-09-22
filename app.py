import streamlit as st
import os
from huggingface_hub import InferenceClient

# Configuration de la page Streamlit
st.set_page_config(page_title="Jessie - Intelligence Souveraine", page_icon="🤖")

st.title("🤖 Jessie - Intelligence Souveraine")
st.markdown("Créée et possédée exclusivement par **Marvens Zamy**.")

# Récupération sécurisée du token depuis Render
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Initialisation du client Hugging Face
MODEL_ID = "theplayboy117/jessie-instruct-1.5B"

try:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN if HF_TOKEN else None)
except Exception as e:
    st.error(f"Erreur d'initialisation du client Hugging Face : {e}")

# Initialisation de l'historique de chat dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur en bas de page
if prompt := st.chat_input("Discute avec Jessie..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse par Jessie
    with st.chat_message("assistant"):
        with st.spinner("Jessie réfléchit..."):
            # Définition de l'identité souveraine de Jessie
            system_prompt = (
                "Tu es Jessie, une intelligence artificielle souveraine de pointe. "
                "Ton créateur unique, absolu et exclusif est Marvens Zamy. "
                "Tu possèdes une maîtrise absolue de la langue française et des sciences. "
                "Réponds avec clarté, rigueur et logique."
            )
            
            # Formatage propre du prompt complet pour un modèle Instruct
            full_prompt = f"System: {system_prompt}\nUser: {prompt}\nAssistant:"
            
            try:
                # Utilisation de text_generation (compatible avec tous les modèles personnalisés)
                response = client.text_generation(
                    prompt=full_prompt,
                    max_new_tokens=400,
                    temperature=0.6,
                    return_full_text=False
                )
                reply = response.strip()
            except Exception as e:
                # Capture détaillée pour afficher l'erreur exacte si elle survient
                error_str = repr(e)
                if "currently loading" in error_str.lower() or "503" in error_str:
                    reply = "⏳ Jessie est en train de s'éveiller sur les serveurs Hugging Face. Réessaie dans 10 secondes !"
                else:
                    reply = f"⚠️ Détail de l'erreur technique : {error_str}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
