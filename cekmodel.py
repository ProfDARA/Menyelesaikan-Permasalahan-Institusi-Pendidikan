

import pandas as pd
import joblib

# Daftar kolom kategorikal yang digunakan untuk encoding
categorical_cols = [
    'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
    'Previous_qualification', 'Nacionality', 'Mothers_qualification', 'Fathers_qualification',
    'Mothers_occupation', 'Fathers_occupation', 'Displaced', 'Educational_special_needs',
    'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International'
]

# Load model yang sudah dilatih
model = joblib.load("model_prediksi.pkl")

# Kode untuk tes model secara lokal
if __name__ == "__main__":

    # Contoh data input (isi sesuai kebutuhan)
    sample_input = {
        'Marital_status': 1,
        'Application_mode': 1,
        'Application_order': 0,
        'Course': 33,
        'Daytime_evening_attendance': 1,
        'Previous_qualification': 1,
        'Previous_qualification_grade': 160.0,
        'Nacionality': 1,
        'Mothers_qualification': 1,
        'Fathers_qualification': 1,
        'Mothers_occupation': 0,
        'Fathers_occupation': 0,
        'Displaced': 0,
        'Educational_special_needs': 0,
        'Debtor': 0,
        'Tuition_fees_up_to_date': 1,
        'Gender': 1,
        'Scholarship_holder': 0,
        'International': 0,
        'Age_at_enrollment': 19,
        'Curricular_units_1st_sem_credited': 1,
        'Curricular_units_1st_sem_enrolled': 6,
        'Curricular_units_1st_sem_evaluations': 6,
        'Curricular_units_1st_sem_approved': 6,
        'Curricular_units_1st_sem_grade': 14.0,
        'Curricular_units_1st_sem_without_evaluations': 0,
        'Curricular_units_2nd_sem_credited': 0,
        'Curricular_units_2nd_sem_enrolled': 6,
        'Curricular_units_2nd_sem_evaluations': 6,
        'Curricular_units_2nd_sem_approved': 6,
        'Curricular_units_2nd_sem_grade': 13.67,
        'Curricular_units_2nd_sem_without_evaluations': 0,
        'Unemployment_rate': 13.9,
        'Inflation_rate': -0.3,
        'GDP': 0.79,
        'Admission_grade': 150.0
    }

    # DataFrame input
    input_df = pd.DataFrame([sample_input])
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
    print(f"Prediksi: {status}")
    print(f"Probabilitas Drop Out: {pred_proba[0][1]*100:.2f}%")