import streamlit as st
import streamlit.components.v1 as components
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="3D Fitness Coach", layout="wide", page_icon="🏋️‍♂️")

# Egzersiz Veritabanı
WORKOUT_PLAN = [
    {
        "name": "1. Goblet Squat",
        "target": "Bacak / Kalça",
        "reps": "12 Tekrar",
        "rest_time": 60,
        "tips": "Dumbbell'ı göğsünde tut, topuklar yerde sabit, kalçayı geriye ver.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    },
    {
        "name": "2. Dumbbell Chest Press",
        "target": "Göğüs / Ön Omuz",
        "reps": "12 Tekrar",
        "rest_time": 60,
        "tips": "Sırt sehpada düz, dirsekleri gövdeye 45-60 derece açıda tut.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    },
    {
        "name": "3. Lat Pulldown",
        "target": "Sırt / Biceps",
        "reps": "12 Tekrar",
        "rest_time": 60,
        "tips": "Barı üst göğse doğru çek, çekerken kürek kemiklerini sıkıştır.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    },
    {
        "name": "4. Seated Cable Row",
        "target": "Sırt / Postür",
        "reps": "12 Tekrar",
        "rest_time": 60,
        "tips": "Gövdeyi dik tut, tutacağı alt karın bölgesine doğru çek.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    },
    {
        "name": "5. Dumbbell Shoulder Press",
        "target": "Omuz / Triceps",
        "reps": "12 Tekrar",
        "rest_time": 60,
        "tips": "Ağırlıkları baş üzerine kontrollü it, dirsekleri kitleme.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    },
    {
        "name": "6. Plank",
        "target": "Core / Karın",
        "reps": "45 Saniye",
        "rest_time": 45,
        "tips": "Vücut başından topuğa tek düz bir çizgi halinde olmalı.",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb"
    }
]

# Session State Başlatma
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "workout_started" not in st.session_state:
    st.session_state.workout_started = False
if "resting" not in st.session_state:
    st.session_state.resting = False

def render_3d_viewer(model_url):
    html_code = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
    <div style="display: flex; justify-content: center; align-items: center; background-color: #12161A; border-radius: 12px; padding: 10px;">
        <model-viewer 
            src="{model_url}" 
            alt="3D Fitness Modeli" 
            auto-rotate 
            camera-controls 
            autoplay
            shadow-intensity="1"
            style="width: 100%; height: 420px; background-color: transparent;">
        </model-viewer>
    </div>
    """
    components.html(html_code, height=450)

st.title("🏋️‍♂️ Full Body Antrenman Asistanı")

if not st.session_state.workout_started:
    st.write("Full Body 1. Ay adaptasyon programına hoş geldin. Hazır olduğunda aşağıdaki butona tıkla.")
    if st.button("🚀 Egzersize Başla", type="primary", use_container_width=True):
        st.session_state.workout_started = True
        st.rerun()

else:
    idx = st.session_state.current_index
    current_ex = WORKOUT_PLAN[idx]

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader(f"Egzersiz {idx + 1} / {len(WORKOUT_PLAN)}")
        render_3d_viewer(current_ex["model_url"])

    with col_right:
        st.header(current_ex["name"])
        st.markdown(f"**🎯 Hedef Bölge:** {current_ex['target']}")
        st.markdown(f"**🔢 Set & Tekrar:** 3 Set x {current_ex['reps']}")
        st.info(f"💡 **Form İpucu:** {current_ex['tips']}")

        st.divider()

        if not st.session_state.resting:
            if st.button("✅ Seti / Egzersizi Tamamla (Dinlenmeye Geç)", type="primary", use_container_width=True):
                st.session_state.resting = True
                st.rerun()
        else:
            st.warning("⏱️ Dinlenme Süresi Başladı...")
            progress_bar = st.progress(0)
            timer_text = st.empty()

            total_rest = current_ex["rest_time"]
            for s in range(total_rest, -1, -1):
                progress = 1 - (s / total_rest)
                progress_bar.progress(progress)
                timer_text.markdown(f"### Kalan Dinlenme: `{s}` saniye")
                time.sleep(1)

            st.session_state.resting = False
            if idx + 1 < len(WORKOUT_PLAN):
                st.session_state.current_index += 1
                st.success("Sıradaki egzersize geçiliyor!")
                time.sleep(1)
                st.rerun()
            else:
                st.balloons()
                st.success("🎉 Tebrikler! Bugünkü antrenmanı tamamladın!")
                if st.button("Yeniden Başlat"):
                    st.session_state.current_index = 0
                    st.session_state.workout_started = False
                    st.rerun()

    st.divider()
    col_prev, col_reset, col_next = st.columns(3)
    with col_prev:
        if st.button("⬅️ Önceki Hareket", disabled=(idx == 0)):
            st.session_state.current_index -= 1
            st.session_state.resting = False
            st.rerun()
    with col_reset:
        if st.button("🔄 Antrenmanı Sıfırla"):
            st.session_state.current_index = 0
            st.session_state.workout_started = False
            st.session_state.resting = False
            st.rerun()
    with col_next:
        if st.button("➡️ Sonraki Hareket", disabled=(idx == len(WORKOUT_PLAN) - 1)):
            st.session_state.current_index += 1
            st.session_state.resting = False
            st.rerun()
