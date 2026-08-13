import "./styles/main.css";
import {
  loadAnalytics,
  renderErrorState,
  renderKpis,
  renderLoadingState,
} from "./dashboard.js";
import { renderCharts } from "./charts.js";

const app = document.querySelector("#app");

app.innerHTML = `
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="#overview" aria-label="University Analytics home">
        <span class="brand-mark" aria-hidden="true">UA</span>
        <span>University Analytics</span>
      </a>
      <nav class="primary-nav" aria-label="Primary navigation">
        <a href="#overview">Overview</a>
        <a href="#insights">Insights</a>
        <a href="#data">Data</a>
      </nav>
      <a class="topbar-action" href="#data">View data source</a>
    </header>

    <main>
      <section class="hero" id="overview" aria-labelledby="page-title">
        <p class="eyebrow">University performance intelligence</p>
        <div class="hero-content">
          <div>
            <h1 id="page-title">A clearer view of academic outcomes.</h1>
            <p class="hero-copy">
              A focused workspace for exploring student progression, academic performance,
              and enrollment patterns.
            </p>
          </div>
          <div class="data-status" id="data">
            <span class="status-dot" aria-hidden="true"></span>
            <span id="data-status-text" aria-live="polite">Loading analytics export</span>
          </div>
        </div>
      </section>

      <section class="kpi-section" aria-labelledby="kpi-heading">
        <div class="section-heading">
          <div>
            <p class="eyebrow">At a glance</p>
            <h2 id="kpi-heading">Key indicators</h2>
          </div>
          <p>Summary metrics are sourced from the static analytics export.</p>
        </div>
        <div class="kpi-grid" id="kpi-grid" aria-live="polite"></div>
      </section>

      <section class="insights-section" id="insights" aria-labelledby="insights-heading">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Analysis workspace</p>
            <h2 id="insights-heading">Charts and trends</h2>
          </div>
          <p>Interactive views use the same static analytics export as the summary.</p>
        </div>
        <div class="chart-grid">
          <article class="panel chart-panel chart-panel-large">
            <div class="panel-heading">
              <div>
                <h3>Students starting university by gender and year</h3>
                <p>Compare enrollment counts for each year from 2000 to 2014.</p>
              </div>
            </div>
            <div class="chart-canvas-wrap chart-canvas-wide">
              <canvas id="enrollment-chart" role="img" aria-label="Grouped bar chart of students starting university by gender and year"></canvas>
            </div>
          </article>
          <article class="panel chart-panel">
            <div class="panel-heading">
              <div>
                <h3>Final grade distribution</h3>
                <p>Recorded results across final grades 2 through 6.</p>
              </div>
            </div>
            <div class="chart-canvas-wrap">
              <canvas id="grade-chart" role="img" aria-label="Bar chart of recorded final grade results"></canvas>
            </div>
          </article>
          <article class="panel chart-panel chart-panel-duration">
            <div class="panel-heading">
              <div>
                <h3>Study duration distribution</h3>
                <p>Students grouped by time spent at university.</p>
              </div>
            </div>
            <div class="chart-canvas-wrap">
              <canvas id="duration-chart" role="img" aria-label="Horizontal bar chart of study duration groups"></canvas>
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <span>University Analytics</span>
      <span>Static analytics pipeline · Dashboard foundation</span>
    </footer>
  </div>
`;

const kpiGrid = document.querySelector("#kpi-grid");
const dataStatus = document.querySelector("#data-status-text");

async function populateDashboard() {
  renderLoadingState(kpiGrid);
  dataStatus.textContent = "Loading analytics export";

  try {
    const analytics = await loadAnalytics();
    const { summary } = analytics;
    renderKpis(kpiGrid, summary);
    renderCharts(analytics);
    kpiGrid.removeAttribute("aria-busy");
    dataStatus.textContent = "Analytics export loaded";
  } catch (error) {
    renderErrorState(kpiGrid, populateDashboard);
    dataStatus.textContent = "Analytics export unavailable";
    console.error(error);
  }
}

populateDashboard();
