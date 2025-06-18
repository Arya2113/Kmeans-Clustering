//import { Chart } from "@/components/ui/chart"
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formKuesioner")
  const hasilDiv = document.getElementById("hasil")
  const hasilText = document.getElementById("hasilText")
  const submitBtn = document.getElementById("submitBtn")
  const submitText = document.getElementById("submitText")
  const loadingText = document.getElementById("loadingText")
  let radarChart = null
  let barChart = null

  form.addEventListener("submit", async (e) => {
    e.preventDefault()

    // Show loading state
    submitBtn.disabled = true
    submitText.classList.add("hidden")
    loadingText.classList.remove("hidden")

    const formData = new FormData(form)
    const data = {}

    // Convert form data to object
    for (const [key, value] of formData.entries()) {
      data[key] = Number.parseFloat(value)
    }

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error("Network response was not ok")
      }

      const result = await response.json()

      if (result.error) {
        throw new Error(result.error)
      }

      // Display result
      displayResult(result)
    } catch (error) {
      console.error("Error:", error)
      hasilText.innerHTML = `
                <div class="inline-block px-6 py-4 rounded-xl shadow-md bg-red-50 text-red-700 font-medium">
                    Terjadi kesalahan: ${error.message}. Silakan coba lagi.
                </div>
            `
      hasilDiv.classList.remove("hidden")
    } finally {
      // Reset button state
      submitBtn.disabled = false
      submitText.classList.remove("hidden")
      loadingText.classList.add("hidden")
    }
  })

  function displayResult(result) {
  const cluster = result.cluster
  const clusterInfo = result.cluster_info
  const featureImportance = result.feature_importance

  // Display text result
  hasilText.innerHTML = `
      <div class="inline-block px-6 py-4 rounded-xl shadow-md ${clusterInfo.bg_class} ${clusterInfo.text_class} font-medium">
          <div class="text-xl font-bold mb-2">Klaster ${cluster}: ${clusterInfo.name}</div>
          <div class="text-sm">${clusterInfo.description}</div>
      </div>
  `

  // Create visualizations
  createRadarChart(featureImportance, clusterInfo.color)
  createBarChart(cluster, clusterInfo.color)

  // Display recommendations
  const recommendationsDiv = document.getElementById("recommendations")
  recommendationsDiv.innerHTML = `
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Rekomendasi untuk Anda:</h3>
      <ul class="space-y-2">
          ${clusterInfo.recommendations
            .map(
              (rec) => `
              <li class="flex items-start">
                  <span class="text-blue-500 mr-2">•</span>
                  <span class="text-gray-700">${rec}</span>
              </li>
          `
            )
            .join("")}
      </ul>
  `

  // Show results
  hasilDiv.classList.remove("hidden")
  hasilDiv.scrollIntoView({ behavior: "smooth" })

  // ➕ Tampilkan tombol reset
  const resetBtn = document.getElementById("resetBtn")
  resetBtn.classList.remove("hidden")
  resetBtn.addEventListener("click", () => {
    form.reset()

    hasilDiv.classList.add("hidden")
    hasilText.innerHTML = ""
    recommendationsDiv.innerHTML = ""

    if (radarChart) radarChart.destroy()
    if (barChart) barChart.destroy()

    resetBtn.classList.add("hidden")
    window.scrollTo({ top: 0, behavior: "smooth" })
  })
}


  function createRadarChart(featureImportance, color) {
    const ctx = document.getElementById("radarChart").getContext("2d")

    if (radarChart) {
      radarChart.destroy()
    }

    const labels = Object.keys(featureImportance)
    const data = Object.values(featureImportance)

    radarChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Skor Area Kesehatan Mental",
            data: data,
            backgroundColor: color.replace("rgb(", "rgba(").replace(")", ", 0.2)"),
            borderColor: color,
            borderWidth: 2,
            pointBackgroundColor: color,
            pointRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          r: {
            angleLines: { display: true },
            suggestedMin: 0,
            suggestedMax: 100,
          },
        },
        plugins: {
          title: {
            display: true,
            text: "Profil Kesehatan Mental",
            font: { size: 16 },
          },
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `Skor: ${context.raw.toFixed(1)}/100`,
            },
          },
        },
      },
    })
  }

  function createBarChart(currentCluster, color) {
    const ctx = document.getElementById("barChart").getContext("2d")

    if (barChart) {
      barChart.destroy()
    }

    const labels = ["Optimal", "Baik", "Perlu Perhatian", "Risiko"]
    const clusterColors = ["#22c55e", "#3b82f6", "#eab308", "#ef4444"]

    const backgroundColor = clusterColors.map((clusterColor, index) =>
      index === currentCluster ? clusterColor : clusterColor.replace("#", "#").concat("80"),
    )

    barChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Klaster Anda",
            data: [
              currentCluster === 0 ? 100 : 0,
              currentCluster === 1 ? 100 : 0,
              currentCluster === 2 ? 100 : 0,
              currentCluster === 3 ? 100 : 0,
            ],
            backgroundColor: backgroundColor,
            borderWidth: 0,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          x: { display: false, max: 100 },
          y: { grid: { display: false } },
        },
        plugins: {
          title: {
            display: true,
            text: "Hasil Klasifikasi",
            font: { size: 16 },
          },
          legend: { display: false },
          tooltip: { enabled: false },
        },
      },
    })
  }
})
