// dashboard.js
(function () {
  // Utility Helpers
  function qs(sel) { return document.querySelector(sel); }
  function qsa(sel) { return Array.from(document.querySelectorAll(sel)); }
  function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }
  const csrftoken = getCookie('csrftoken') || qs('[name=csrfmiddlewaretoken]')?.value || '';

  // === Sidebar Rail Pin/Expand Logic ===
  const sidebarRail = qs('#sidebarRail');
  const toggleBtn = qs('#toggleSidebar');

  // Load saved sidebar state from localStorage
  if (sidebarRail && localStorage.getItem('sidebar_expanded') === 'true') {
    sidebarRail.classList.add('is-expanded');
  }

  if (toggleBtn && sidebarRail) {
    toggleBtn.addEventListener('click', () => {
      sidebarRail.classList.toggle('is-expanded');
      const isExpanded = sidebarRail.classList.contains('is-expanded');
      localStorage.setItem('sidebar_expanded', isExpanded ? 'true' : 'false');
    });
  }

  // Modal Helpers
  function openModal(mod) {
    if (!mod) return;
    mod.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal(mod) {
    if (!mod) return;
    mod.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // Modal Elements
  const createModal = qs('#createModal');
  const editModal = qs('#editModal');
  const deleteModal = qs('#deleteModal');

  // Open Create
  const openCreate = qs('#openCreateModal');
  if (openCreate) {
    openCreate.addEventListener('click', (e) => {
      e.preventDefault();
      openModal(createModal);
    });
  }
  qs('#closeCreateModal')?.addEventListener('click', () => closeModal(createModal));
  qs('#cancelCreate')?.addEventListener('click', () => closeModal(createModal));

  // Edit Dynamic Trigger
  qsa('.edit-request-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const id = btn.dataset.id;
      if (qs('#edit_request_id')) qs('#edit_request_id').value = id;
      if (qs('#edit_title')) qs('#edit_title').value = btn.dataset.title || '';
      if (qs('#edit_description')) qs('#edit_description').value = btn.dataset.description || '';
      if (qs('#edit_location')) qs('#edit_location').value = btn.dataset.location || '';
      openModal(editModal);
    });
  });
  qs('#closeEditModal')?.addEventListener('click', () => closeModal(editModal));
  qs('#cancelEdit')?.addEventListener('click', () => closeModal(editModal));

  // Delete Dynamic Trigger
  qsa('.delete-request-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const id = btn.dataset.id;
      if (qs('#delete_request_id')) qs('#delete_request_id').value = id;
      openModal(deleteModal);
    });
  });
  qs('#closeDeleteModal')?.addEventListener('click', () => closeModal(deleteModal));
  qs('#cancelDelete')?.addEventListener('click', () => closeModal(deleteModal));

  // AJAX Create Submit
  const createForm = qs('#createRequestForm');
  if (createForm) {
    createForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (typeof ajaxCreateUrl === 'undefined') {
        console.error('ajaxCreateUrl is not defined');
        return;
      }
      try {
        const res = await fetch(ajaxCreateUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: new FormData(createForm)
        });
        const data = await res.json();
        if (res.ok && data.success) {
          closeModal(createModal);
          window.location.reload();
        } else {
          alert(data.error || 'Create failed');
        }
      } catch (err) {
        console.error(err);
        alert('Network error');
      }
    });
  }

  // AJAX Edit Submit
  const editForm = qs('#editRequestForm');
  if (editForm) {
    editForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (typeof ajaxUpdateUrl === 'undefined') {
        console.error('ajaxUpdateUrl is not defined');
        return;
      }
      const id = qs('#edit_request_id')?.value;
      if (!id) return;
      try {
        const res = await fetch(ajaxUpdateUrl + id + '/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: new FormData(editForm)
        });
        const data = await res.json();
        if (res.ok && data.success) {
          closeModal(editModal);
          window.location.reload();
        } else {
          alert(data.error || 'Update failed');
        }
      } catch (err) {
        console.error(err);
        alert('Network error');
      }
    });
  }

  // AJAX Delete Submit
  const deleteForm = qs('#deleteRequestForm');
  if (deleteForm) {
    deleteForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (typeof ajaxDeleteUrl === 'undefined') {
        console.error('ajaxDeleteUrl is not defined');
        return;
      }
      const id = qs('#delete_request_id')?.value;
      if (!id) return;
      try {
        const res = await fetch(ajaxDeleteUrl + id + '/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: new FormData(deleteForm)
        });
        const data = await res.json();
        if (res.ok && data.success) {
          closeModal(deleteModal);
          window.location.reload();
        } else {
          alert(data.error || 'Delete failed');
        }
      } catch (err) {
        console.error(err);
        alert('Network error');
      }
    });
  }

  // Close modals when clicking overlay backdrop
  [createModal, editModal, deleteModal].forEach(m => {
    if (!m) return;
    m.addEventListener('click', (ev) => {
      if (ev.target === m) closeModal(m);
    });
  });
})();