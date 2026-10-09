'use strict';
const $ = selector => document.querySelector(selector);
let opportunities = [];
let deletingId = null;
let loading = false;
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
function notify(message, error = false) {
  const notice = $('#notice'); notice.textContent = message;
  notice.className = error ? 'error' : ''; notice.hidden = false;
}
async function api(path = '', method = 'GET', data) {
  let response;
  try { response = await fetch('/api/opportunities' + path, {
    method, headers: data ? {'Content-Type':'application/json'} : {},
    body: data ? JSON.stringify(data) : undefined
  }); } catch { throw new Error('Cannot connect to the server. Check that the backend is running.'); }
  const body = await response.json();
  if (!response.ok) throw new Error(body.errors ? Object.entries(body.errors).map(([key,value]) => `${key}: ${value}`).join('\n') : body.message || 'Request failed.');
  return body;
}
function render() {
  $('#total-count').textContent = opportunities.length;
  const open = opportunities.filter(item => item.status === 'Open');
  $('#open-count').textContent = open.length;
  $('#positions-count').textContent = open.reduce((sum,item) => sum + item.available_positions, 0);
  const query = $('#search').value.toLowerCase().trim(), status = $('#status-filter').value;
  const visible = opportunities.filter(item => (status === 'all' || item.status === status) &&
    [item.title,item.research_area,item.faculty_name,item.department].some(value => value.toLowerCase().includes(query)));
  $('#opportunities').innerHTML = visible.length ? visible.map(item => `
    <article class="card"><div class="card-top"><span class="area">${escapeHtml(item.research_area)}</span><span class="badge ${item.status === 'Closed' ? 'closed' : ''}">${item.status}</span></div>
    <h3>${escapeHtml(item.title)}</h3><p class="description">${escapeHtml(item.description.length > 110 ? item.description.slice(0,110) + '...' : item.description)}</p>
    <div class="meta"><b>${escapeHtml(item.faculty_name)}</b><br>${escapeHtml(item.department)}<br>${item.available_positions} position${item.available_positions === 1 ? '' : 's'} · Deadline ${escapeHtml(item.application_deadline)}</div>
    <div class="actions"><button class="secondary" data-action="view" data-id="${item.id}">Details</button><button class="secondary" data-action="edit" data-id="${item.id}">Edit</button><button class="secondary" data-action="status" data-id="${item.id}">${item.status === 'Open' ? 'Close' : 'Reopen'}</button><button class="delete-link" data-action="delete" data-id="${item.id}">Delete</button></div></article>`).join('') : '<div class="empty">No opportunities found. Post an opportunity or adjust your search.</div>';
}
async function load() {
  if (loading) return; loading = true; $('#refresh').disabled = true;
  try { opportunities = (await api()).data; render(); }
  catch (error) { notify(error.message, true); $('#opportunities').innerHTML = '<div class="empty">Could not load opportunities. Check the database connection and click Refresh.</div>'; }
  finally { loading = false; $('#refresh').disabled = false; }
}
function openEditor(item) {
  $('#opportunity-form').reset(); $('#opportunity-id').value = item ? item.id : '';
  $('#form-title').textContent = item ? 'Edit research opportunity' : 'Post a research opportunity';
  $('#form-error').hidden = true;
  if (item) for (const [key,value] of Object.entries(item)) {
    const field = $('#opportunity-form').elements.namedItem(key); if (field) field.value = value;
  }
  $('#editor').showModal();
}
$('#new-opportunity').addEventListener('click', () => openEditor());
document.querySelectorAll('.close-editor').forEach(button => button.addEventListener('click', () => $('#editor').close()));
$('#close-details').addEventListener('click', () => $('#details').close());
$('#cancel-delete').addEventListener('click', () => $('#delete-dialog').close());
$('#refresh').addEventListener('click', load);
$('#search').addEventListener('input', render);
$('#status-filter').addEventListener('change', render);
$('#opportunity-form').addEventListener('submit', async event => {
  event.preventDefault(); const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form));
  for (const key of Object.keys(data)) if (typeof data[key] === 'string') data[key] = data[key].trim();
  data.available_positions = Number(data.available_positions);
  const id = $('#opportunity-id').value;
  $('#save').disabled = true; $('#form-error').hidden = true;
  try { const result = await api(id ? '/' + id : '', id ? 'PUT' : 'POST', data);
    $('#editor').close(); await load(); notify(result.message);
  } catch (error) { $('#form-error').textContent = error.message; $('#form-error').hidden = false; }
  finally { $('#save').disabled = false; }
});
$('#opportunities').addEventListener('click', async event => {
  const button = event.target.closest('button[data-action]'); if (!button) return;
  const id = Number(button.dataset.id); button.disabled = true;
  try {
    const item = (await api('/' + id)).data;
    if (button.dataset.action === 'edit') openEditor(item);
    if (button.dataset.action === 'view') {
      $('#detail-content').innerHTML = `<h2>${escapeHtml(item.title)}</h2><p class="details-description">${escapeHtml(item.description)}</p><dl>${[['ID',item.id],['Research area',item.research_area],['Faculty member',item.faculty_name],['Department',item.department],['Required skills',item.required_skills],['Positions',item.available_positions],['Deadline',item.application_deadline],['Status',item.status]].map(([key,value]) => `<dt>${key}</dt><dd>${escapeHtml(value)}</dd>`).join('')}</dl>`;
      $('#details').showModal();
    }
    if (button.dataset.action === 'status') { const result = await api('/' + id, 'PUT', {status:item.status === 'Open' ? 'Closed' : 'Open'}); await load(); notify(result.message); }
    if (button.dataset.action === 'delete') { deletingId = id; $('#delete-description').textContent = item.title; $('#delete-dialog').showModal(); }
  } catch(error) { notify(error.message, true); }
  finally { button.disabled = false; }
});
$('#confirm-delete').addEventListener('click', async () => {
  $('#confirm-delete').disabled = true;
  try { const result = await api('/' + deletingId, 'DELETE'); $('#delete-dialog').close(); await load(); notify(result.message); }
  catch(error) { $('#delete-dialog').close(); notify(error.message, true); }
  finally { $('#confirm-delete').disabled = false; }
});
load();
