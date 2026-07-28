import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const initialForm = {
  temp_max: 41,
  humidity: 18,
  wind_max: 28,
  rain: 0,
  et0: 7.8,
  vpd_max: 3.2,
  radiation: 25.5,
  consecutive_hot_days_38: 6,
};

function PredictionPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm({
      ...form,
      [name]: Number(value),
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await api.post("/predict", form);
      setResult(response.data);
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        navigate("/login");
        return;
      }

      setError(
        err.response?.data?.detail ||
          "Impossible de calculer la prédiction. Réessayez."
      );
    } finally {
      setLoading(false);
    }
  }

  const prediction = result?.prediction || result;

  return (
    <section className="prediction-page">
      <div>
        <h1>Prédiction du risque</h1>
        <p>
          Entrez les conditions météorologiques pour estimer le risque
          d'incendie lié à une vague de chaleur.
        </p>

        <form className="prediction-form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <div>
              <label htmlFor="temp_max">Température maximale (°C)</label>
              <input
                id="temp_max"
                name="temp_max"
                type="number"
                step="0.1"
                value={form.temp_max}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="humidity">Humidité moyenne (%)</label>
              <input
                id="humidity"
                name="humidity"
                type="number"
                step="0.1"
                value={form.humidity}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="wind_max">Vent maximal (km/h)</label>
              <input
                id="wind_max"
                name="wind_max"
                type="number"
                step="0.1"
                value={form.wind_max}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="rain">Précipitations (mm)</label>
              <input
                id="rain"
                name="rain"
                type="number"
                step="0.1"
                min="0"
                value={form.rain}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="et0">Évapotranspiration ET0</label>
              <input
                id="et0"
                name="et0"
                type="number"
                step="0.1"
                min="0"
                value={form.et0}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="vpd_max">VPD maximal</label>
              <input
                id="vpd_max"
                name="vpd_max"
                type="number"
                step="0.1"
                min="0"
                value={form.vpd_max}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="radiation">Rayonnement solaire</label>
              <input
                id="radiation"
                name="radiation"
                type="number"
                step="0.1"
                min="0"
                value={form.radiation}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="consecutive_hot_days_38">
                Jours consécutifs ≥ 38°C
              </label>
              <input
                id="consecutive_hot_days_38"
                name="consecutive_hot_days_38"
                type="number"
                min="0"
                step="1"
                value={form.consecutive_hot_days_38}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Calcul en cours..." : "Calculer le risque"}
          </button>
        </form>
      </div>

      {prediction && (
        <div className={`prediction-result ${prediction.risk_level.toLowerCase()}`}>
          <h2>Résultat de la prédiction</h2>

          <div className="risk-level">{prediction.risk_level}</div>

          <div className="result-grid">
            <div>
              <span>Score de risque</span>
              <strong>{prediction.risk_score} / 100</strong>
            </div>

            <div>
              <span>Probabilité risque élevé</span>
              <strong>
                {(prediction.probability_high_risk * 100).toFixed(2)}%
              </strong>
            </div>

            <div>
              <span>Confiance du modèle</span>
              <strong>{prediction.confidence}%</strong>
            </div>

            <div>
              <span>Modèle utilisé</span>
              <strong>{prediction.model_name}</strong>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default PredictionPage;