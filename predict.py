import pandas as pd
import numpy as np
import joblib

# Fungsi manual untuk normalisasi Min-Max
def minmax_scale(X):
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    return (X - X_min) / (X_max - X_min), X_min, X_max

# Fungsi jarak Euclidean
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Fungsi untuk assign cluster
def assign_clusters(X, centroids):
    labels = []
    for point in X:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        labels.append(np.argmin(distances))
    return np.array(labels)

# Fungsi update centroid
def update_centroids(X, labels, k):
    new_centroids = []
    for i in range(k):
        cluster_points = X[labels == i]
        if len(cluster_points) > 0:
            new_centroids.append(cluster_points.mean(axis=0))
        else:
            new_centroids.append(np.random.rand(X.shape[1]))  # fallback
    return np.array(new_centroids)

# Baca data
df = pd.read_excel('dataCleaning.xlsx')

# Kolom fitur
fitur = [
    'Waktu_Tidur', 'Kualitas_Tidur', 'Kesulitan_Tidur', 'Kebugaran_Bangun',
    'Akt_Fisik', 'Akt_Akademik', 'Akt_NonAkademik',
    'Rasa_Lelah', 'Rasa_Stress', 'Sulit_Fokus', 'Hilang_Minat'
]
X = df[fitur].values

# Normalisasi manual
X_scaled, X_min, X_max = minmax_scale(X)

# Inisialisasi centroid (acak dari data)
np.random.seed(42)
k = 4  # ubah jumlah cluster sesuai kebutuhan
centroids = X_scaled[np.random.choice(X_scaled.shape[0], k, replace=False)]

# Iterasi KMeans manual
max_iter = 10
for i in range(max_iter):
    labels = assign_clusters(X_scaled, centroids)
    new_centroids = update_centroids(X_scaled, labels, k)
    if np.allclose(centroids, new_centroids):
        break
    centroids = new_centroids

# Tambahkan hasil cluster ke DataFrame
df['Cluster'] = labels

# Simpan model manual: centroid & normalizer
joblib.dump({'centroids': centroids, 'X_min': X_min, 'X_max': X_max}, 'kmeans_manual.pkl')

# Simpan hasil cluster
df.to_excel('hasil_clustering_manual.xlsx', index=False)

print("Clustering manual selesai dan disimpan!")
