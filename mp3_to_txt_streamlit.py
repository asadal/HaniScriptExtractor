from tempfile import NamedTemporaryFile
import whisper
import streamlit as st
import time
import os


# whisper_model = "medium" # tiny, base, small, medium, large

@st.cache_resource
def load_whisper_model(whisper_model):
    return whisper.load_model(whisper_model)

def transcribe_audio(model, file_path):
    return model.transcribe(file_path)
# def extract_script(mp3_file):
#     with NamedTemporaryFile(suffix="mp3", delete=False) as tmp_file:
#             tmp_file.write(mp3_file.getvalue())
#             file_path = tmp_file.name
            
#             # Extract Script
#             model = st.write(load_whisper_model())
#             result = model.transcribe(file_path)
#             script = result["text"]
#             return script

def mp3_to_txt_app():
#     title nad fabicon
    st.set_page_config(page_title = "MP3 to TXT", page_icon = "🎙️")
    
#     featured image
    st.image("https://cdn.pixabay.com/photo/2017/01/31/13/50/headphones-2024215_1280.png", width=150)
    st.title("Hani Script Extractor")
    st.subheader("Convert MP3 to TXT")
    st.markdown("오픈AI의 오픈소스 인공지능 STT(Speech-to-Text) 모델인 [Whisper](https://github.com/openai/whisper)를 활용했습니다. ")
    
    # whisper model 선택
    whisper_model = st.selectbox("모델을 선택해주세요.(base나 small을 권장합니다. medium과 large는 스크립트 추출 속도가 느려지거나 오류가 날 수 있습니다.)", ('tiny', 'base', 'small', 'medium', 'large'))
    st.write("모델 : ", whisper_model) 
    st.divider()
    
    # 파일 업로드
    mp3_file = st.file_uploader("MP3 파일을 올려주세요.", type=["mp3"])
    
    if mp3_file is not None:
#         progress_text = "Operation in progress. Please wait."
#         my_bar = st.progress(0, text=progress_text)
#         for percent_complete in range(100):
#             time.sleep(0.1)
#             my_bar.progress(percent_complete + 1, text=progress_text)
#         time.sleep(3)
        try:
            with st.spinner("스크립트를 추출하고 있습니다. 잠시만 기다려주세요..."):
                with NamedTemporaryFile(suffix="mp3", delete=False) as tmp_file:
                    tmp_file.write(mp3_file.getvalue())
                    file_path = tmp_file.name
            
               # Extract Script
                model = load_whisper_model(whisper_model)
                model = whisper.load_model(whisper_model)
              # result = transcribe_audio(model, file_path)
                result = model.transcribe(file_path)
                script = result["text"]
                if script:
                    st.success("스크립트 추출 완료!")
                    st.write(script)
        except Exception as e:
            st.error("오류가 발생했습니다. 😥")
            st.write("웹페이지를 새로고침한 후 모델을 'base'나 'small'로 지정하고 재시도해보세요.")
        # 다운로드 링크 생성
        file_name = '-'.join(mp3_file.name.split(".")[:-1]) + ".txt"
        file_bytes = script.encode()
        st.download_button(label="Download Script", data=file_bytes, file_name=file_name)

if __name__ ==  "__main__":
    mp3_to_txt_app()
