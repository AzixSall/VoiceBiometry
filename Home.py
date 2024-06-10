import streamlit as st
from speechbrain.inference.speaker import SpeakerRecognition
import os

st.set_page_config(
        page_title="Acceuil",
        page_icon="👋",
)

st.write("# Démo de voice Biometry - PCCI!")

st.markdown(
    """
    Bienvenue sur cette demo portant sur l'identification d'une personne
    en se basant sur sa voix, merci de uploader les deux enregistrements de voix que vous voulez comparer
    le systeme determinera automatiquement s'il sagit de la meme personne qui parle
"""
)

authentication_method = st.selectbox("Choississez une option", ["Enrollement", "Authentification"])

data_folder = "Data"
data_temp = "Temp"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

if not os.path.exists(data_temp):
    os.makedirs(data_temp)

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

# Create an input box based on the dropdown selection
if authentication_method == "Enrollement":
    st.write("### Creer un compte avec votre empreinte vocale")
    user_input = st.text_input("Entrer votre nom (sans espace ni caracteres speciales)")
    uploaded_file = st.file_uploader("Uploader un enregistrement de votre voix", type=["wav"])
    if uploaded_file is not None:
        if st.button('Enrollement'):
            file_path = os.path.join(data_folder, f'{user_input}_{uploaded_file.name}')
            with open(f'{file_path}', "wb") as f:
                f.write(uploaded_file.getvalue())
            st.info("Enrollement effectue avec succes, merci de choisir l'option Authentification pour vous authentifier.")
            st.session_state["uploader"] = None
    else:
        st.info("Merci de mettre un audio.")
        
elif authentication_method == "Authentification":
    # If "Verification" is selected, create a disabled input box
    st.write("### Authentifiez-vous avec votre empreinte vocale")
    #name = st.text_input("Entrer votre nom ", disabled=True)

    uploaded_file = st.file_uploader("Uploader un enregistrement de votre voix", type=["wav"])

    if uploaded_file is not None:
        if st.button('Connexion'):
            file_path_to_compare = os.path.join(data_temp, uploaded_file.name)
            with open(f'{file_path_to_compare}', "wb") as f:
                f.write(uploaded_file.getvalue())

            data_folder = "Data"
            files_in_data = os.listdir(data_folder)

            for file in files_in_data:
                file_path = os.path.join(data_folder, file)
                score, prediction = verification.verify_files(file_path_to_compare, file_path)
                st.write(f'My temp file {file_path_to_compare} comparing to {file_path} : score {score} - meme personne? : {prediction}')
                
                if prediction.item():
                    directory, file_name = os.path.split(file_path)
                    speaker_id, recording_id = file_name.split("_")
                    st.info(f'Vous etes {speaker_id}')
                    #st.info(f'Vous etes {file_path.split('_')[0].split('/')[0]}')
                    break

            st.session_state["uploader"] = None
    else:
        st.info("Merci de mettre un audio.")
        
else:
    st.write("### Option indisponible")



