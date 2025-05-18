let topicCount = 0;

function addTopic() {
  const topicsContainer = document.getElementById('topicsContainer');
  const topicId = topicCount++;

  const topicHTML = `
    <div class="topic" data-topic="${topicId}" style="margin-top:1em; padding:1em; border:1px solid #ccc;">
      <h3>Tema ${topicId + 1}</h3>
      <input type="text" name="topicTitle" placeholder="Título del tema" class="field" required>
      <textarea name="topicDescription" placeholder="Descripción del tema" class="field" required></textarea>
      <input type="number" step="0.1" name="topicWeight" placeholder="Peso (%)" class="field" required>

      <label><strong>Corte:</strong></label>
      <select name="topicCorte" class="field" required>
        <option value="">Seleccionar corte</option>
        <option value="1">Corte 1</option>
        <option value="2">Corte 2</option>
        <option value="3">Corte 3</option>
      </select>

      <div class="topic-links" id="topic-links-${topicId}"></div>
      <button type="button" onclick="addLinkField('topic-links-${topicId}')">+ Link del Tema</button>

      <div class="activities" id="activities-${topicId}"></div>
      <button type="button" onclick="addActivity(${topicId})">+ Agregar Actividad</button>
    </div>
  `;
  topicsContainer.insertAdjacentHTML('beforeend', topicHTML);
}

function addActivity(topicId) {
  const activitiesContainer = document.getElementById(`activities-${topicId}`);
  const activityIndex = activitiesContainer.childElementCount;

  const activityHTML = `
    <div class="activity" style="margin-top:1em;">
      <input type="text" name="activityTitle" placeholder="Título de la actividad" class="field" required>
      <textarea name="activityDescription" placeholder="Descripción" class="field" required></textarea>
      <input type="number" step="0.1" name="activityWeight" placeholder="Peso (%)" class="field" required>

      <div class="activity-links" id="activity-links-${topicId}-${activityIndex}"></div>
      <button type="button" onclick="addLinkField('activity-links-${topicId}-${activityIndex}')">+ Link de Actividad</button>
    </div>
  `;
  activitiesContainer.insertAdjacentHTML('beforeend', activityHTML);
}

function addLinkField(containerId) {
  const container = document.getElementById(containerId);
  const input = `<input type="url" name="link" placeholder="https://ejemplo.com" class="field" style="margin-top: 4px;" required>`;
  container.insertAdjacentHTML('beforeend', input);
}

document.getElementById('courseForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const title = form.title.value;
  const description = form.description.value;

  const topicsDivs = document.querySelectorAll('.topic');
  let topics = [];

  topicsDivs.forEach(topicDiv => {
    const topicTitle = topicDiv.querySelector('input[name="topicTitle"]').value;
    const topicDescription = topicDiv.querySelector('textarea[name="topicDescription"]').value;
    const topicWeight = topicDiv.querySelector('input[name="topicWeight"]').value;
    const topicCorte = parseInt(topicDiv.querySelector('select[name="topicCorte"]').value);

    const topicLinks = Array.from(topicDiv.querySelectorAll('.topic-links input[name="link"]')).map(i => i.value);

    const activitiesDivs = topicDiv.querySelectorAll('.activity');
    let activities = [];

    activitiesDivs.forEach(activityDiv => {
      const actTitle = activityDiv.querySelector('input[name="activityTitle"]').value;
      const actDescription = activityDiv.querySelector('textarea[name="activityDescription"]').value;
      const actWeight = activityDiv.querySelector('input[name="activityWeight"]').value;
      const activityLinks = Array.from(activityDiv.querySelectorAll('.activity-links input[name="link"]')).map(i => i.value);

      activities.push({
        title: actTitle,
        description: actDescription,
        weight: parseFloat(actWeight),
        links: activityLinks
      });
    });

    topics.push({
      title: topicTitle,
      description: topicDescription,
      weight: topicWeight,
      corte: topicCorte,
      links: topicLinks,
      activities: activities
    });
  });

  const data = { title, description, topics };

  try {
    const response = await fetch('/create_course', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      window.location.href = '/dashboard';
    } else {
      alert('Error al crear el curso.');
    }
  } catch (error) {
    alert('Error al enviar datos.');
    console.error(error);
  }
});