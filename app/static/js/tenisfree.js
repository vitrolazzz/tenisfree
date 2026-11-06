/**
 * tenisfree.js — Scripts específicos da área de produtos
 * Carregado apenas nas páginas de listagem, detalhe, criar e editar.
 */

'use strict';

// ── Preview de imagem em tempo real ──────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const imgInput   = document.getElementById('imgUrlInput');
  const previewImg = document.getElementById('imgPreview');
  const previewWrap= document.getElementById('imgPreviewWrap');

  if (!imgInput) return;

  function updatePreview() {
    const url = imgInput.value.trim();
    if (url) {
      previewImg.src = url;
      previewWrap.style.display = 'block';
    } else {
      previewWrap.style.display = 'none';
      previewImg.src = '';
    }
  }

  imgInput.addEventListener('input', updatePreview);
  imgInput.addEventListener('change', updatePreview);

  // Inicializa caso já exista valor (edição)
  if (imgInput.value.trim()) updatePreview();

  // Esconde preview se a imagem falhar ao carregar
  if (previewImg) {
    previewImg.addEventListener('error', () => {
      previewWrap.style.display = 'none';
    });
  }
});

// ── Confirmação de exclusão por teclado (acessibilidade) ─────────────
document.addEventListener('DOMContentLoaded', () => {
  const deleteModal = document.getElementById('modalExcluir');
  if (!deleteModal) return;

  deleteModal.addEventListener('shown.bs.modal', () => {
    const cancelBtn = deleteModal.querySelector('[data-bs-dismiss="modal"]');
    if (cancelBtn) cancelBtn.focus();
  });
});
