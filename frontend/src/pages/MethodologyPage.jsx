function MethodologyPage() {
  return (
    <section className="methodology-page">
      <div className="methodology-hero">
        <p className="eyebrow">Méthodologie</p>
        <h1>Comment HeatShield AI estime le risque</h1>
        <p>
          Le projet combine des données météorologiques, du feature engineering
          et un modèle de machine learning afin de produire une estimation
          claire du risque d’incendie pendant les périodes de chaleur intense.
        </p>
      </div>

      <div className="methodology-grid">
        <article>
          <span>01</span>
          <h2>Données météo</h2>
          <p>
            Les analyses reposent sur des variables comme la température,
            l’humidité, le vent, les précipitations, l’évapotranspiration ET0,
            le VPD et le rayonnement solaire.
          </p>
        </article>

        <article>
          <span>02</span>
          <h2>Variables dérivées</h2>
          <p>
            Des indicateurs supplémentaires sont construits: moyennes mobiles,
            jours chauds consécutifs, indice chaleur-humidité, indice
            vent-sécheresse et intensité de vague de chaleur.
          </p>
        </article>

        <article>
          <span>03</span>
          <h2>Modèle ML</h2>
          <p>
            Le modèle LightGBM estime la probabilité d’un risque élevé à partir
            de 31 variables météorologiques et dérivées.
          </p>
        </article>

        <article>
          <span>04</span>
          <h2>Interprétation</h2>
          <p>
            La probabilité est convertie en score de 0 à 100 puis en niveau:
            Faible, Modéré, Élevé ou Critique.
          </p>
        </article>
      </div>

      <section className="importance-section">
        <div>
          <p className="eyebrow">Facteurs dominants</p>
          <h2>Les variables les plus importantes</h2>
          <p>
            Selon l’analyse d’importance du modèle, les facteurs les plus
            influents incluent le vent maximal, l’humidité, la température
            maximale, l’ET0, le VPD et les indicateurs combinant chaleur,
            humidité et sécheresse.
          </p>
        </div>

        <ul className="importance-list">
          <li><span>1</span> Vent maximal</li>
          <li><span>2</span> Humidité moyenne</li>
          <li><span>3</span> Température maximale</li>
          <li><span>4</span> Évapotranspiration ET0</li>
          <li><span>5</span> Ratio chaleur / humidité</li>
          <li><span>6</span> Déficit de pression de vapeur (VPD)</li>
        </ul>
      </section>

      <section className="disclaimer">
        <h2>Limite importante</h2>
        <p>
          HeatShield AI est un outil d’aide à la décision et de sensibilisation.
          Les résultats constituent une estimation basée sur les variables
          météo disponibles; ils ne remplacent pas les alertes officielles, les
          autorités de protection civile ni les analyses opérationnelles sur le
          terrain.
        </p>
      </section>
    </section>
  );
}

export default MethodologyPage;