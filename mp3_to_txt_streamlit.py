from tempfile import NamedTemporaryFile
import whisper
import streamlit as st
import time

whisper_model = "medium" # tiny, base, small, medium, large

def extract_script(mp3_file):
    with NamedTemporaryFile(suffix="mp3") as temp:
            temp.write(mp3_file.getvalue())
            temp.seek(0)
            model = whisper.load_model(whisper_model)
            result = model.transcribe(temp.name)
            script = result["text"]
            return script

def mp3_to_txt_app():
    st.title("Hani Script Extractor")
    st.subheader("Convert MP3 to TXT")
    # 파일 업로드
    mp3_file = st.file_uploader("Upload MP3", type=["mp3"])
    if mp3_file is not None:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text=progress_text)
        script = extract_script(mp3_file)
        st.write(script)

        # 다운로드 링크 생성
        file_name = '-'.join(mp3_file.name.split(".")[:-1]) + ".txt"
        file_bytes = script.encode()
        st.download_button(label="Download Script", data=file_bytes, file_name=file_name)

if __name__ ==  "__main__":
    mp3_to_txt_app()
