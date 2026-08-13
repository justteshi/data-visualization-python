const numberFormatter = new Intl.NumberFormat("en-US");

function analyticsUrl() {
  return `${import.meta.env.BASE_URL}data/analytics.json`;
}

function assertSummary(summary) {
  if (
    !summary ||
    !summary.academicYears ||
    !summary.genderTotals ||
    !summary.mostCommonGrade ||
    !summary.largestStudyDurationGroup
  ) {
    throw new Error("The analytics export does not contain the required summary data.");
  }
}

export async function loadAnalytics() {
  const response = await fetch(analyticsUrl());
  if (!response.ok) {
    throw new Error(`Analytics data could not be loaded (HTTP ${response.status}).`);
  }

  const analytics = await response.json();
  assertSummary(analytics.summary);
  return analytics;
}

function createKpiCard({ label, value, description }) {
  return `
    <article class="panel kpi-card">
      <p>${label}</p>
      <strong>${value}</strong>
      <span>${description}</span>
    </article>
  `;
}

export function renderKpis(container, summary) {
  const cards = [
    {
      label: "Total students",
      value: numberFormatter.format(summary.totalStudents),
      description: "Represented in the study-duration distribution",
    },
    {
      label: "Academic years",
      value: numberFormatter.format(summary.academicYears.count),
      description: `${summary.academicYears.first}–${summary.academicYears.last} enrollment years`,
    },
    {
      label: "Female students",
      value: numberFormatter.format(summary.genderTotals.F),
      description: "Across the exported enrollment data",
    },
    {
      label: "Male students",
      value: numberFormatter.format(summary.genderTotals.M),
      description: "Across the exported enrollment data",
    },
    {
      label: "Most common final grade",
      value: `Grade ${summary.mostCommonGrade.grade}`,
      description: `${numberFormatter.format(summary.mostCommonGrade.count)} recorded results`,
    },
    {
      label: "Largest study-duration group",
      value: summary.largestStudyDurationGroup.label,
      description: `${numberFormatter.format(summary.largestStudyDurationGroup.count)} students`,
    },
  ];

  container.innerHTML = cards.map(createKpiCard).join("");
}

export function renderLoadingState(container) {
  container.setAttribute("aria-busy", "true");
  container.innerHTML = Array.from(
    { length: 6 },
    () => `
      <article class="panel kpi-card kpi-card-loading" aria-label="Loading key indicator">
        <span class="loading-line loading-line-short"></span>
        <span class="loading-line loading-line-value"></span>
        <span class="loading-line"></span>
      </article>
    `,
  ).join("");
}

export function renderErrorState(container, onRetry) {
  container.removeAttribute("aria-busy");
  container.innerHTML = `
    <div class="panel data-error" role="alert">
      <div>
        <p class="eyebrow">Data unavailable</p>
        <h3>Summary metrics could not be loaded.</h3>
        <p>Check that the static analytics export is available, then try again.</p>
      </div>
      <button class="retry-button" type="button">Try again</button>
    </div>
  `;
  container.querySelector("button").addEventListener("click", onRetry);
}
