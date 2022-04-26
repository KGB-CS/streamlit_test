import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

# モデルファイル
cascade_path = "./data/haarcascade_frontalface_default.xml"
#cascade_path = "./data/haarcascade_frontalface_alt.xml"


st.title("Streamlit Test")
st.write("顔認識")


class VideoProcessor:
    def __init__(self) -> None:
        return

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cascade = cv2.CascadeClassifier(cascade_path)

        facerect = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

        color = (255, 255, 255)

            # 検出した場合
        if len(facerect) > 0:

            #検出した顔を囲む矩形の作成
            for rect in facerect:
                cv2.rectangle(  img, 
                                tuple(rect[0:2]), 
                                tuple(rect[0:2] + rect[2:4]),
                                color,
                                thickness=2)
    
        return av.VideoFrame.from_ndarray(img, format="bgr24")

ctx = webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
