/**
 * main.js — Scripts globais TenisFree
 * Carregado em todas as páginas via base.html
 */

'use strict';

// ── Auto-fechar alertas após 5 s ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  });
});
