import streamlit as st
import time

st.set_page_config(page_title="Fitness & Kalori Koçu", layout="centered", page_icon="🏋️‍♂️")

# ==========================================
# VERİTABANLARI: EGZERSİZ VE BESLENME
# ==========================================
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
    "💪 Biceps (Ön Kol)": {
        "Dumbbell Biceps Curl": {"reps": "10-12 Tekrar", "tips": "Dirsekleri gövdeye sabitle, beli sallamadan sadece ön kolu kaldır."},
        "Hammer Curl (Dumbbell)": {"reps": "10-12 Tekrar", "tips": "Avuç içleri birbirine baksın; hem ön kolu hem de kolun kalınlığını hedefler."},
        "Cable Biceps Curl": {"reps": "12 Tekrar", "tips": "Kablo gerilimiyle dirsekleri sabit tutarak barı göğse doğru çek."},
        "Concentration Curl": {"reps": "10 Tekrar (Her Kol)", "tips": "Dirseğini uyluğuna daya, tüm yükü biceps kasına odakla."}
    },
    "🦾 Triceps (Arka Kol)": {
        "Rope Triceps Pushdown": {"reps": "12 Tekrar", "tips": "Dirsekleri gövdeye yapıştır, halatı aşağı iterken en altta iki yana aç."},
        "Straight Bar Pushdown": {"reps": "10-12 Tekrar", "tips": "Düz barı göğüs hizasından aşağı düz bir çizgi halinde it."},
        "Dumbbell Overhead Triceps Extension": {"reps": "10-12 Tekrar", "tips": "Tek dumbbell'ı iki elle baş arkasından yukarı doğru presle."},
        "Bench Dips": {"reps": "10-12 Tekrar", "tips": "Elleri sehpa kenarına koy, dirsekleri geriye bükerek gövdeyi indir ve it."}
    },
    "🧘 Karın & Core": {
        "Plank": {"reps": "30-45 Saniye", "tips": "Vücut başından topuğa tek düz bir çizgi halinde olmalı, karnı sıkı tut."},
        "Deadbug": {"reps": "12 Tekrar", "tips": "Sırt üstü uzan, beli yere tam yapıştır, zıt kol ve bacağı kontrollü uzat."},
        "Hanging Knee Raise": {"reps": "10-12 Tekrar", "tips": "Dizlerini göğsüne doğru kontrollü çek, sallanmamaya çalış."}
    }
}

DINNER_OPTIONS = {
    "--- EV YEMEĞİ SEÇENEKLERİ ---": {"cal": 0, "protein": 0, "carb": 0, "fat": 0},
    "Ev: Izgara Köfte/Et (250g) + Fırın Patates + Ayran": {"cal": 680, "protein": 52, "carb": 40, "fat": 32},
    "Ev: Tavuk Göğsü (250g) + Bulgur Pilavı + Yoğurt": {"cal": 590, "protein": 60, "carb": 48, "fat": 14},
    "Ev: Fırın Somon/Balık (250g) + Mercimek Çorbası + Salata": {"cal": 560, "protein": 48, "carb": 30, "fat": 24},
    "Ev: Etli Sebze Yemeği + Karabuğday Pilavı + Cacık": {"cal": 520, "protein": 38, "carb": 45, "fat": 20},
    "Ev: Çift Kutu Ton Balıklı Büyük Salata + 1 Dilim Ekmek": {"cal": 490, "protein": 54, "carb": 28, "fat": 16},
    "--- AVM & DIŞARI SEÇENEKLERİ ---": {"cal": 0, "protein": 0, "carb": 0, "fat": 0},
    "AVM: Tavuk Dünyası (Kekiklim/Barbekü - Çift Salata & Sossuz) + Ayran": {"cal": 540, "protein": 52, "carb": 15, "fat": 28},
    "AVM: Tavuk Dünyası (Standart Menü - Kremalı Makarna & Soslu Tavuk)": {"cal": 920, "protein": 46, "carb": 85, "fat": 42},
    "AVM: Köfteci / Izgaracı (Porsiyon Köfte + Közlenmiş Sebze + Ayran)": {"cal": 620, "protein": 44, "carb": 18, "fat": 40},
    "AVM: Tabak Tavuk Döner (Pilavsız/Ekmeksiz) + Salata + Ayran": {"cal": 510, "protein": 48, "carb": 12, "fat": 28},
    "AVM: Tabak Et Döner (Pilavsız/Ekmeksiz) + Salata + Ayran": {"cal": 580, "protein": 45, "carb": 10, "fat": 38},
    "AVM: Izgara Tavuk Burger (Tek / Patatessiz / Ayran ile)": {"cal": 480, "protein": 36, "carb": 42, "fat": 16},
    "AVM: Çorbacı & Ev Yemeği (Mercimek Çorba + Tas Kebabı + Yoğurt)": {"cal": 570, "protein": 42, "carb": 32, "fat": 26},
    "AVM: Fast Food Menü (Klasik Burger + Patates Kızartması + Kola)": {"cal": 1150, "protein": 28, "carb": 135, "fat": 52}
}

# Session State Değişkenleri
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
# SOL MENÜ
# ==========================================
st.sidebar.title("⚡ Menü")
app_mode = st.sidebar.radio("Mod Seçiniz:", ["⏱️ Antrenman & Sayaç", "🥗 Günlük Beslenme & Kalori"])

# ==============================================================================
# MODÜL 1: BESLENME & KALORİ TAKİBİ
# ==============================================================================
if app_mode == "🥗 Günlük Beslenme & Kalori":
    st.title("🥗 Günlük Kalori & Makro Takibi")
    st.caption("2 Öğün + Ara Öğün Düzenine Göre Canlı Kalori Dengesi")

    DAILY_CALORIE_TARGET = 2300
    DAILY_PROTEIN_TARGET = 160

    st.markdown("### 1. Öğün: Standart Kahvaltın")
    col_k1, col_k2 = st.columns([3, 1])
    with col_k1:
        st.markdown("""
        * **Yoğurtlu Yulaf Kasesi:** 200g Yoğurt + 4-5 YK Yulaf + Kuru Nane & Tuz
        * **Protein:** 3 Adet Yumurta (Haşlama / Omlet)
        * **İçecek:** 1 Büyük Bardak Iced Americano (Sade)
        """)
    with col_k2:
        st.metric("Kalori", "520 kcal")
        st.caption("Protein: 33g | Karb: 36g | Yağ: 23g")

    st.divider()

    st.markdown("### Ara Öğün / İkindi Köprüsü")
    col_a1, col_a2 = st.columns([3, 1])
    with col_a1:
        eat_snack = st.checkbox("Ara öğünü tükettim (1 Avuç Kuruyemiş + 1 Muz + Sade Maden Suyu)", value=True)
    with col_a2:
        if eat_snack:
            st.metric("Kalori", "280 kcal")
            st.caption("Protein: 6g | Karb: 32g | Yağ: 14g")
        else:
            st.metric("Kalori", "0 kcal")

    st.divider()

    st.markdown("### 2. Öğün: Akşam Yemeği Seçimi")
    st.caption("Bugün evde mi yedin yoksa AVM'de mi? Menünü seç:")
    
    dinner_choice = st.selectbox("Akşam Yemeği Menüsü:", list(DINNER_OPTIONS.keys()), index=7)
    dinner_data = DINNER_OPTIONS[dinner_choice]

    total_cal = 520
    total_protein = 33
    total_carb = 36
    total_fat = 23

    if eat_snack:
        total_cal += 280
        total_protein += 6
        total_carb += 32
        total_fat += 14

    total_cal += dinner_data["cal"]
    total_protein += dinner_data["protein"]
    total_carb += dinner_data["carb"]
    total_fat += dinner_data["fat"]

    st.divider()
    st.subheader("📊 Günlük Toplam Değerlerin")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Toplam Kalori", 
        f"{total_cal} kcal", 
        delta=f"{DAILY_CALORIE_TARGET - total_cal} bütçe kaldı" if total_cal <= DAILY_CALORIE_TARGET else f"{total_cal - DAILY_CALORIE_TARGET} aşıldı", 
        delta_color="inverse" if total_cal > DAILY_CALORIE_TARGET else "normal"
    )
    c2.metric(
        "Protein", 
        f"{total_protein} g", 
        delta=f"{total_protein - DAILY_PROTEIN_TARGET} g" if total_protein >= DAILY_PROTEIN_TARGET else f"{DAILY_PROTEIN_TARGET - total_protein} g eksik"
    )
    c3.metric("Karbonhidrat", f"{total_carb} g")
    c4.metric("Sağlıklı Yağ", f"{total_fat} g")

    cal_progress = min(total_cal / DAILY_CALORIE_TARGET, 1.0)
    st.progress(cal_progress)

    if total_cal > DAILY_CALORIE_TARGET:
        st.error(f"⚠️ Hedef kaloriyi {total_cal - DAILY_CALORIE_TARGET} kcal aştın!")
    elif total_cal >= DAILY_CALORIE_TARGET - 250:
        st.success("🎯 Harika! Hedef kalori ve yağ yakım aralığındasın.")
    else:
        st.info("💡 Kalori açığın oldukça iyi seviyede.")

# ==============================================================================
# MODÜL 2: ANTRENMAN VE SAYAÇ
# ==============================================================================
elif app_mode == "⏱️ Antrenman & Sayaç":
    if st.session_state.view == "setup":
        st.title("🏋️ Antrenman Planlama")
        st.caption("Bölgelerden o günkü hareketlerini seç ve antrenmanı başlat.")

        with st.form("workout_setup_form"):
            temp_selections = {}
            for group_name, exercises in EXERCISE_CATALOG.items():
                st.markdown(f"**{group_name}**")
                options = ["(Bu Bölgeyi Pas Geç)"] + list(exercises.keys())
                temp_selections[group_name] = st.selectbox(
                    f"{group_name} seçimi", 
                    options, 
                    index=1, 
                    label_visibility="collapsed"
                )

            st.divider()
            st.markdown("### Set ve Dinlenme Ayarları")
            col1, col2, col3 = st.columns(3)
            with col1:
                t_sets = st.number_input("Set Sayısı:", min_value=1, max_value=8, value=3)
            with col2:
                r_set = st.slider("Set Arası Dinlenme (sn):", min_value=15, max_value=120, value=60, step=5)
            with col3:
                r_ex = st.slider("Hareket Arası Dinlenme (sn):", min_value=30, max_value=240, value=120, step=10)

            submit_btn = st.form_submit_button("🚀 Antrenmanı Başlat", type="primary", use_container_width=True)

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
                    st.session_state.target_sets = int(t_sets)
                    st.session_state.rest_set_seconds = int(r_set)
                    st.session_state.rest_exercise_seconds = int(r_ex)
                    st.session_state.current_index = 0
                    st.session_state.current_set = 1
                    st.session_state.rest_mode = None
                    st.session_state.view = "workout"
                    st.rerun()

    elif st.session_state.view == "workout":
        queue = st.session_state.workout_queue

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
        col_b.metric("🔢 Hedef", curr["reps"])
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
