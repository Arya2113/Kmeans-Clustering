import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

df = pd.read_excel('dataCleaning.xlsx', header=0)
fitur = [
    'Waktu_Tidur', 'Kualitas_Tidur', 'Kesulitan_Tidur', 'Kebugaran_Bangun',
    'Akt_Fisik', 'Akt_Akademik', 'Akt_NonAkademik',
    'Rasa_Lelah', 'Rasa_Stress', 'Sulit_Fokus', 'Hilang_Minat'
]
X = df[fitur]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 8), wcss, marker='o')
plt.title('Elbow Method')
plt.xlabel('Cluster (K)')
plt.ylabel('WCSS')
plt.show()
