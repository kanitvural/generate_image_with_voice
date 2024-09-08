import wave

import pyaudio


def record(record_active, frames):
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    while record_active.is_set():  # Multithreading
        data = stream.read(num_frames=1024, exception_on_overflow=False)
        frames.append(data)
        
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # save audiofile with same format
    audio_file = wave.open("voice_prompt.wav", "wb")
    audio_file.setnchannels(1)
    audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    audio_file.setframerate(44100)
    audio_file.writeframes(b''.join(frames))
    audio_file.close()
