import streamlit as st
import pandas as pd
import joblib


# Load model
model = joblib.load("model_prediksi.pkl")

categorical_cols = [
    'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
    'Previous_qualification', 'Nacionality', 'Mothers_qualification',
    'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation',
    'Displaced', 'Educational_special_needs', 'Debtor',
    'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International'
]

numerical_cols = [
    'Application_order', 'Previous_qualification_grade', 'Admission_grade',
    'Age_at_enrollment', 'Curricular_units_1st_sem_credited',
    'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_evaluations',
    'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade',
    'Curricular_units_1st_sem_without_evaluations', 'Curricular_units_2nd_sem_credited',
    'Curricular_units_2nd_sem_enrolled', 'Curricular_units_2nd_sem_evaluations',
    'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
    'Curricular_units_2nd_sem_without_evaluations', 'Unemployment_rate',
    'Inflation_rate', 'GDP'
]

st.set_page_config(page_title="Prediksi Drop Out", layout="wide")
st.title("🎓 Prediksi Drop Out Mahasiswa - Jaya Jaya Institut")
with st.form("input_form"):
    st.subheader("📋 Formulir Input Data Mahasiswa")
    input_dict = {}

    col1, col2 = st.columns(2)

    def load_options_from_readme(col_name):

        mapping = {
            'Marital_status': [
                ("Belum Menikah", 1), ("Menikah", 2), ("Duda/Janda", 3),
                ("Cerai", 4), ("Fakta Union", 5), ("Pisah Hukum", 6)
            ],
            'Application_mode': [
                ("1st phase - general contingent", 1), ("Ordinance No. 612/93", 2),
                ("Special contingent Azores", 5), ("Other higher courses", 7),
                ("Ordinance 854-B/99", 10), ("International student", 15),
                ("Special contingent Madeira", 16), ("2nd phase", 17),
                ("3rd phase", 18), ("Diff Plan", 26), ("Other Institution", 27),
                ("Over 23", 39), ("Transfer", 42), ("Change of course", 43),
                ("Tech spec diploma", 44), ("Change inst/course", 51),
                ("Short cycle", 53), ("Change inst/course Int", 57)
            ],
            'Course': [
                ("Biofuel", 33), ("Multimedia Design", 171), ("Social Service Eve", 8014),
                ("Agronomy", 9003), ("Design", 9070), ("Vet Nursing", 9085),
                ("IT Eng", 9119), ("Equinculture", 9130), ("Management", 9147),
                ("Social Service", 9238), ("Tourism", 9254), ("Nursing", 9500),
                ("Oral Hygiene", 9556), ("Marketing", 9670), ("Journalism", 9773),
                ("Basic Ed", 9853), ("Management Eve", 9991)
            ],
            'Daytime_evening_attendance': [("Siang", 1), ("Malam", 0)],
            'Previous_qualification': [
                ("Secondary education", 1), ("Bachelor's", 2), ("Degree", 3),
                ("Master's", 4), ("Doctorate", 5), ("Freq HE", 6),
                ("12th not completed", 9), ("11th not completed", 10),
                ("Other 11th", 12), ("10th", 14), ("10th not completed", 15),
                ("Basic 3rd cycle", 19), ("Basic 2nd cycle", 38),
                ("Tech spec", 39), ("Degree 1st cycle", 40),
                ("Prof Tech", 42), ("Master 2nd cycle", 43)
            ],
            'Nacionality': [
                ("Portugal", 1), ("German", 2), ("Spanish", 6), ("Italian", 11),
                ("Dutch", 13), ("English", 14), ("Lithuanian", 17), ("Angolan", 21),
                ("Cape Verdean", 22), ("Guinean", 24), ("Mozambican", 25),
                ("Santomean", 26), ("Turkish", 32), ("Brazilian", 41),
                ("Romanian", 62), ("Moldova", 100), ("Mexican", 101),
                ("Ukrainian", 103), ("Russian", 105), ("Cuban", 108),
                ("Colombian", 109)
            ],
            'Displaced': [("Ya", 1), ("Tidak", 0)],
            'Educational_special_needs': [("Ya", 1), ("Tidak", 0)],
            'Debtor': [("Ya", 1), ("Tidak", 0)],
            'Tuition_fees_up_to_date': [("Ya", 1), ("Tidak", 0)],
            'Gender': [("Laki-laki", 1), ("Perempuan", 0)],
            'Scholarship_holder': [("Ya", 1), ("Tidak", 0)],
            'International': [("Ya", 1), ("Tidak", 0)],
        }
        return mapping.get(col_name, [])

    with col1:
        input_dict['Marital_status'] = st.selectbox(
            "Status Pernikahan",
            load_options_from_readme('Marital_status'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Application_mode'] = st.selectbox(
            "Jalur Pendaftaran",
            load_options_from_readme('Application_mode'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Application_order'] = st.slider("Urutan Pilihan (0-9)", 0, 9, 0)
        input_dict['Course'] = st.selectbox(
            "Program Studi",
            load_options_from_readme('Course'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Daytime_evening_attendance'] = st.radio(
            "Waktu Kuliah",
            load_options_from_readme('Daytime_evening_attendance'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Previous_qualification'] = st.selectbox(
            "Kualifikasi Sebelumnya",
            load_options_from_readme('Previous_qualification'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Previous_qualification_grade'] = st.number_input(
            "Nilai Kualifikasi Sebelumnya (0-200)", 0.0, 200.0, 160.0
        )
        input_dict['Nacionality'] = st.selectbox(
            "Kewarganegaraan",
            load_options_from_readme('Nacionality'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Mothers_qualification'] = st.number_input(
            "Kode Pendidikan Ibu (1-44)", 1, 44, 1
        )
        input_dict['Fathers_qualification'] = st.number_input(
            "Kode Pendidikan Ayah (1-44)", 1, 44, 1
        )
        input_dict['Mothers_occupation'] = st.number_input(
            "Kode Pekerjaan Ibu (0-194)", 0, 194, 0
        )
        input_dict['Fathers_occupation'] = st.number_input(
            "Kode Pekerjaan Ayah (0-195)", 0, 195, 0
        )

    with col2:
        input_dict['Displaced'] = st.radio(
            "Apakah Terdampak (Displaced)?",
            load_options_from_readme('Displaced'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Educational_special_needs'] = st.radio(
            "Kebutuhan Khusus?",
            load_options_from_readme('Educational_special_needs'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Debtor'] = st.radio(
            "Memiliki Tunggakan?",
            load_options_from_readme('Debtor'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Tuition_fees_up_to_date'] = st.radio(
            "Bayar Kuliah Lancar?",
            load_options_from_readme('Tuition_fees_up_to_date'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Gender'] = st.radio(
            "Jenis Kelamin",
            load_options_from_readme('Gender'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Scholarship_holder'] = st.radio(
            "Penerima Beasiswa?",
            load_options_from_readme('Scholarship_holder'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['International'] = st.radio(
            "Mahasiswa Internasional?",
            load_options_from_readme('International'),
            format_func=lambda x: x[0]
        )[1]
        input_dict['Age_at_enrollment'] = st.slider("Usia Saat Masuk", 15, 60, 19)

    st.subheader("📘 Info Akademik dan Ekonomi")
    for k, label, minv, maxv, default in [
        ('Curricular_units_1st_sem_credited', "Smt 1 Diakui", 0, 20, 1),
        ('Curricular_units_1st_sem_enrolled', "Smt 1 Diambil", 0, 20, 6),
        ('Curricular_units_1st_sem_evaluations', "Smt 1 Evaluasi", 0, 20, 6),
        ('Curricular_units_1st_sem_approved', "Smt 1 Lulus", 0, 20, 6),
        ('Curricular_units_1st_sem_grade', "Nilai Rata-rata Smt 1", 0.0, 20.0, 14.0),
        ('Curricular_units_1st_sem_without_evaluations', "Smt 1 Tanpa Evaluasi", 0, 20, 0),
        ('Curricular_units_2nd_sem_credited', "Smt 2 Diakui", 0, 20, 0),
        ('Curricular_units_2nd_sem_enrolled', "Smt 2 Diambil", 0, 20, 6),
        ('Curricular_units_2nd_sem_evaluations', "Smt 2 Evaluasi", 0, 20, 6),
        ('Curricular_units_2nd_sem_approved', "Smt 2 Lulus", 0, 20, 6),
        ('Curricular_units_2nd_sem_grade', "Nilai Rata-rata Smt 2", 0.0, 20.0, 13.67),
        ('Curricular_units_2nd_sem_without_evaluations', "Smt 2 Tanpa Evaluasi", 0, 20, 0),
        ('Unemployment_rate', "Pengangguran (%)", 0.0, 100.0, 13.9),
        ('Inflation_rate', "Inflasi (%)", -10.0, 20.0, -0.3),
        ('GDP', "Pertumbuhan GDP (%)", -10.0, 10.0, 0.79),
        ('Admission_grade', "Nilai Ujian Masuk", 0.0, 200.0, 150.0)
    ]:
        input_dict[k] = st.number_input(label, min_value=minv, max_value=maxv, value=default, key=k)

    submitted = st.form_submit_button("🔍 Prediksi Drop Out")

if submitted:
    st.subheader("📊 Hasil Prediksi")
    input_df = pd.DataFrame([input_dict])
    df = pd.read_csv("cleaned_dataset.csv")
    df_encoded = pd.get_dummies(df.drop(columns=['Status']), columns=categorical_cols, drop_first=True)
    input_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

    for col in df_encoded.columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[df_encoded.columns]

    pred_proba = model.predict_proba(input_encoded)
    pred = model.predict(input_encoded)

    status = {0: "Tidak Drop Out", 1: "Drop Out"}.get(pred[0], "Unknown")
    st.success(f"✅ Prediksi: {status}")
    st.info(f"Probabilitas Drop Out: {pred_proba[0][1]*100:.2f}%")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://slidechef.net/wp-content/uploads/2023/10/Free-Simple-White-Background.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    

    """,
    unsafe_allow_html=True
)


