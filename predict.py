import pandas as pd
import numpy as np
import joblib

def minmax_scale(X):
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    return (X - X_min) / (X_max - X_min), X_min, X_max

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def assign_clusters(X, centroids):
    labels = []
    for point in X:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        labels.append(np.argmin(distances))
    return np.array(labels)

def update_centroids(X, labels, k):
    new_centroids = []
    for i in range(k):
        cluster_points = X[labels == i]
        if len(cluster_points) > 0:
            new_centroids.append(cluster_points.mean(axis=0))
        else:
            new_centroids.append(np.random.rand(X.shape[1]))
    return np.array(new_centroids)

def kmeans_plus_plus_init(X, k):
    np.random.seed(42)
    centroids = []
    centroids.append(X[np.random.choice(X.shape[0])])
    
    for _ in range(1, k):
        dists = np.array([min([euclidean_distance(x, c)**2 for c in centroids]) for x in X])
        probas = dists / dists.sum()
        next_centroid_idx = np.random.choice(X.shape[0], p=probas)
        centroids.append(X[next_centroid_idx])
    
    return np.array(centroids)

df = pd.read_excel('dataCleaning.xlsx')
fitur = [
    'Waktu_Tidur', 'Kualitas_Tidur', 'Kesulitan_Tidur', 'Kebugaran_Bangun',
    'Akt_Fisik', 'Akt_Akademik', 'Akt_NonAkademik',
    'Rasa_Lelah', 'Rasa_Stress', 'Sulit_Fokus', 'Hilang_Minat'
]
X = df[fitur].values
X_scaled, X_min, X_max = minmax_scale(X)

k = 4
centroids = X_scaled[[0, 1, 2, 3]]  # C1 dari data ke-1, C2 dari ke-2, dst
centroids_iter1 = centroids.copy()

labels_iter1 = assign_clusters(X_scaled, centroids_iter1)
dist_iter1 = [[euclidean_distance(x, c) for c in centroids_iter1] for x in X_scaled]
df_iter1 = df.copy()
df_iter1[['C1', 'C2', 'C3', 'C4']] = pd.DataFrame(dist_iter1, index=df.index)
df_iter1['Cluster'] = labels_iter1

max_iter = 10
centroids_final = centroids_iter1.copy()
for i in range(max_iter):
    labels = assign_clusters(X_scaled, centroids_final)
    new_centroids = update_centroids(X_scaled, labels, k)
    if np.allclose(centroids_final, new_centroids):
        break
    centroids_final = new_centroids

labels_final = assign_clusters(X_scaled, centroids_final)
dist_final = [[euclidean_distance(x, c) for c in centroids_final] for x in X_scaled]
df_final = df.copy()
df_final[['C1', 'C2', 'C3', 'C4']] = pd.DataFrame(dist_final, index=df.index)
df_final['Cluster'] = labels_final

# Hitung rata-rata akhir
cluster_means = df_final.groupby('Cluster')[fitur].mean()
cluster_means.index = ['C1', 'C2', 'C3', 'C4']


joblib.dump({'centroids': centroids_final, 'X_min': X_min, 'X_max': X_max}, 'kmeans_manual.pkl')
with pd.ExcelWriter('hasil_clustering_manual.xlsx') as writer:
    df_iter1.to_excel(writer, sheet_name='Data Cluster', index=False)
    df_final.to_excel(writer, sheet_name='Data Cluster Konvergen', index=False)
    cluster_means.to_excel(writer, sheet_name='Rata-rata per Cluster')

print(f"Clustering selesai dalam {i+1} iterasi dengan inisialisasi K-Means++ dan disimpan ke Excel!")
