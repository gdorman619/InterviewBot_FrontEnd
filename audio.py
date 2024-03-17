from pvrecorder import PvRecorder
import wave
import struct


def record_user_audio():

    for index, device in enumerate(PvRecorder.get_available_devices()):
        print(f"[{index}] {device}")
        
    print("")
        
    mic_input = int(input("Enter the number for the respective audio device that should be used: "))

    recorder = PvRecorder(device_index=mic_input, frame_length=512)

    audio = []

    try:
        recorder.start()
        print("")
        print("Recording has started. Press Ctrl+C to stop the recording.")

        while True:
            frame = recorder.read()
            audio.extend(frame) 
    except KeyboardInterrupt:
        print("Recording Stopped. Saving File.")
        print("")
        recorder.stop()
        with wave.open("User Recording.wav", 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()
