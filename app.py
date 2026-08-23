import streamlit as st
import time

st.set_page_config(page_title="Fitness Workout Planner & Timer", layout="centered", page_icon="🏋️‍♂️")

# Kas Gruplarına Göre Alternatif Egzersiz Havuzu
EXERCISE_CATALOG = {
    "🦵 Bacak & Kalça": {
        "Goblet Squat (Dumbbell)": {"reps": "10-12 Tekrar", "tips": "Dumbbell göğüste sabit, topuklar yerde, kalçayı geriye vererek çök."},
        "Leg Press (Makine)": {"reps": "10-12 Tekrar", "tips": "Ayakları omuz genişliğinde koy, dizleri içeri bükme, tepe noktada dizleri kilitleme."},
        "Bodyweight Squat": {"reps": "12-15 Tekrar", "tips": "Kendi ağırlığınla kontrollü çök, göğsü dik tut."},
        "Dumbbell Lunge": {"reps": "10 Tekrar (Her Bacak)", "tips": "Öne adım atarken öndeki dizin ayak parmağını geçmemesine dikkat et."},
        "Leg Extension (Makine)": {"reps": "12 Tekrar", "tips": "Ön bacak kaslarını tepe noktada 1 saniye sıkıştır."}
    },
    "🧱 Göğüs": {
        "Dumbbell Chest Press": {"reps": "10-12 Tekrar", "tips": "Sırt sehpada düz, ağırlıkları yukarı kontrollü it, omuzları geriye kilitle."},
        "Machine Chest Press": {"reps": "10-12 Tekrar", "tips": "Tutacakları göğüs hizasına ayarla, kontrollü itiş yap."},
        "Incline Dumbbell Press": {"reps": "10-12 Tekrar", "tips": "Üst göğüs odaklı; 30-45 derece eğimli sehpada kontrollü bas."},
        "Push-up (Şınav / Diz Üstü Şınav)": {"reps": "8-12 Tekrar", "tips": "Gövde düz bir hat üzerinde kalsın, dirsekleri vücuda 45 derece tut."}
    },
    "🦅 Sırt": {
        "Lat Pulldown": {"reps": "10-12 Tekrar", "tips": "Barı üst göğse çek, çekerken kürek kemiklerini birbirine yaklaştır."},
        "Seated Cable Row": {"reps": "10-12 Tekrar", "tips": "Gövde dik, tutacağı alt karın bölgesine çekip 1 sn sıkıştır."},
        "Dumbbell One-Arm Row": {"reps": "10-12 Tekrar", "tips": "Sehpaya tek dizini koy, sırtını düz tutarak dumbbell'ı kalçana doğru çek."},
        "Chest Supported Machine Row": {"reps": "10-12 Tekrar", "tips": "Göğsünü pede yasla, beli oynatmadan sadece sırt kaslarıyla çekiş yap."},
        "Straight Arm Pulldown": {"reps": "12 Tekrar", "tips": "Kolları çok hafif kırık tutarak barı uyluklarına doğru indir."}
    },
    "🛡️ Omuz": {
        "Dumbbell Shoulder Press": {"reps": "10-12 Tekrar", "tips": "Sırt destekli otur, dirsekleri kilitlemeden baş üzerine presle."},
        "Machine Shoulder Press": {"reps": "10-12 Tekrar", "tips": "Kolları kontrollü şekilde yukarı uzat, inerken kulak hizasında dur."},
        "Dumbbell Lateral Raise": {"reps": "12-15 Tekrar", "tips": "Hafif kilo kullan, kolları yana açarken dirsekleri hafif kırık tut."},
        "Face Pull (Kablo / Halat)": {"reps": "12-15 Tekrar", "tips": "Arka omuz ve postür için halatı alnına doğru çek ve dirsekleri yukarıda tut."}
    },
    "💪 Kollar (Ön & Arka Kol)": {
        "Dumbbell Biceps Curl": {"reps": "12 Tekrar", "tips": "Dirsekleri gövdeye sabitle, savurma yapmadan sadece ön kolu kaldır."},
        "Rope Triceps Pushdown": {"reps": "12 Tekrar", "tips": "Dirsekleri sabit tut, halatı aşağı iterken en altta hafifçe iki yana aç."},
        "Cable Biceps Curl": {"reps": "12 Tekrar", "tips": "Sürekli gerilim sağlamak için dirsekleri kıpırdatmadan barı yukarı bük."},
        "Dumbbell Overhead Triceps Extension": {"reps": "12 Tekrar", "tips": "Tek bir dumbbell'ı başının arkasından yukarı doğru uzat."}
    },
    "🧘 Karın & Core": {
        "Plank": {"reps": "30-45 Saniye", "tips": "Vücut başından topuğa tek düz bir çizgi halinde olmalı, karnı sıkı tut."},
        "Deadbug": {"reps": "12 Tekrar", "tips": "Sırt üstü uzan, beli yere tam yapıştır, zıt kol ve bacağı kontrollü uzat."},
        "Hanging Knee Raise": {"reps": "10-12 Tekrar", "tips": "Dizlerini göğsüne doğru kontrollü çek, sallanmamaya çalış."}
    }
}

# Session State Başlatma
if "view" not in st.session_state:
    st.session_state.view = "setup"
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "current_set" not in st.session_state:
    st.session_state.current_set = 1
if "workout_queue" not in st.session_state:
    st.session_state.workout_queue = []
if "rest_set_seconds" not in st.session_state:
    st.session_state.rest_set_seconds = 60
if "rest_exercise_seconds" not in st.session_state:
    st.session_state.rest_exercise_seconds = 120
if "target_sets" not in st.session_state:
    st.session_state.target_sets = 3
if "rest_mode" not in st.session_state:
    st.session_state.rest_mode = None

# ==========================================
# 1. EKRAN: BÖLGE VE ALTERNATİF HAREKET SEÇİMİ
# ==========================================
if st.session_state.view == "setup":
    st.title("🏋️ Kişisel Antrenmanını Oluştur")
    st.caption("Her kas grubu için yapmak istediğin egzersizi seç.")

    st.markdown("### 1. Egzersiz Alternatifleri")
    
    # Form kullanarak seçimlerin kaybolmasını önleme
    with st.form("workout_setup_form"):
        temp_selections = {}
        for group_name, exercises in EXERCISE_CATALOG.items():
            st.markdown(f"**{group_name}**")
            options = ["(Bu Bölgeyi Pas Geç)"] + list(exercises.keys())
            # Varsayılan olarak her grubun 1. egzersizini seç
            temp_selections[group_name] = st.selectbox(
                f"{group_name} seçimi", 
                options, 
                index=1, 
                label_visibility="collapsed"
            )

        st.divider()
        st.markdown("### 2. Set ve Dinlenme Ayarları")
        col1, col2, col3 = st.columns(3)
        with col1:
            t_sets = st.number_input("Set Sayısı:", min_value=1, max_value=8, value=3)
        with col2:
            r_set = st.slider("Set Arası Dinlenme (sn):", min_value=15, max_value=120, value=60, step=5)
        with col3:
            r_ex = st.slider("Hareket Arası Dinlenme (sn):", min_value=30, max_value=240, value=120, step=10)

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("🚀 Seçtiğim Antrenmanı Başlat", type="primary", use_container_width=True)

        if submit_btn:
            queue = []
            for g_name, choice in temp_selections.items():
                if choice != "(Bu Bölgeyi Pas Geç)":
                    queue.append({
                        "group": g_name,
                        "name": choice,
                        "reps": EXERCISE_CATALOG[g_name][choice]["reps"],
                        "tips": EXERCISE_CATALOG[g_name][choice]["tips"]
                    })

            if not queue:
                st.error("Lütfen en az bir bölgeden hareket seçin!")
            else:
                st.session_state.workout_queue = queue
                st.session_state.target_sets = t_sets
                st.session_state.rest_set_seconds = r_set
                st.session_state.rest_exercise_seconds = r_ex
                st.session_state.current_index = 0
                st.session_state.current_set = 1
                st.session_state.rest_mode = None
                st.session_state.view = "workout"
                st.rerun()

# ==========================================
# 2. EKRAN: AKTİF ANTRENMAN & SAYAÇ
# ==========================================
elif st.session_state.view == "workout":
    queue = st.session_state.workout_queue

    # Dizin Güvenlik Kontrolü (IndexError Koruması)
    if not queue:
        st.session_state.view = "setup"
        st.rerun()

    if st.session_state.current_index >= len(queue):
        st.session_state.current_index = len(queue) - 1

    curr = queue[st.session_state.current_index]

    overall_progress = (st.session_state.current_index) / len(queue)
    st.progress(overall_progress)
    st.caption(f"Antrenman İlerlemesi: Egzersiz {st.session_state.current_index + 1} / {len(queue)}")

    st.title(curr["name"])

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("🎯 Bölge", curr["group"])
    col_b.metric("🔢 Hedef Tekrar", curr["reps"])
    col_c.metric("🔄 Set", f"{st.session_state.current_set} / {st.session_state.target_sets}")

    st.info(f"💡 **Form İpucu:** {curr['tips']}")
    st.divider()

    if st.session_state.rest_mode is None:
        st.subheader("💪 Set Sırası Sende!")
        st.write("Seti tamamladığında butona basarak dinlenmeyi başlat.")
        
        is_last_set = st.session_state.current_set >= st.session_state.target_sets
        button_label = "🏁 Hareketi Bitir (Sıradaki Egzersize Geçiş)" if is_last_set else "✅ Set Bitti (Set Dinlenmesi)"
        
        if st.button(button_label, type="primary", use_container_width=True):
            st.session_state.rest_mode = "exercise" if is_last_set else "set"
            st.rerun()

    else:
        is_exercise_rest = st.session_state.rest_mode == "exercise"
        total_t = st.session_state.rest_exercise_seconds if is_exercise_rest else st.session_state.rest_set_seconds
        
        if is_exercise_rest:
            st.warning("🚶‍♂️ **Hareketler Arası Dinlenme & İstasyon Değişimi**")
        else:
            st.info("⏱️ **Set Arası Dinlenme**")

        progress_bar = st.progress(0.0)
        timer_box = st.empty()

        for s in range(total_t, -1, -1):
            progress_bar.progress((total_t - s) / total_t)
            timer_box.markdown(f"## ⏳ Kalan Süre: `{s}` saniye")
            time.sleep(1)

        st.session_state.rest_mode = None
        if not is_exercise_rest:
            st.session_state.current_set += 1
        else:
            st.session_state.current_set = 1
            if st.session_state.current_index + 1 < len(queue):
                st.session_state.current_index += 1
            else:
                st.balloons()
                st.success("🎉 Tebrikler! Bugünkü antrenmanı başarıyla bitirdin!")
                if st.button("Yeniden Planla"):
                    st.session_state.view = "setup"
                    st.rerun()
        st.rerun()

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
        if st.button("➡️ Sonraki Hareket", disabled=(st.session_state.current_index == len(queue) - 1)):
            st.session_state.current_index += 1
            st.session_state.current_set = 1
            st.session_state.rest_mode = None
            st.rerun()
