import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function DashboardPage() {
  const navigate = useNavigate();
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response = await api.get("/predictions/history");
        setPredictions(response.data);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem("access_token");
          navigate("/login");
          return;
        }

        setError("Impossible de charger les données du dashboard.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [navigate]);

  if (loading) {
    return <p>Chargement du dashboard...</p>;
  }

  const total = predictions.length;
  const criticalCount = predictions.filter(
    (item) => item.risk_level === "Critique"
  ).length;

  const averageScore =
    total > 0
      ? (
          predictions.reduce((sum, item) => sum + item.risk_score, 0) / total
        ).toFixed(1)
      : "0.0";

  const latest = predictions[0];

  return (
    <section className="dashboard-page">
      <div className="dashboard-heading">
        <div>
          <p className="eyebrow">Espace utilisateur</p>
          <h1>Dashboard</h1>
          <p>Vue d’ensemble de vos analyses de risque enregistrées.</p>
        </div>

        <Link className="primary-action dashboard-action" to="/predict">
          Nouvelle prédiction
        </Link>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="stats-grid">
        <article className="stat-card">
          <span>Analyses enregistrées</span>
          <strong>{total}</strong>
        </article>

        <article className="stat-card">
          <span>Score moyen</span>
          <strong>{averageScore} / 100</strong>
        </article>

        <article className="stat-card">
          <span>Cas critiques</span>
          <strong>{criticalCount}</strong>
        </article>

        <article className="stat-card">
          <span>Dernier niveau</span>
          <strong className={latest ? latest.risk_level.toLowerCase() : ""}>
            {latest ? latest.risk_level : "Aucune donnée"}
          </strong>
        </article>
      </div>

      {latest ? (
        <section className="latest-card">
          <div>
            <p className="eyebrow">Dernière analyse</p>
            <h2>Risque {latest.risk_level}</h2>
            <p>
              Score: <strong>{latest.risk_score} / 100</strong> · Température:
              {" "}
              <strong>{latest.temp_max}°C</strong> · Humidité:{" "}
              <strong>{latest.humidity}%</strong>
            </p>
          </div>

          <Link className="secondary-dashboard-action" to="/history">
            Voir tout l’historique
          </Link>
        </section>
      ) : (
        <section className="empty-state">
          <p>Vous n’avez pas encore réalisé de prédiction.</p>
          <Link className="primary-action" to="/predict">
            Commencer une analyse
          </Link>
        </section>
      )}
    </section>
  );
}

export default DashboardPage;