function renderSubjectInputs() {
  const courseSelect = document.getElementById("course-select");
  const subjectsContainer = document.getElementById("subjects-container");

  if (!courseSelect || !subjectsContainer || !window.courseSubjects) {
    return;
  }

  const selectedCourse = courseSelect.value;
  const existingSubjects = safeParseSubjects(subjectsContainer.dataset.subjects);
  const subjectMap = new Map(existingSubjects.map((subject) => [subject.subject_name, subject]));
  const subjects = window.courseSubjects[selectedCourse] || [];

  subjectsContainer.innerHTML = subjects.map((subjectName, index) => {
    const existing = subjectMap.get(subjectName) || {};
    const marks = Number(existing.marks || 0);
    return `
      <article class="subject-card">
        <h4>${escapeHtml(subjectName)}</h4>
        <p>Subject assigned automatically from the selected course.</p>
        <div class="subject-input-grid">
          <label>
            <span>Attendance (%)</span>
            <input type="number" name="attendance_${index}" min="0" max="100" value="${existing.attendance ?? 0}" required>
          </label>
          <label>
            <span>Assignments</span>
            <input type="number" name="assignments_${index}" min="0" value="${existing.assignments_count ?? 0}" required>
          </label>
          <label>
            <span>Marks</span>
            <input type="number" name="marks_${index}" min="0" max="100" step="0.01" value="${existing.marks ?? 0}" required>
          </label>
        </div>
        <span class="pill ${marks >= 40 ? "ok" : "pending"}">${marks >= 40 ? "On Track" : "Needs Improvement"}</span>
      </article>
    `;
  }).join("");
}

function safeParseSubjects(value) {
  if (!value) {
    return [];
  }

  try {
    return JSON.parse(value);
  } catch (error) {
    return [];
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

document.addEventListener("DOMContentLoaded", () => {
  const courseSelect = document.getElementById("course-select");
  if (!courseSelect) {
    return;
  }

  renderSubjectInputs();
  courseSelect.addEventListener("change", renderSubjectInputs);
});
