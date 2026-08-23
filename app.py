import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="3D Fitness Coach", layout="wide", page_icon="🏋️‍♂️")

# Egzersiz Veritabanı (İnternet üzerinden çekilen insan 3D modelleri)
EXERCISE_DATABASE = {
    "Goblet Squat": {
        "target": "Bacak & Kalça",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "12 Tekrar",
        "tips": "Dumbbell'ı göğsünde tut, topuklar yerde sabit kalsın, kalçayı geriye vererek çök."
    },
    "Dumbbell Chest Press": {
        "target": "Göğüs & Ön Omuz",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "12 Tekrar",
        "tips": "Sırt sehpaya tam otursun, ağırlıkları göğüsten yukarı kontrollü şekilde it."
    },
    "Lat Pulldown": {
        "target": "Sırt & Biceps",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "12 Tekrar",
        "tips": "Barı üst göğse doğru çek, çekerken kürek kemiklerini birbirine yaklaştır."
    },
    "Seated Cable Row": {
        "target": "Sırt & Postür",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "12 Tekrar",
        "tips": "Gövdeyi dik tut, tutacağı alt karın bölgesine çekip 1 saniye sıkıştır."
    },
    "Dumbbell Shoulder Press": {
        "target": "Omuz & Triceps",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "12 Tekrar",
        "tips": "Dirsekleri kilitlemeden ağırlıkları baş hizasının üzerine presle."
    },
    "Plank": {
        "target": "Karın & Core",
        "model_url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
        "reps": "45 Saniye",
        "tips": "Vücut başından topuğa tek bir düz çizgi olsun, karın kaslarını sıkı tut."
    }
}

# Session State Yönetimi
if "view" not in st.session_state:
    st.session_state.view = "setup"
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "current_set" not in st.session_state:
    st.session_state.current_set = 1
if "selected_list" not in st.session_state:
    st.session_state.selected_list = list(EXERCISE_DATABASE.keys())
if "rest_seconds" not in st.session_state:
    st.session_state.rest_seconds = 60
if "target_sets" not in st.session_state:
    st.session_state.target_sets = 3
if "is_resting" not in st.session_state:
    st.session_state.is_resting = False


def render_online_3d_model(url):
    """Google Model-Viewer ile 3D GLB Modelini WebGL Üzerinde Oynatır"""
    html_code = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
        <style>
          body {{ margin: 0; padding: 0; background: transparent; }}
          model-viewer {{
            width: 100%;
            height: 440px;
            background-color: #11141a;
            border-radius: 12px;
            border: 1px solid #2d333b;
            --poster-color: transparent;
          }}
        </style>
      </head>
      <body>
        <model-viewer 
            src="{url}" 
            alt="3D Fitness Egzersiz Modeli" 
            auto-rotate 
            camera-controls 
            autoplay 
            animation-name="*"
            shadow-intensity="1.5">
        </model-viewer>
      </body>
    </html>
    """
    components.html(html_code, height=460)


# ==========================================
# 1. EKRAN: EGZERSİZ SEÇİMİ VE AYARLAR
# ==========================================
if st.session_state.view == "setup":
    st.title("🏋️‍♂️ Antrenman Planlama")
    st.write("Bugün uygulamak istediğin hareketleri seç ve dinlenme süreni belirle.")

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.subheader("📋 Egzersiz Havuzu")
        selected = []
        for name, data in EXERCISE_DATABASE.items():
            checked = st.checkbox(f"**{name}** — *{data['target']}*", value=True)
            if checked:
                selected.append(name)
        st.session_state.selected_list = selected

    with col2:
        st.subheader("⏱️ Antrenman Parametreleri")
        st.session_state.target_sets = st.number_input(
            "Hareket Başına Set Sayısı:", 
            min_value=1, 
            max_value=6, 
            value=3
        )
        st.session_state.rest_seconds = st.slider(
            "Setler Arası Dinlenme Süresi (Saniye):", 
            min_value=15, 
            max_value=120, 
            value=60, 
            step=5
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Antrenmanı Başlat", type="primary", use_container_width=True):
            if not st.session_state.selected_list:
                st.error("Lütfen en az bir egzersiz seçin!")
            else:
                st.session_state.view = "workout"
                st.session_state.current_index = 0
                st.session_state.current_set = 1
                st.session_state.is_resting = False
                st.rerun()

# ==========================================
# 2. EKRAN: CANLI 3D ANTRENMAN & SAYAÇ
# ==========================================
elif st.session_state.view == "workout":
    active_exercises = st.session_state.selected_list
    current_name = active_exercises[st.session_state.current_index]
    current_data = EXERCISE_DATABASE[current_name]

    col_3d, col_details = st.columns([1.3, 1])

    with col_3d:
        st.subheader(f"Egzersiz {st.session_state.current_index + 1} / {len(active_exercises)}")
        render_online_3d_model(current_data["model_url"])

    with col_details:
        st.header(current_name)
        st.markdown(f"**🎯 Hedef Bölge:** `{current_data['target']}`")
        st.markdown(f"**🔢 Tekrar:** `{current_data['reps']}`")
        st.markdown(f"**🔄 Set Durumu:** `{st.session_state.current_set} / {st.session_state.target_sets}`")
        st.info(f"💡 **İpucu:** {current_data['tips']}")

        st.divider()

        # Dinlenme Sayacı Kontrolü
        if not st.session_state.is_resting:
            if st.button("✅ Seti Tamamla (Dinlenmeye Geç)", type="primary", use_container_width=True):
                st.session_state.is_resting = True
                st.rerun()
        else:
            st.warning("⏱️ Dinlenme Süresi İşliyor...")
            progress_bar = st.progress(0.0)
            timer_box = st.empty()

            total_t = st.session_state.rest_seconds
            for s in range(total_t, -1, -1):
                progress_bar.progress((total_t - s) / total_t)
                timer_box.markdown(f"### Kalan Süre: `{s}` saniye")
                time.sleep(1)

            st.session_state.is_resting = False

            # Set ve Egzersiz İlerleme Mantığı
            if st.session_state.current_set < st.session_state.target_sets:
                st.session_state.current_set += 1
            else:
                st.session_state.current_set = 1
                if st.session_state.current_index + 1 < len(active_exercises):
                    st.session_state.current_index += 1
                else:
                    st.balloons()
                    st.success("🎉 Harika! Bugünkü tüm egzersizleri ve setleri tamamladın!")
                    if st.button("Başa Dön"):
                        st.session_state.view = "setup"
                        st.rerun()
            st.rerun()

    # Alt Kontrol Butonları
    st.divider()
    b_prev, b_home, b_next = st.columns(3)
    with b_prev:
        if st.button("⬅️ Önceki Egzersiz", disabled=(st.session_state.current_index == 0)):
            st.session_state.current_index -= 1
            st.session_state.current_set = 1
            st.session_state.is_resting = False
            st.rerun()
    with b_home:
        if st.button("⚙️ Ayarlara Geri Dön"):
            st.session_state.view = "setup"
            st.session_state.is_resting = False
            st.rerun()
    with b_next:
        if st.button("➡️ Sonraki Egzersiz", disabled=(st.session_state.current_index == len(active_exercises) - 1)):
            st.session_state.current_index += 1
            st.session_state.current_set = 1
            st.session_state.is_resting = False
            st.rerun()
