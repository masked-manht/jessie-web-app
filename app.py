import streamlit as st
import os
import requests

# Configuration de la page Streamlit
st.set_page_config(page_title="Jessie - Intelligence Souveraine", page_icon="🤖")

st.title("🤖 Jessie - Intelligence Souveraine")
st.markdown("Créée et possédée exclusivement par **Marvens Zamy**.")

# Récupération sécurisée du token depuis Render
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# URL de l'API Serverless de ton modèle
MODEL_ID = "theplayboy117/jessie-instruct-1.5B"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

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
            
            full_prompt = f"System: {system_prompt}\nUser: {prompt}\nAssistant:"
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 400,
                    "temperature": 0.6,
                    "return_full_text": False
                }
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                result = response.json()
                
                # Gestion des différents formats de retour possibles de l'API HF
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    reply = result[0]["generated_text"].strip()
                elif isinstance(result, dict) and "error" in result:
                    error_msg = result["error"]
                    if "currently loading" in str(error_msg).lower():
                        reply = "⏳ Jessie s'éveille sur les serveurs Hugging Face. Réessaie dans 15 secondes !"
                    else:
                        reply = f"⚠️ Erreur de l'API Hugging Face : {error_msg}"
                else:
                    reply = f"⚠️ Réponse inattendue du modèle : {str(result)}"
            except Exception as e:
                reply = f"⚠️ Erreur de connexion technique : {repr(e)}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
                    
