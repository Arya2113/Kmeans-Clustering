from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'mental_health_prediction_secret_key_2024'

# Load model dan scaler
try:
    model_manual = joblib.load('kmeans_manual.pkl')
    centroids = model_manual['centroids']
    X_min = model_manual['X_min']
    X_max = model_manual['X_max']
    print("Model manual berhasil dimuat!")
except FileNotFoundError as e:
    print(f"Error loading model: {e}")

fitur_prediksi = [
    'Waktu_Tidur', 'Kualitas_Tidur', 'Kesulitan_Tidur', 'Kebugaran_Bangun',
    'Akt_Fisik', 'Akt_Akademik', 'Akt_NonAkademik',
    'Rasa_Lelah', 'Rasa_Stress', 'Sulit_Fokus', 'Hilang_Minat'
]

def minmax_scale_input(arr, X_min, X_max):
    return (arr - X_min) / (X_max - X_min)

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def assign_cluster_manual(arr_scaled, centroids):
    distances = [euclidean_distance(arr_scaled[0], c) for c in centroids]
    return int(np.argmin(distances))


# Definisi karakteristik klaster
cluster_info = {
    0: {
        'name': 'Kesehatan Mental Optimal',
        'description': 'Anda memiliki pola tidur yang baik, aktivitas seimbang, dan tingkat stres rendah.',
        'color': '#22c55e',
        'bg_class': 'bg-green-50',
        'text_class': 'text-green-700',
        'recommendations': [
            'Pertahankan pola tidur yang baik',
            'Lanjutkan aktivitas fisik rutin',
            'Jaga keseimbangan akademik dan non-akademik'
        ]
    },
    1: {
        'name': 'Kesehatan Mental Baik',
        'description': 'Anda memiliki kesehatan mental yang cukup baik, namun ada beberapa area yang bisa ditingkatkan.',
        'color': '#3b82f6',
        'bg_class': 'bg-blue-50',
        'text_class': 'text-blue-700',
        'recommendations': [
            'Tingkatkan kualitas tidur',
            'Tambah aktivitas fisik jika memungkinkan',
            'Kelola stres dengan teknik relaksasi'
        ]
    },
    2: {
        'name': 'Perlu Perhatian',
        'description': 'Beberapa aspek kesehatan mental Anda memerlukan perhatian lebih.',
        'color': '#eab308',
        'bg_class': 'bg-yellow-50',
        'text_class': 'text-yellow-700',
        'recommendations': [
            'Perbaiki pola tidur secara bertahap',
            'Kurangi beban stres dengan manajemen waktu',
            'Pertimbangkan konsultasi dengan konselor'
        ]
    },
    3: {
        'name': 'Risiko Kesehatan Mental',
        'description': 'Anda menunjukkan beberapa tanda risiko kesehatan mental yang perlu ditangani.',
        'color': '#ef4444',
        'bg_class': 'bg-red-50',
        'text_class': 'text-red-700',
        'recommendations': [
            'Segera perbaiki pola tidur',
            'Cari dukungan dari keluarga atau teman',
            'Sangat disarankan konsultasi dengan profesional kesehatan mental'
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = {f: request.form[f] for f in fitur_prediksi}
        
        arr = np.array([float(data[f]) for f in fitur_prediksi]).reshape(1, -1)
        arr_scaled = minmax_scale_input(arr, X_min, X_max)
        label = assign_cluster_manual(arr_scaled, centroids)

        feature_importance = calculate_feature_importance(data)
        
        session['hasil'] = {
            'input': data,
            'cluster': label,
            'cluster_info': cluster_info[label],
            'feature_importance': feature_importance
        }

        if request.is_json:
            return jsonify({
                "cluster": label,
                "cluster_info": cluster_info[label],
                "feature_importance": feature_importance
            })

        return redirect(url_for('result'))
    except Exception as e:
        print('Predict error:', str(e))
        if request.is_json:
            return jsonify({"error": str(e)}), 400
        return f"Error: {str(e)}", 400


@app.route('/result')
def result():
    hasil = session.get('hasil', None)
    if hasil is None:
        return redirect(url_for('index'))
    return render_template('result.html', hasil=hasil)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('hasil', None)
    return redirect(url_for('index'))

def calculate_feature_importance(data):
    """Hitung feature importance untuk visualisasi"""
    return {
        'Pola Tidur': (float(data['Waktu_Tidur']) * 0.4 + 
                      float(data['Kualitas_Tidur']) * 0.4 + 
                      (6 - float(data['Kesulitan_Tidur'])) * 0.2) * 20,

        'Aktivitas Fisik & Keseimbangan': (
            (float(data['Akt_Fisik']) * 0.5 * 20) + 
            ((1 - abs(float(data['Akt_Akademik']) - float(data['Akt_NonAkademik'])) / 10) * 100 * 0.5)
        ),

        'Energi & Vitalitas': ((6 - float(data['Rasa_Lelah'])) * 0.5 + 
                              float(data['Kebugaran_Bangun']) * 0.5) * 20,

        'Kesehatan Emosional': ((6 - float(data['Rasa_Stress'])) * 0.4 + 
                               (6 - float(data['Sulit_Fokus'])) * 0.3 + 
                               (6 - float(data['Hilang_Minat'])) * 0.3) * 20
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
