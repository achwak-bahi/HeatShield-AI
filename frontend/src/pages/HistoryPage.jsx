import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function HistoryPage() {
  const navigate = useNavigate();

  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await api.get("/predictions/history");
        setPredictions(response.data);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem("access_token");
          navigate("/login");
          return;
        }

        setError(
          err.response?.data?.detail ||
            "Impossible de charger l'historique."
        );
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, [navigate]);

  function formatDate(dateValue) {
    return new Date(dateValue).toLocaleString("fr-FR");
  }

  function riskClass(level) {
    return level
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  if (loading) {
    return <p>Chargement de l'historique...</p>;
  }

  return (
    <section className="history-page">
      <h1>Historique des prédictions</h1>
      <p>Retrouvez les analyses enregistrées sur votre compte.</p>

      {error && <p className="error-message">{error}</p>}

      {!error && predictions.length === 0 && (
        <div className="empty-state">
          <p>Aucune prédiction enregistrée pour le moment.</p>
          <button onClick={() => navigate("/predict")}>
            Faire une prédiction
          </button>
        </div>
      )}

      {predictions.length > 0 && (
        <div className="history-list">
          {predictions.map((item) => (
            <article className="history-card" key={item.id}>
              <div className="history-card-header">
                <div>
                  <h2>Analyse #{item.id}</h2>
                  <p>{formatDate(item.created_at)}</p>
                </div>

                <span className={`risk-badge ${riskClass(item.risk_level)}`}>
                  {item.risk_level}
                </span>
              </div>

              <div className="history-grid">
                <div>
                  <span>Score</span>
                  <strong>{item.risk_score} / 100</strong>
                </div>

                <div>
                  <span>Probabilité</span>
                  <strong>
                    {(item.probability_high_risk * 100).toFixed(2)}%
                  </strong>
                </div>

                <div>
                  <span>Température max</span>
                  <strong>{item.temp_max}°C</strong>
                </div>

                <div>
                  <span>Humidité</span>
                  <strong>{item.humidity}%</strong>
                </div>

                <div>
                  <span>Vent max</span>
                  <strong>{item.wind_max} km/h</strong>
                </div>

                <div>
                  <span>Modèle</span>
                  <strong>{item.model_name}</strong>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default HistoryPage;