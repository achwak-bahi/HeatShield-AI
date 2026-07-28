import { Link } from "react-router-dom";

function HomePage() {
  const isAuthenticated = Boolean(localStorage.getItem("access_token"));

  return (
    <section className="home-page">
      <div className="hero">
        <div className="hero-content">
          <p className="eyebrow">HeatShield AI · Algérie</p>

          <h1>Anticipez le risque d’incendie pendant les vagues de chaleur.</h1>

          <p className="hero-text">
            HeatShield AI utilise des variables météorologiques et un modèle
            d’apprentissage automatique pour estimer le niveau de risque,
            soutenir la prévention et faciliter la prise de décision.
          </p>

          <div className="hero-actions">
            <Link className="primary-action" to="/predict">
              Faire une prédiction
            </Link>

            {!isAuthenticated && (
              <Link className="secondary-action" to="/register">
                Créer un compte
              </Link>
            )}

            {isAuthenticated && (
              <Link className="secondary-action" to="/history">
                Voir mon historique
              </Link>
            )}
          </div>
        </div>

        <div className="hero-card">
          <span className="hero-card-icon">🔥</span>
          <p>Analysez les conditions critiques</p>
          <strong>Température · Humidité · Vent · Sécheresse</strong>
        </div>
      </div>

      <div className="info-grid">
        <article>
          <span>01</span>
          <h2>Collecter</h2>
          <p>
            Les conditions météo sont structurées autour de la température,
            l’humidité, le vent, les précipitations et des indicateurs de
            sécheresse.
          </p>
        </article>

        <article>
          <span>02</span>
          <h2>Évaluer</h2>
          <p>
            Le modèle LightGBM estime la probabilité de risque élevé et la
            convertit en un score lisible de 0 à 100.
          </p>
        </article>

        <article>
          <span>03</span>
          <h2>Prévenir</h2>
          <p>
            Chaque analyse est conservée dans votre historique afin de suivre
            les situations à surveiller.
          </p>
        </article>
      </div>

      <section className="risk-legend">
        <div>
          <p className="eyebrow">Niveaux d’alerte</p>
          <h2>Comprendre le score de risque</h2>
        </div>

        <div className="legend-items">
          <span className="legend faible">Faible</span>
          <span className="legend modere">Modéré</span>
          <span className="legend eleve">Élevé</span>
          <span className="legend critique">Critique</span>
        </div>
      </section>
    </section>
  );
}

export default HomePage;