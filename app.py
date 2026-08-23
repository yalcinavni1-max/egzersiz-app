import streamlit as st
import time

st.set_page_config(page_title="Fitness Workout & Rest Timer", layout="centered", page_icon="⏱️")

EXERCISE_DATABASE = {
    "Goblet Squat": {
        "target": "Bacak & Kalça",
        "reps": "12 Tekrar",
        "tips": "Dumbbell göğüste sabit, topuklar yerde, kalçayı geriye vererek çök."
    },
    "Dumbbell Chest Press": {
        "target": "Göğüs & Ön Omuz",
        "reps": "12 Tekrar",
        "tips": "Sırt sehpada düz, ağırlıkları yukarı kontrollü it, dirsekleri kilitleme."
    },
    "Lat Pulldown": {
        "target": "Sırt & Biceps",
        "reps": "12 Tekrar",
        "tips": "Barı üst göğse doğru çek, kürek kemiklerini birbirine yaklaştır."
    },
    "Seated Cable Row": {
        "target": "Sırt & Postür",
        "reps": "12 Tekrar",
        "tips": "Gövdeyi dik tut, tutacağı alt karın bölgesine çekip 1 sn sıkıştır."
    },
    "Dumbbell Shoulder Press": {
        "target": "Omuz & Triceps",
        "reps": "12 Tekrar",
        "tips": "Dirsekleri kilitlemeden ağırlıkları baş üzerine presle."
    },
    "Plank": {
        "target": "Karın & Core",
        "reps": "45 Saniye",
        "tips": "Vücut başından topuğa tek düz bir çizgi halinde olmalı, karnı sık."
    }
}

# Session State
if "view" not in st.session_state:
    st.session_state.view = "setup"
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "current_set" not in st.session_state:
    st.session_state.current_set = 1
if "selected_list" not in st.session_state:
    st.session_state.selected_list = list(EXERCISE_DATABASE.keys())
if "rest_set_seconds" not in st.session_state:
    st.session_state.rest_set_seconds = 60
if "rest_exercise_seconds" not in st.session_state:
    st.session_state.rest_exercise_seconds = 120
if "target_sets" not in st.session_state:
    st.session_state.target_sets = 3
if "rest_mode" not in st.session_state:
    st.session_state.rest_mode = None  # None | "set" | "exercise"

# ==========================================
# 1. EKRAN: KURULUM
# ==========================================
if st.session_state.view == "setup":
    st.title("⏱️ Antrenman & Dinlenme Sayacı")
    st.caption("Egzersizlerini seç, set ve dinlenme sürelerini ayarla.")

    st.markdown("### 1. Yapılacak Egzersizler")
    selected = []
    for name, data in EXERCISE_DATABASE.items():
        if st.checkbox(f"**{name}** — *{data['target']}*", value=True):
            selected.append(name)
    st.session_state.selected_list = selected

    st.divider()

    st.markdown("### 2. Antrenman ve Dinlenme Parametreleri")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.target_sets = st.number_input(
            "Set Sayısı:", 
            min_value=1, 
            max_value=8, 
            value=3
        )
    with col2:
        st.session_state.rest_set_seconds = st.slider(
            "Set Arası Dinlenme (sn):", 
            min_value=15, 
            max_value=120, 
            value=60, 
            step=5
        )
    with col3:
        st.session_state.rest_exercise_seconds = st.slider(
            "Hareket Arası Dinlenme (sn):", 
            min_value=30, 
            max_value=240, 
            value=120, 
            step=10
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Antrenmanı Başlat", type="primary", use_container_width=True):
        if not st.session_state.selected_list:
            st.error("Lütfen en az 1 egzersiz seçin!")
        else:
            st.session_state.view = "workout"
            st.session_state.current_index = 0
            st.session_state.current_set = 1
            st.session_state.rest_mode = None
            st.rerun()

# ==========================================
# 2. EKRAN: AKTİF ANTRENMAN
# ==========================================
elif st.session_state.view == "workout":
    active_exercises = st.session_state.selected_list
    current_name = active_exercises[st.session_state.current_index]
    current_data = EXERCISE_DATABASE[current_name]

    overall_progress = st.session_state.current_index / len(active_exercises)
    st.progress(overall_progress)
    st.caption(f"Genel İlerleme: Egzersiz {st.session_state.current_index + 1} / {len(active_exercises)}")

    st.title(current_name)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("🎯 Bölge", current_data["target"])
    col_b.metric("🔢 Hedef", current_data["reps"])
    col_c.metric("🔄 Set", f"{st.session_state.current_set} / {st.session_state.target_sets}")

    st.info(f"💡 **Form İpucu:** {current_data['tips']}")
    st.divider()

    # Sayaç Mantığı
    if st.session_state.rest_mode is None:
        st.subheader("💪 Set Sırası Sende!")
        st.write("Seti tamamladığında butona basarak dinlenmeyi başlat.")
        
        is_last_set = st.session_state.current_set >= st.session_state.target_sets
        button_label = "🏁 Egzersizi Tamamla (Yeni Harekete Geçiş Dinlenmesi)" if is_last_set else "✅ Set Bitti (Set Arası Dinlenme)"
        
        if st.button(button_label, type="primary", use_container_width=True):
            st.session_state.rest_mode = "exercise" if is_last_set else "set"
            st.rerun()

    else:
        is_exercise_rest = st.session_state.rest_mode == "exercise"
        total_t = st.session_state.rest_exercise_seconds if is_exercise_rest else st.session_state.rest_set_seconds
        
        if is_exercise_rest:
            st.warning("🚶‍♂️ **Hareketler Arası Geçiş & Dinlenme Süresi** (Su iç, nefeslen ve sıradaki makineye geç)")
        else:
            st.info("⏱️ **Set Arası Dinlenme Süresi**")

        progress_bar = st.progress(0.0)
        timer_box = st.empty()

        for s in range(total_t, -1, -1):
            progress_bar.progress((total_t - s) / total_t)
            timer_box.markdown(f"## ⏳ Kalan Süre: `{s}` saniye")
            time.sleep(1)

        # Dinlenme Bitişinde İlerleme
        st.session_state.rest_mode = None
        if not is_exercise_rest:
            st.session_state.current_set += 1
        else:
            st.session_state.current_set = 1
            if st.session_state.current_index + 1 < len(active_exercises):
                st.session_state.current_index += 1
            else:
                st.balloons()
                st.success("🎉 Tebrikler! Tüm antrenmanı tamamladın!")
                if st.button("Başa Dön"):
                    st.session_state.view = "setup"
                    st.rerun()
        st.rerun()

    # Alt Navigasyon
    st.divider()
    b_prev, b_home, b_next = st.columns(3)
    with b_prev:
        if st.button("⬅️ Önceki Hareket", disabled=(st.session_state.current_index == 0)):
            st.session_state.current_index -= 1
            st.session_state.current_set = 1
            st.session_state.rest_mode = None
            st.rerun()
    with b_home:
        if st.button("⚙️ Ayarlara Dön"):
            st.session_state.view = "setup"
            st.session_state.rest_mode = None
            st.rerun()
    with b_next:
        if st.button("➡️ Sonraki Hareket", disabled=(st.session_state.current_index == len(active_exercises) - 1)):
            st.session_state.current_index += 1
            st.session_state.current_set = 1
            st.session_state.rest_mode = None
            st.rerun()
