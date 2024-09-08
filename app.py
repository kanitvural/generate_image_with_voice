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
    latest_image_check = st.checkbox(label="Use last picture")

with col_image:
    st.subheader("Image Generation")
    st.divider()

    for message in st.session_state.messages:

        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar="./icons/ai_avatar.png"):
                st.warning("Here’s the image I created for you:")
                st.image(image=message["content"], width=300)
        elif message["role"] == "user":
            with st.chat_message(
                name=message["role"], avatar="./icons/user_avatar.png"
            ):
                st.success(message["content"])

    if stop_btn:
        with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
            with st.spinner("Analyzing..."):
                transcriptor = AudioTranscriptor()
                voice_prompt = transcriptor.transcribe_with_whisper(
                    audio_file_name="voice_prompt.wav"
                )
            st.success(voice_prompt)

        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        with st.chat_message(name="assistant", avatar="./icons/ai_avatar.png"):
            st.warning("Here’s the image I created for you:")

            with st.spinner("Generating your image..."):
                if latest_image_check:
                    image_generator = ImageGenerator()
                    image_file_name = image_generator.generate_image(
                        image_path=st.session_state.latest_image, prompt=voice_prompt
                    )
                else:
                    image_generator_dalle = ImageGenerator()
                    image_file_name = image_generator_dalle.generate_image_with_dalle(
                        prompt=voice_prompt
                    )

            st.image(image=image_file_name, width=300)

            with open(image_file_name, "rb") as file:
                st.download_button(
                    label="Download",
                    data=file,
                    file_name=image_file_name,
                    mime="image/png",
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": image_file_name}
        )
        st.session_state.latest_image = image_file_name
