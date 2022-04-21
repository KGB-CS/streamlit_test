import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

st.title("Streamlit Test")
st.write("HSV conversion")


class VideoProcessor:
    def __init__(self) -> None:
        self.Hue = 0
        self.Sat = 100
        self.Val = 100

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # 色空間をBGRからHSVに変換
        h_deg = self.Hue        # 色相(Hue)の回転度数
        s_mag = self.Sat / 100  # 彩度(Saturation)の倍率
        v_mag = self.Val / 100  # 明度(Value)の倍率

        img_hsv[:,:,(0)] = img_hsv[:,:,(0)] + h_deg     # 色相の計算
        img_hsv[:,:,(1)] = img_hsv[:,:,(1)] * s_mag     # 彩度の計算
        img_hsv[:,:,(2)] = img_hsv[:,:,(2)] * v_mag     # 明度の計算
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR) # 色空間をHSVからBGRに変
        return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
if ctx.video_processor:
    ctx.video_processor.Hue = st.slider("Hue",          min_value=0, max_value=360, step=1, value=0)
    ctx.video_processor.Sat = st.slider("Saturation",   min_value=0, max_value=100, step=1, value=100)
    ctx.video_processor.Val = st.slider("Brightness",   min_value=0, max_value=100, step=1, value=100)    