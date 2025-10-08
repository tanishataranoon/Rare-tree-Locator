// dashboard.js
(function(){
  // helpers
  function qs(sel){ return document.querySelector(sel) }
  function qsa(sel){ return Array.from(document.querySelectorAll(sel)) }
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }
  const csrftoken = getCookie('csrftoken');

  // modal helpers
  function openModal(mod) { mod.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function closeModal(mod) { mod.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }

  // elements
  const createModal = qs('#createModal');
  const editModal = qs('#editModal');
  const deleteModal = qs('#deleteModal');

  // open create
  const openCreate = qs('#openCreateModal');
  if(openCreate){
    openCreate.addEventListener('click', (e)=>{
      e.preventDefault();
      openModal(createModal);
    });
  }
  // close create
  qs('#closeCreateModal')?.addEventListener('click', ()=> closeModal(createModal));
  qs('#cancelCreate')?.addEventListener('click', ()=> closeModal(createModal));

  // open edit buttons (dynamic)
  qsa('.edit-request-btn').forEach(btn=>{
    btn.addEventListener('click', e=>{
      e.preventDefault();
      const id = btn.dataset.id;
      qs('#edit_request_id').value = id;
      qs('#edit_title').value = btn.dataset.title || '';
      qs('#edit_description').value = btn.dataset.description || '';
      qs('#edit_location').value = btn.dataset.location || '';
      openModal(editModal);
    });
  });

  qs('#closeEditModal')?.addEventListener('click', ()=> closeModal(editModal));
  qs('#cancelEdit')?.addEventListener('click', ()=> closeModal(editModal));

  // delete
  qsa('.delete-request-btn').forEach(btn=>{
    btn.addEventListener('click', e=>{
      e.preventDefault();
      const id = btn.dataset.id;
      qs('#delete_request_id').value = id;
      openModal(deleteModal);
    });
  });
  qs('#closeDeleteModal')?.addEventListener('click', ()=> closeModal(deleteModal));
  qs('#cancelDelete')?.addEventListener('click', ()=> closeModal(deleteModal));

  // AJAX create
  const createForm = qs('#createRequestForm');
  if(createForm){
    createForm.addEventListener('submit', async function(e){
      e.preventDefault();
      const fd = new FormData(createForm);
      try{
        const res = await fetch(ajaxCreateUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: fd
        });
        const data = await res.json();
        if(res.ok && data.success){
          alert('Request created');
          closeModal(createModal);
          window.location.reload();
        } else {
          alert(data.error || 'Create failed');
        }
      }catch(err){ console.error(err); alert('Network error'); }
    });
  }

  // AJAX edit
  const editForm = qs('#editRequestForm');
  if(editForm){
    editForm.addEventListener('submit', async function(e){
      e.preventDefault();
      const id = qs('#edit_request_id').value;
      if(!id){ alert('Missing id'); return; }
      const fd = new FormData(editForm);
      try{
        const res = await fetch(ajaxUpdateUrl + id + '/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: fd
        });
        const data = await res.json();
        if(res.ok && data.success){
          alert('Request updated');
          closeModal(editModal);
          window.location.reload();
        } else {
          alert(data.error || 'Update failed');
        }
      }catch(err){ console.error(err); alert('Network error'); }
    });
  }

  // AJAX delete
  const deleteForm = qs('#deleteRequestForm');
  if(deleteForm){
    deleteForm.addEventListener('submit', async function(e){
      e.preventDefault();
      const id = qs('#delete_request_id').value;
      if(!id){ alert('Missing id'); return; }
      try{
        const res = await fetch(ajaxDeleteUrl + id + '/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: new FormData(deleteForm)
        });
        const data = await res.json();
        if(res.ok && data.success){
          alert('Deleted');
          closeModal(deleteModal);
          window.location.reload();
        } else {
          alert(data.error || 'Delete failed');
        }
      }catch(err){ console.error(err); alert('Network error'); }
    });
  }

  // click outside modal to close
  [createModal, editModal, deleteModal].forEach(m=>{
    if(!m) return;
    m.addEventListener('click', (ev)=>{
      if(ev.target === m) closeModal(m);
    });
  });

  // optional: answer buttons (for contributor)
  qsa('.answer-btn').forEach(b=>{
    b.addEventListener('click', e=>{
      e.preventDefault();
      const id = b.dataset.id;
      // simple redirect to request detail page (you likely have view to answer)
      window.location.href = `/requests/${id}/`; // adjust if your url differs
    });
  });

})();
