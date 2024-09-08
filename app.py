import threading
import streamlit as st

from audio_transcriptor import AudioTranscriptor
from image_generator import ImageGenerator
from voice_recorder import VoiceRecorder

if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Ready!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.frames = []


def start_recording():
    st.session_state.record_active.set()  # start threading
    st.session_state.frames = []
    st.session_state.recording_status = "🔴 **Recording...**"
    st.session_state.recording_completed = False

    threading.Thread(
        target=VoiceRecorder.record,
        args=(st.session_state.record_active, st.session_state.frames),
    ).start()


def stop_recording():
    st.session_state.record_active.clear()  # stop threading
    st.session_state.recording_status = "✅ **Completed**"
    st.session_state.recording_completed = True


st.set_page_config(
    page_title="Voice2Image", layout="wide", page_icon="./icons/icon.png"
)

st.image("./icons/banner.jpg", use_column_width=True)
st.title("Voice2Image: Generates image with your voice")
st.divider()

col_audio, col_image = st.columns([1, 4])

with col_audio:
    st.subheader("Record Voice")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    subcol_left, subcol_right = st.columns([1, 2])

    with subcol_left:
        start_btn = st.button(
            label="Start",
            on_click=start_recording,
            disabled=st.session_state.record_active.is_set(),
        )
        stop_btn = st.button(
            label="Stop",
            on_click=stop_recording,
            disabled=not st.session_state.record_active.is_set(),
        )
    with subcol_right:
        recorded_audio = st.empty()

        if st.session_state.recording_completed:
            recorded_audio.audio(data="voice_prompt.wav")
            
    st.divider()
    latest_image = st.checkbox(label="Use last picture")
