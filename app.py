import streamlit as st
import streamlit.components.v1 as components
import time

# Sayfa Yapılandırması
st.set_page_config(
    page_title="3D Pro Fitness Coach",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tüm Egzersizler Veritabanı
ALL_EXERCISES = [
    {
        "id": "squat",
        "name": "1. Goblet Squat",
        "target": "Bacak / Kalça / Core",
        "default_reps": "3 Set x 12 Tekrar",
        "tips": "Dumbbell'ı göğsünde tut, topuklar yerde sabit. Kalçayı geriye verip sandalye gibi otur.",
        "equipment": "Dumbbell"
    },
    {
        "id": "chest_press",
        "name": "2. Dumbbell Chest Press",
        "target": "Göğüs / Ön Omuz / Triceps",
        "default_reps": "3 Set x 12 Tekrar",
        "tips": "Sırt sehpada düz durmalı. Ağırlıkları yukarı iterken göğüs kaslarını sıkıştır.",
        "equipment": "Dumbbell & Sehpa"
    },
    {
        "id": "lat_pulldown",
        "name": "3. Lat Pulldown",
        "target": "Sırt / Biceps",
        "default_reps": "3 Set x 12 Tekrar",
        "tips": "Barı üst göğsüne doğru çek. Kürek kemiklerini arkada birbirine yaklaştır.",
        "equipment": "Kablosu Makinesi"
    },
    {
        "id": "seated_row",
        "name": "4. Seated Cable Row",
        "target": "Sırt / Postür",
        "default_reps": "3 Set x 12 Tekrar",
        "tips": "Gövdeni dik tut, tutacağı göbek deliğine doğru çek. Omuzlarını düşürme.",
        "equipment": "Row Makinesi"
    },
    {
        "id": "shoulder_press",
        "name": "5. Dumbbell Shoulder Press",
        "target": "Omuz / Triceps",
        "default_reps": "3 Set x 12 Tekrar",
        "tips": "Ağırlıkları kulak hizasından baş üzerine doğru sür. Tepe noktada dirsekleri kitleme.",
        "equipment": "Dumbbell"
    },
    {
        "id": "biceps_curl",
        "name": "6. Dumbbell Biceps Curl",
        "target": "Ön Kol (Biceps)",
        "default_reps": "2 Set x 12 Tekrar",
        "tips": "Dirsekleri gövdeye sabitle. Gövdeni sallamadan sadece ön kolları kaldır.",
        "equipment": "Dumbbell"
    },
    {
        "id": "triceps_pushdown",
        "name": "7. Rope Triceps Pushdown",
        "target": "Arka Kol (Triceps)",
        "default_reps": "2 Set x 12 Tekrar",
        "tips": "Dirsekler sabit, halatı aşağı iterken en altta iki ucu dışa doğru aç.",
        "equipment": "Makaralı Halat"
    },
    {
        "id": "plank",
        "name": "8. Core Plank",
        "target": "Karın / Core",
        "default_reps": "3 Set x 35 Saniye",
        "tips": "Dirsekler üzerinde başından topuğa kadar düz bir tahta gibi sabit dur.",
        "equipment": "Mat / Vücut Ağırlığı"
    }
]

# Session State Yönetimi
if "app_state" not in st.session_state:
    st.session_state.app_state = "SETUP"  # SETUP, WORKOUT, FINISHED
if "selected_exercises" not in st.session_state:
    st.session_state.selected_exercises = []
if "rest_duration" not in st.session_state:
    st.session_state.rest_duration = 60
if "current_ex_idx" not in st.session_state:
    st.session_state.current_ex_idx = 0
if "current_set" not in st.session_state:
    st.session_state.current_set = 1
if "total_sets" not in st.session_state:
    st.session_state.total_sets = 3
if "is_resting" not in st.session_state:
    st.session_state.is_resting = False


def render_threejs_mannequin(exercise_id):
    """Three.js ile 3D Anatomi Manikeni ve Gerçek Zamanlı Egzersiz Animasyonu Render Eder"""
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #0e1117; font-family: sans-serif; }}
            #canvas-container {{ width: 100%; height: 480px; position: relative; }}
            #info-overlay {{
                position: absolute; bottom: 12px; left: 12px; 
                color: #00f2fe; background: rgba(14, 17, 23, 0.85);
                padding: 6px 14px; border-radius: 20px; font-size: 12px;
                border: 1px solid #00f2fe; pointer-events: none;
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div id="info-overlay">🖱️ Sol Tık: Döndür | Sağ Tık: Kaydır | Tekerlek: Yakınlaş</div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 480, 0.1, 1000);
            camera.position.set(0, 1.3, 3.5);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, 480);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.target.set(0, 1, 0);

            // Işıklandırma (Studio Lighting)
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0x00f2fe, 1.2);
            dirLight.position.set(3, 5, 4);
            dirLight.castShadow = true;
            scene.add(dirLight);

            const rimLight = new THREE.DirectionalLight(0x4facfe, 0.8);
            rimLight.position.set(-3, 2, -3);
            scene.add(rimLight);

            // Zemin Izgarası
            const gridHelper = new THREE.GridHelper(10, 20, 0x00f2fe, 0x1f2937);
            gridHelper.position.y = 0;
            scene.add(gridHelper);

            // Materyaller (Futuristic Anatomical Body)
            const bodyMat = new THREE.MeshStandardMaterial({{ color: 0x2a364f, roughness: 0.3, metalness: 0.6 }});
            const jointMat = new THREE.MeshStandardMaterial({{ color: 0x00f2fe, roughness: 0.2, metalness: 0.8, emissive: 0x005577 }});
            const equipMat = new THREE.MeshStandardMaterial({{ color: 0xff8c00, roughness: 0.3, metalness: 0.7 }});

            // İnsan Manikeni Parçaları Gruplama
            const bodyGroup = new THREE.Group();
            scene.add(bodyGroup);

            // Torso (Gövde)
            const torsoGeo = new THREE.CylinderGeometry(0.22, 0.15, 0.55, 12);
            const torso = new THREE.Mesh(torsoGeo, bodyMat);
            torso.position.y = 1.15;
            bodyGroup.add(torso);

            // Baş
            const headGeo = new THREE.SphereGeometry(0.12, 16, 16);
            const head = new THREE.Mesh(headGeo, jointMat);
            head.position.y = 1.55;
            bodyGroup.add(head);

            // Omuz Eklemleri
            const shoulderL = new THREE.Group(); shoulderL.position.set(-0.26, 1.35, 0); bodyGroup.add(shoulderL);
            const shoulderR = new THREE.Group(); shoulderR.position.set(0.26, 1.35, 0); bodyGroup.add(shoulderR);

            // Üst Kollar
            const armGeo = new THREE.CylinderGeometry(0.05, 0.04, 0.3, 10);
            armGeo.translate(0, -0.15, 0);
            const upperArmL = new THREE.Mesh(armGeo, bodyMat); shoulderL.add(upperArmL);
            const upperArmR = new THREE.Mesh(armGeo, bodyMat); shoulderR.add(upperArmR);

            // Dirsek Eklemleri & Ön Kollar
            const elbowL = new THREE.Group(); elbowL.position.set(0, -0.3, 0); upperArmL.add(elbowL);
            const elbowR = new THREE.Group(); elbowR.position.set(0, -0.3, 0); upperArmR.add(elbowR);

            const forearmGeo = new THREE.CylinderGeometry(0.04, 0.035, 0.3, 10);
            forearmGeo.translate(0, -0.15, 0);
            const forearmL = new THREE.Mesh(forearmGeo, bodyMat); elbowL.add(forearmL);
            const forearmR = new THREE.Mesh(forearmGeo, bodyMat); elbowR.add(forearmR);

            // Kalça Eklemleri & Bacaklar
            const hipL = new THREE.Group(); hipL.position.set(-0.12, 0.88, 0); bodyGroup.add(hipL);
            const hipR = new THREE.Group(); hipR.position.set(0.12, 0.88, 0); bodyGroup.add(hipR);

            const legGeo = new THREE.CylinderGeometry(0.08, 0.06, 0.4, 10);
            legGeo.translate(0, -0.2, 0);
            const thighL = new THREE.Mesh(legGeo, bodyMat); hipL.add(thighL);
            const thighR = new THREE.Mesh(legGeo, bodyMat); hipR.add(thighR);

            const kneeL = new THREE.Group(); kneeL.position.set(0, -0.4, 0); thighL.add(kneeL);
            const kneeR = new THREE.Group(); kneeR.position.set(0, -0.4, 0); thighR.add(kneeR);

            const shinGeo = new THREE.CylinderGeometry(0.06, 0.04, 0.4, 10);
            shinGeo.translate(0, -0.2, 0);
            const shinL = new THREE.Mesh(shinGeo, bodyMat); kneeL.add(shinL);
            const shinR = new THREE.Mesh(shinGeo, bodyMat); kneeR.add(shinR);

            // Ekipmanlar (Dumbbell / Barbell / Bench / Pulldown)
            const equipGroup = new THREE.Group();
            bodyGroup.add(equipGroup);

            const dbGeo = new THREE.Dumbbell = new THREE.CylinderGeometry(0.08, 0.08, 0.25, 12);

            const dbL = new THREE.Mesh(dbGeo, equipMat);
            const dbR = new THREE.Mesh(dbGeo, equipMat);
            dbL.rotation.z = Math.PI / 2;
            dbR.rotation.z = Math.PI / 2;

            const exType = "{exercise_id}";

            // Ekipman Yerleşimi & Pozlama
            if (exType === "squat" || exType === "biceps_curl" || exType === "shoulder_press") {{
                forearmL.add(dbL); dbL.position.set(0, -0.3, 0);
                forearmR.add(dbR); dbR.position.set(0, -0.3, 0);
            }}

            const benchGeo = new THREE.BoxGeometry(0.45, 0.25, 1.2);
            const bench = new THREE.Mesh(benchGeo, equipMat);
            bench.position.set(0, 0.12, 0);

            if (exType === "chest_press") {{
                scene.add(bench);
                forearmL.add(dbL); dbL.position.set(0, -0.3, 0);
                forearmR.add(dbR); dbR.position.set(0, -0.3, 0);
            }}

            const barGeo = new THREE.CylinderGeometry(0.02, 0.02, 1.4, 12);
            barGeo.rotateZ(Math.PI / 2);
            const latBar = new THREE.Mesh(barGeo, equipMat);

            if (exType === "lat_pulldown") {{
                scene.add(latBar);
            }}

            // Animasyon Döngüsü
            let clock = new THREE.Clock();

            function animate() {{
                requestAnimationFrame(animate);
                let t = clock.getElapsedTime() * 2.2; 
                let cycle = (Math.sin(t) + 1) / 2; // 0 ile 1 arası yumuşak salınım

                // Pozların Sıfırlanması
                bodyGroup.position.set(0, 0, 0);
                bodyGroup.rotation.set(0, 0, 0);
                shoulderL.rotation.set(0, 0, 0); shoulderR.rotation.set(0, 0, 0);
                elbowL.rotation.set(0, 0, 0); elbowR.rotation.set(0, 0, 0);
                hipL.rotation.set(0, 0, 0); hipR.rotation.set(0, 0, 0);
                kneeL.rotation.set(0, 0, 0); kneeR.rotation.set(0, 0, 0);

                if (exType === "squat") {{
                    let squatDepth = cycle * 0.45;
                    bodyGroup.position.y = -squatDepth;
                    hipL.rotation.x = cycle * 1.3;
                    hipR.rotation.x = cycle * 1.3;
                    kneeL.rotation.x = -cycle * 1.4;
                    kneeR.rotation.x = -cycle * 1.4;
                    // Dumbbell göğüste tutulur
                    shoulderL.rotation.x = 0.8; shoulderR.rotation.x = 0.8;
                    elbowL.rotation.x = -1.5; elbowR.rotation.x = -1.5;
                }}
                else if (exType === "chest_press") {{
                    bodyGroup.position.y = 0.35;
                    bodyGroup.rotation.x = -Math.PI / 2; // Yatar pozisyon
                    shoulderL.rotation.y = -Math.PI / 2 + (cycle * 0.5);
                    shoulderR.rotation.y = Math.PI / 2 - (cycle * 0.5);
                    elbowL.rotation.x = -cycle * 1.2;
                    elbowR.rotation.x = -cycle * 1.2;
                }}
                else if (exType === "lat_pulldown") {{
                    bodyGroup.position.y = -0.1;
                    shoulderL.rotation.z = 2.4 - (cycle * 0.9);
                    shoulderR.rotation.z = -2.4 + (cycle * 0.9);
                    elbowL.rotation.z = -1.2 + (cycle * 0.5);
                    elbowR.rotation.z = 1.2 - (cycle * 0.5);
                    latBar.position.set(0, 1.8 - (cycle * 0.55), 0);
                }}
                else if (exType === "seated_row") {{
                    shoulderL.rotation.x = 0.9 - (cycle * 0.7);
                    shoulderR.rotation.x = 0.9 - (cycle * 0.7);
                    elbowL.rotation.x = -cycle * 1.2;
                    elbowR.rotation.x = -cycle * 1.2;
                    hipL.rotation.x = 1.2; hipR.rotation.x = 1.2;
                    kneeL.rotation.x = -0.6; kneeR.rotation.x = -0.6;
                    bodyGroup.position.y = -0.2;
                }}
                else if (exType === "shoulder_press") {{
                    shoulderL.rotation.z = 1.4; shoulderR.rotation.z = -1.4;
                    elbowL.rotation.x = -0.5 + (cycle * 1.0);
                    elbowR.rotation.x = -0.5 + (cycle * 1.0);
                }}
                else if (exType === "biceps_curl") {{
                    elbowL.rotation.x = -cycle * 2.2;
                    elbowR.rotation.x = -(1 - cycle) * 2.2; // Alternatif curl
                }}
                else if (exType === "triceps_pushdown") {{
                    shoulderL.rotation.x = 0.3; shoulderR.rotation.x = 0.3;
                    elbowL.rotation.x = -1.8 + (cycle * 1.6);
                    elbowR.rotation.x = -1.8 + (cycle * 1.6);
                }}
                else if (exType === "plank") {{
                    bodyGroup.rotation.x = -Math.PI / 2 + 0.1;
                    bodyGroup.position.y = 0.2;
                    shoulderL.rotation.x = 1.4; shoulderR.rotation.x = 1.4;
                    elbowL.rotation.x = -1.4; elbowR.rotation.x = -1.4;
                    bodyGroup.position.z = Math.sin(t * 2) * 0.02; // Nefes efekti
                }}

                controls.update();
                renderer.render(scene, camera);
            }}

            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / 480;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, 480);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=500)


# --- EKRAN 1: KURULUM & SEÇİM (SETUP) ---
if st.session_state.app_state == "SETUP":
    st.title("🏋️‍♂️ Full Body Antrenman Özelleştirme")
    st.markdown("Bugünkü antrenmanına eklemek istediğin egzersizleri ve dinlenme süreni belirle.")

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("1️⃣ Egzersiz Seçimi")
        st.caption("Yapmak istediğin hareketlerin yanındaki kutucukları işaretle:")

        selected_list = []
        for ex in ALL_EXERCISES:
            is_checked = st.checkbox(
                f"**{ex['name']}** — *({ex['target']})*",
                value=True,
                key=f"check_{ex['id']}"
            )
            if is_checked:
                selected_list.append(ex)

    with col2:
        st.subheader("2️⃣ Ayarlar")
        rest_time = st.slider(
            "⏱️ Set Arası Dinlenme Süresi (Saniye):",
            min_value=15,
            max_value=120,
            value=60,
            step=5
        )

        set_count = st.number_input(
            "🔢 Toplam Set Sayısı:",
            min_value=1,
            max_value=5,
            value=3
        )

        st.divider()

        st.metric("Seçilen Egzersiz", f"{len(selected_list)} Hareket")
        st.metric("Set Başı Dinlenme", f"{rest_time} sn")

        if st.button("🚀 Antrenmanı Başlat", type="primary", use_container_width=True):
            if len(selected_list) == 0:
                st.error("Lütfen en az 1 egzersiz seçin!")
            else:
                st.session_state.selected_exercises = selected_list
                st.session_state.rest_duration = rest_time
                st.session_state.total_sets = set_count
                st.session_state.current_ex_idx = 0
                st.session_state.current_set = 1
                st.session_state.app_state = "WORKOUT"
                st.rerun()

# --- EKRAN 2: ANTRENMAN (WORKOUT) ---
elif st.session_state.app_state == "WORKOUT":
    exercises = st.session_state.selected_exercises
    idx = st.session_state.current_ex_idx
    current_ex = exercises[idx]

    # Üst İlerleme Çubuğu
    progress_val = (idx) / len(exercises)
    st.progress(progress_val)

    st.caption(f"Egzersiz {idx + 1} / {len(exercises)}")

    col_3d, col_info = st.columns([1.3, 1])

    with col_3d:
        st.subheader(f"🎬 3D Biyomekanik Model: {current_ex['name']}")
        render_threejs_mannequin(current_ex["id"])

    with col_info:
        st.header(current_ex["name"])
        st.markdown(f"**🎯 Hedef Kas Grubu:** `{current_ex['target']}`")
        st.markdown(f"**🏋️ Gereken Ekipman:** `{current_ex['equipment']}`")

        # Set Takip Sayacı
        st.subheader(f"Set {st.session_state.current_set} / {st.session_state.total_sets}")

        st.info(f"💡 **Doğru Form İpucu:**\n{current_ex['tips']}")

        st.divider()

        # DİNLENME MODU
        if st.session_state.is_resting:
            st.warning("⏱️ DINLENME SÜRESİ")
            rest_bar = st.progress(0)
            timer_box = st.empty()

            total_r = st.session_state.rest_duration
            for sec in range(total_r, -1, -1):
                pct = 1.0 - (sec / total_r)
                rest_bar.progress(pct)
                timer_box.markdown(f"### ⏳ Kalan Süre: `{sec}` Saniye")
                time.sleep(1)

            st.session_state.is_resting = False

            # Set veya Egzersiz Geçiş Mantığı
            if st.session_state.current_set < st.session_state.total_sets:
                st.session_state.current_set += 1
            else:
                st.session_state.current_set = 1
                if idx + 1 < len(exercises):
                    st.session_state.current_ex_idx += 1
                else:
                    st.session_state.app_state = "FINISHED"

            st.rerun()

        else:
            if st.button("✅ Seti / Harekatı Tamamla", type="primary", use_container_width=True):
                st.session_state.is_resting = True
                st.rerun()

    st.divider()

    # Alt Navigasyon Butonları
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅️ Önceki Egzersiz", disabled=(idx == 0)):
            st.session_state.current_ex_idx -= 1
            st.session_state.current_set = 1
            st.session_state.is_resting = False
            st.rerun()
    with c2:
        if st.button("⚙️ Ayarlara Dön"):
            st.session_state.app_state = "SETUP"
            st.session_state.is_resting = False
            st.rerun()
    with c3:
        if st.button("➡️ Sonraki Egzersiz", disabled=(idx == len(exercises) - 1)):
            st.session_state.current_ex_idx += 1
            st.session_state.current_set = 1
            st.session_state.is_resting = False
            st.rerun()

# --- EKRAN 3: BİTİŞ & TEBRİKLER (FINISHED) ---
elif st.session_state.app_state == "FINISHED":
    st.balloons()
    st.title("🎉 Tebrikler! Antrenmanı Tamamladın!")
    st.success("Bugünkü Full Body seansını başarıyla bitirdin. Kas gelişimi ve toparlanma için bol su içmeyi ve protein almayı unutma!")

    st.subheader("📊 Tamamlanan Antrenman Özeti:")
    for ex in st.session_state.selected_exercises:
        st.write(f"✔️ {ex['name']} — {st.session_state.total_sets} Set")

    st.divider()
    if st.button("🔄 Yeni Antrenman Planla", type="primary"):
        st.session_state.app_state = "SETUP"
        st.rerun()
