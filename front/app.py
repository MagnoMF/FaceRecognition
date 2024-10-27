import streamlit as st
import cv2
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer
import asyncio
import httpx
import plotly.express as px
import pandas as pd
import os
import requests
import re

st.set_page_config(
    page_title="Face Recognition",
    page_icon=":camera_with_flash:",
)
api_url = "http://localhost:8080"
# st.session_state.api_response = [12, 2, "eu"]
# st.session_state.page = "dash_board_page"
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None
        self.sn_await = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.response = None
        self.first_detection = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            if len(faces) > 0 and not self.sn_await:
                self.sn_await = True
                self.first_detection = True
                asyncio.create_task(self.send_request(img))
        
        if self.first_detection:
            self.frame = img

        return frame

    async def send_request(self, img):
        try:
            _, img_encoded = cv2.imencode('.jpg', img)
            img_binary = img_encoded.tobytes()
            files = {'img_upload': ('image.jpg', img_binary, 'image/jpeg')}
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{api_url}/auth_user", files=files)
                self.sn_await = False
                if response.status_code == 200:
                    self.response = response.json()
        except httpx.HTTPError as e:
            self.sn_await = False
            print(f"Erro ao processar a imagem. {e}")
            print(e)

if "page" in st.session_state and st.session_state.page == "dash_board_page":
    st.title(f"Olá, {st.session_state.api_response[2]}. Seja bem-vindo(a)!")
    path = os.path.join(os.path.dirname(__file__), './database/database_airquality.xlsx')
    sn_path = os.path.exists(path)
    if(not sn_path):
        st.write("Planilha de dados não encontrada")
    df = pd.read_excel(path, sheet_name="Update 2024 (V6.1)", engine="openpyxl")
    # st.write(st.session_state.api_response)
    city_filter = st.session_state.api_response[1]
    df = df[(df["iso3"] == "BRA") & (df["city"] == city_filter)]
    df = df[["year", "no2_concentration"]]
    fig = fig = px.bar(df, x='year', y='no2_concentration', title=f"Concentração de CO2 por ano em {city_filter}")
    st.plotly_chart(fig)

else:
    st.title("Captura de Webcam e Reconhecimento Facial com Streamlit")

    # Create a placeholder to display the processed frame and response
    image_placeholder = st.empty()
    response_placeholder = st.empty()
    st.subheader("Reconhecimento de pessoas já cadastradas")
    st.write("Clique em start para iniciar o reconhecimento")
    webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
    if webrtc_ctx.video_processor:
        while True:
            if webrtc_ctx.video_processor.first_detection:
                if webrtc_ctx.video_processor.response:
                    st.session_state.api_response = webrtc_ctx.video_processor.response
                    response_placeholder.write(webrtc_ctx.video_processor.response)
                    st.session_state.page = "dash_board_page"
                    st.rerun()
            import time
            time.sleep(0.1)
    st.subheader("Cadastrar nova foto")
    cityes = ['Sao Bernardo Do Campo/BRA', 'Ribeirao Preto/BRA', 'Madre De Deus/BRA', 'Betim/BRA', 'Resende/BRA', 'Diadema/BRA', 'Paulinia/BRA', 'Salvador/BRA', 'Nova Iguacu/BRA', 'Aracatuba/BRA', 'Sao Paulo/BRA', 'Maua/BRA', 'Quatis/BRA', 'Santa Gertrudes/BRA', 'Vitoria/BRA', 'Dias D Avila/BRA', 'Taboao Da Serra/BRA', 'Seropedica/BRA', 'Araraquara/BRA', 'Cariacica/BRA', 'Cantagalo Euclidelandia/BRA', 'Sao Caetano Do Sul/BRA', 'Sao Jose Do Rio Preto/BRA', 'Cordeiripolis/BRA', 'Jai/BRA', 'Cantagalo/BRA', 'Macuco/BRA', 'Campinas/BRA', 'Carapicuiba/BRA', 'Santo Andre/BRA', 'Americana/BRA', 'Candeias/BRA', 'Guapimirim/BRA', 'Niteroi/BRA', 'Belo Horizonte/BRA', 'Itaguai/BRA', 'Jaboticabal/BRA', 'Canoas/BRA', 'Cubatao/BRA', 'Charqueadas/BRA', 'Araucaria/BRA', 'Camacari/BRA', 'Rio Claro/BRA', 'Japeri/BRA', 'Porto Real/BRA', 'Osasco/BRA', 'Piracicaba/BRA', 'Pirassununga/BRA', 'Regiao Metropolitana De Sao Paulo/BRA', 'Santos/BRA', 'Tatui/BRA', 'Nilopolis/BRA', 'Sao Joao De Meriti/BRA', 'Macae/BRA', 'Marilia/BRA', 'Rio De Janeiro/BRA', 'Catanduva/BRA', 'Duque De Caxias/BRA', 'Presidente Prudente/BRA', 'Campos/BRA', 'Ibirite/BRA', 'Barra Mansa/BRA', 'Sao Goncalo/BRA', 'Gravatai/BRA', 'Colombo/BRA', 'Jundiai/BRA', 'Sorocaba/BRA', 'Esteio/BRA', 'Limeira/BRA', 'Serra/BRA', 'Brasilia/BRA', 'Curitiba/BRA', 'Regiao Metropolitana Do Rio De Janeiro/BRA', 'Volta Redonda/BRA', 'Malemba/BRA', 'Vila Velha/BRA', 'Sao Jose Dos Campos/BRA', 'Campos Dos Goitacazes/BRA', 'Guarulhos/BRA', 'Jacarei/BRA', 'Jau/BRA', 'Bauru/BRA', 'Itaborai/BRA']
    name = st.text_input("Nome")
    pattern = r"^[A-Za-zÀ-ÿ\s]+$"
    valid_name = bool(re.match(pattern=pattern, string=name))
    if(not valid_name):
        st.warning("Digite apenas o primeiro nome")
    city = st.selectbox("Selecione a cidade", cityes)
    uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        if st.button("Enviar para API"):
            files = {"img_upload": uploaded_file.getvalue()}
            response = requests.post(f"{api_url}/create_user?ds_name={name}&city={city}", files=files)
            if(response.status_code != 200):
                st.error(response.json()["detail"])
            else: 
                st.success("Face cadastrada com sucesso ")
                info = response.json()
                card_html = f"""
                    <div style="
                        padding: 1.5rem;
                        margin-top: 1rem;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                        background-color: #262730;
                    ">
                        <h4>Usuário: {info['ds_name']}</h4>
                        <p><strong>Cidade:</strong> {info['city']}</p>
                        <p><strong>Data de Criação:</strong> {info['create_date']}</p>
                    </div>
                    """

                # Exibe o card no Streamlit
                st.markdown(card_html, unsafe_allow_html=True)