import streamlit as st 

st.title("Streamlit 기본 API 살펴보기")
st.header("Input widgets") 
# Widget (Window(창) + Gadget(도구) -> 화면상에서 사용자가 클릭하거나 값을 입력할 수 있게 해주는 작은 조작 도구들)

st.button("버튼")
st.success("clicked button") 

st.link_button("Go to gallery", "https://streamlit.io/gallery")

ml_radio = st.radio(
    "머신러닝 방법", 
    ("신경망", "랜덤포레스트", "SVM"), 
    index=1 # 인데스 1인 "랜덤포레스트"를 기본 선택값으로 지정
)
st.info(f"나의 선택 : {ml_radio}")
st.checkbox("토큰화")

ml_select = st.selectbox(
    "머신러닝 방법", 
    ("SVM", "랜덤포레스트", "신경망")
)
st.info(ml_select)

ml_method_multi = st.multiselect(
    "머신러닝 방법", 
    ["랜덤포레스트", "신경망", "SVM"], 
    default=["랜덤포레스트"] 
)

if ml_method_multi:
    st.info(ml_method_multi)

weight = st.slider("가중치", 0, 10, 5) # 최소 0, 최대 10, 기본값 5
st.info(f"가중치 : {weight}")