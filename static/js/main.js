// Flash auto-dismiss
document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(f => {
    setTimeout(() => f.style.opacity = '0', 4000);
    setTimeout(() => f.remove(), 4500);
    f.querySelector('.flash-close')?.addEventListener('click', () => f.remove());
  });

  // Sidebar hamburger
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.querySelector('.sidebar');
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Upload zone
  const uploadZone = document.querySelector('.upload-zone');
  const fileInput = document.getElementById('image');
  const imgPreview = document.getElementById('img-preview');
  if (uploadZone && fileInput) {
    uploadZone.addEventListener('click', () => fileInput.click());
    uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
    uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
    uploadZone.addEventListener('drop', e => {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');
      const files = e.dataTransfer.files;
      if (files.length) {
        fileInput.files = files;
        previewImage(files[0]);
      }
    });
    fileInput.addEventListener('change', e => {
      if (e.target.files[0]) previewImage(e.target.files[0]);
    });
  }

  function previewImage(file) {
    if (!imgPreview) return;
    const reader = new FileReader();
    reader.onload = e => {
      imgPreview.src = e.target.result;
      imgPreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  // Modals
  document.querySelectorAll('[data-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.dataset.modal;
      document.getElementById(modalId)?.classList.add('open');
    });
  });
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.classList.remove('open');
    });
  });
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('.modal-overlay')?.classList.remove('open'));
  });

  // Edit admin modal
  document.querySelectorAll('.edit-admin-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const aid = btn.dataset.id;
      const name = btn.dataset.name;
      const email = btn.dataset.email;
      const blocks = JSON.parse(btn.dataset.blocks || '[]');
      const modal = document.getElementById('edit-admin-modal');
      if (!modal) return;
      modal.querySelector('[name=aid]').value = aid;
      modal.querySelector('[name=name]').value = name;
      modal.querySelector('[name=email]').value = email;
      modal.querySelectorAll('[name=blocks]').forEach(cb => {
        cb.checked = blocks.includes(cb.value);
      });
      modal.querySelector('form').action = `/superadmin/admin/${aid}/edit`;
      modal.classList.add('open');
    });
  });

  // Update complaint modal
  document.querySelectorAll('.update-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const cid = btn.dataset.id;
      const status = btn.dataset.status;
      const remarks = btn.dataset.remarks || '';
      const modal = document.getElementById('update-modal');
      if (!modal) return;
      modal.querySelector('[name=status]').value = status;
      modal.querySelector('[name=remarks]').value = remarks;
      modal.querySelector('form').action = btn.dataset.action;
      modal.classList.add('open');
    });
  });

  // Profile Menu Toggle
  const profileTrigger = document.getElementById('profile-trigger');
  const profilePopup = document.getElementById('profile-popup');
  
  if (profileTrigger && profilePopup) {
    profileTrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      profileTrigger.classList.toggle('active');
      profilePopup.classList.toggle('show');
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!profileTrigger.contains(e.target)) {
        profileTrigger.classList.remove('active');
        profilePopup.classList.remove('show');
      }
    });

    // Prevent closing when clicking inside popup
    profilePopup.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  }
});
