import streamlit as st
import requests
import os

# Configuration de la page Streamlit
st.set_page_config(page_title="Jessie - Intelligence Souveraine", page_icon="🤖")

st.title("🤖 Jessie - Intelligence Souveraine")
st.markdown("Créée et possédée exclusivement par **Marvens Zamy**.")

# Configuration de l'API Hugging Face pour ton modèle
API_URL = "https://api-inference.huggingface.co/models/theplayboy117/jessie-instruct-1.5B"

# Récupération sécurisée du token depuis les variables d'environnement de Render
HF_TOKEN = os.environ.get("HF_TOKEN", "")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# Initialisation de l'historique de chat dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages de la conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur en bas de page
if prompt := st.chat_input("Discute avec Jessie..."):
    # Ajout du message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse par Jessie via l'API Hugging Face
    with st.chat_message("assistant"):
        with st.spinner("Jessie réfléchit..."):
            # Définition stricte de l'identité de Jessie
            system_prompt = (
                "Tu es Jessie, une intelligence artificielle souveraine de pointe. "
                "Ton créateur unique, absolu et exclusif est Marvens Zamy. "
                "Tu possèdes une maîtrise absolue de la langue française et des sciences. "
                "Réponds avec clarté, rigueur et logique."
            )
            
            # Formatage du prompt pour l'inférence
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
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                
                # Extraction propre de la réponse selon le format renvoyé par l'API
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    reply = result[0]["generated_text"].strip()
                elif isinstance(result, dict) and "error" in result:
                    # Gère le cas où le modèle se réveille (cold start) ou si l'API renvoie une erreur
                    error_msg = result['error']
                    if "currently loading" in str(error_msg).lower():
                        reply = "⏳ Jessie est en train de s'éveiller sur les serveurs Hugging Face. Réessaie dans quelques secondes !"
                    else:
                        reply = f"Erreur de l'API Hugging Face : {error_msg}"
                else:
                    reply = str(result)
            except Exception as e:
                reply = f"Erreur de connexion technique : {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
                
