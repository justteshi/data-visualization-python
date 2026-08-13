import Chart from "chart.js/auto";

const genderLabels = { M: "Male", F: "Female" };

function chartTheme() {
  const styles = getComputedStyle(document.documentElement);
  return {
    accent: styles.getPropertyValue("--color-accent").trim(),
    text: styles.getPropertyValue("--color-text").trim(),
    muted: styles.getPropertyValue("--color-text-muted").trim(),
    border: styles.getPropertyValue("--color-border").trim(),
    surface: styles.getPropertyValue("--color-surface").trim(),
    female: styles.getPropertyValue("--color-chart-female").trim(),
    male: styles.getPropertyValue("--color-accent").trim(),
    duration: [
      styles.getPropertyValue("--color-chart-duration-1").trim(),
      styles.getPropertyValue("--color-chart-duration-2").trim(),
      styles.getPropertyValue("--color-chart-duration-3").trim(),
      styles.getPropertyValue("--color-accent").trim(),
    ],
  };
}

function sharedOptions(theme) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 350 },
    plugins: {
      legend: {
        labels: { boxWidth: 10, boxHeight: 10, color: theme.muted, padding: 16 },
      },
      tooltip: {
        backgroundColor: theme.surface,
        borderColor: theme.border,
        borderWidth: 1,
        titleColor: theme.text,
        bodyColor: theme.muted,
        padding: 10,
        displayColors: false,
      },
    },
  };
}

function cartesianScales(theme, { horizontal = false, valueLabel = "Students" } = {}) {
  const valueAxis = {
    beginAtZero: true,
    ticks: { color: theme.muted, precision: 0 },
    title: { display: true, text: valueLabel, color: theme.muted, padding: { top: 8 } },
    grid: { color: theme.border },
    border: { display: false },
  };
  const labelAxis = {
    ticks: { color: theme.muted },
    grid: { display: false },
    border: { display: false },
  };

  return horizontal ? { x: valueAxis, y: labelAxis } : { x: labelAxis, y: valueAxis };
}

function renderGradeDistribution(canvas, analytics, theme) {
  const grades = analytics.gradeDistribution;
  return new Chart(canvas, {
    type: "bar",
    data: {
      labels: grades.map(({ grade }) => `Grade ${grade}`),
      datasets: [
        {
          label: "Recorded results",
          data: grades.map(({ count }) => count),
          backgroundColor: theme.accent,
          borderRadius: 3,
          borderSkipped: false,
          maxBarThickness: 48,
        },
      ],
    },
    options: {
      ...sharedOptions(theme),
      plugins: {
        ...sharedOptions(theme).plugins,
        legend: { display: false },
        tooltip: {
          ...sharedOptions(theme).plugins.tooltip,
          callbacks: { label: (context) => `${context.parsed.y} recorded results` },
        },
      },
      scales: cartesianScales(theme, { valueLabel: "Recorded results" }),
    },
  });
}

function renderEnrollmentByGender(canvas, analytics, theme) {
  const records = analytics.studentsByGenderAndYear;
  const years = [...new Set(records.map(({ year }) => year))];
  const dataForGender = (gender) =>
    years.map(
      (year) => records.find((record) => record.year === year && record.gender === gender)?.count ?? 0,
    );

  return new Chart(canvas, {
    type: "bar",
    data: {
      labels: years.map(String),
      datasets: [
        { label: genderLabels.M, data: dataForGender("M"), backgroundColor: theme.male, borderRadius: 2 },
        { label: genderLabels.F, data: dataForGender("F"), backgroundColor: theme.female, borderRadius: 2 },
      ],
    },
    options: {
      ...sharedOptions(theme),
      scales: {
        ...cartesianScales(theme),
        x: {
          ...cartesianScales(theme).x,
          title: { display: true, text: "Enrollment year", color: theme.muted, padding: { top: 8 } },
        },
      },
    },
  });
}

function renderStudyDuration(canvas, analytics, theme) {
  const durations = analytics.studyDuration;
  return new Chart(canvas, {
    type: "bar",
    data: {
      labels: durations.map(({ label }) => label),
      datasets: [
        {
          label: "Students",
          data: durations.map(({ count }) => count),
          backgroundColor: theme.duration,
          borderRadius: 3,
          borderSkipped: false,
        },
      ],
    },
    options: {
      ...sharedOptions(theme),
      indexAxis: "y",
      plugins: {
        ...sharedOptions(theme).plugins,
        legend: { display: false },
        tooltip: {
          ...sharedOptions(theme).plugins.tooltip,
          callbacks: { label: (context) => `${context.parsed.x} students` },
        },
      },
      scales: cartesianScales(theme, { horizontal: true }),
    },
  });
}

export function renderCharts(analytics) {
  const theme = chartTheme();
  return [
    renderGradeDistribution(document.querySelector("#grade-chart"), analytics, theme),
    renderEnrollmentByGender(document.querySelector("#enrollment-chart"), analytics, theme),
    renderStudyDuration(document.querySelector("#duration-chart"), analytics, theme),
  ];
}
