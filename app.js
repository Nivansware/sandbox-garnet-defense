/**
 * ==========================================================================
 * BUKUKAS MANDIRI NIVANSWARE - MAIN APPLICATION CONTROLLER
 * Single Page Architecture | Ergonomic Mobile & Desktop Flow
 * Sesuai Doktrin Anti-AI Writing Style & Cultural Localization (ID, EN, JA)
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  const store = window.bukuKasStore;
  const chartEngine = window.nativeChart;
  const icons = window.uiIcons;
  const i18n = window.i18n;

  // Cache DOM Elements
  const heroBalanceEl = document.getElementById('hero-balance-val');
  const heroIncomeEl = document.getElementById('hero-income-val');
  const heroExpenseEl = document.getElementById('hero-expense-val');
  const heroCurrencySymbolEl = document.getElementById('hero-currency-symbol');

  const navItems = document.querySelectorAll('.nav-item');
  const tabViews = document.querySelectorAll('.tab-view');
  const langBtns = document.querySelectorAll('.btn-lang');

  const txListContainer = document.getElementById('tx-list-container');
  const txCountBadge = document.getElementById('tx-count-badge');
  const txSearchInput = document.getElementById('tx-search-input');
  const txFilterType = document.getElementById('tx-filter-type');
  const txFilterCategory = document.getElementById('tx-filter-category');

  // Progressive Load More Elements & State
  const txLoadMoreWrap = document.getElementById('tx-load-more-wrap');
  const btnLoadMoreTx = document.getElementById('btn-load-more-tx');
  const textLoadMore = document.getElementById('text-load-more');
  const iconLoadMore = document.getElementById('icon-load-more');
  let txDisplayLimit = 10;
  const TX_PAGE_STEP = 10;

  const reportTableBody = document.getElementById('report-table-body');
  const tableTotalIncome = document.getElementById('table-total-income');
  const tableTotalExpense = document.getElementById('table-total-expense');
  const tableTotalBalance = document.getElementById('table-total-balance');

  // Report Table Pagination Elements & State
  const reportPaginationBar = document.getElementById('report-pagination-bar');
  const reportPaginationInfo = document.getElementById('report-pagination-info');
  const btnReportPrev = document.getElementById('btn-report-prev');
  const btnReportNext = document.getElementById('btn-report-next');
  const reportPageNumbers = document.getElementById('report-page-numbers');
  const iconPagePrev = document.getElementById('icon-page-prev');
  const iconPageNext = document.getElementById('icon-page-next');
  let reportCurrentPage = 1;
  const REPORT_PAGE_SIZE = 10;

  const notesGridContainer = document.getElementById('notes-grid-container');
  const incomeCatList = document.getElementById('income-categories-list');
  const expenseCatList = document.getElementById('expense-categories-list');

  // Modals
  const modalTx = document.getElementById('modal-transaction');
  const modalNote = document.getElementById('modal-note');
  const modalCategory = document.getElementById('modal-category');
  const modalBackup = document.getElementById('modal-backup');
  const modalConfirm = document.getElementById('modal-confirm');

  // Confirmation Modal Elements
  const confirmModalTitle = document.getElementById('confirm-modal-title');
  const confirmModalDesc = document.getElementById('confirm-modal-desc');
  const confirmModalIcon = document.getElementById('confirm-modal-icon');
  const btnConfirmCancel = document.getElementById('btn-confirm-cancel');
  const btnConfirmProceed = document.getElementById('btn-confirm-proceed');
  let confirmCallback = null;

  // Transaction Form Elements
  const formTx = document.getElementById('form-transaction');
  const txTypeVal = document.getElementById('tx-type-val');
  const btnTypeIncome = document.getElementById('btn-type-income');
  const btnTypeExpense = document.getElementById('btn-type-expense');
  const txAmountInput = document.getElementById('tx-amount-input');
  const txCategorySelect = document.getElementById('tx-category-select');
  const txDateInput = document.getElementById('tx-date-input');
  const txTimeInput = document.getElementById('tx-time-input');
  const txNoteInput = document.getElementById('tx-note-input');

  // Note Form Elements
  const formNote = document.getElementById('form-note');
  const noteTitleInput = document.getElementById('note-title-input');
  const noteTagSelect = document.getElementById('note-tag-select');
  const noteContentInput = document.getElementById('note-content-input');
  const notePinCheckbox = document.getElementById('note-pin-checkbox');

  // Category Form Elements
  const formCategory = document.getElementById('form-category');
  const catTypeSelect = document.getElementById('cat-type-select');
  const catNameInput = document.getElementById('cat-name-input');
  const catIconSelect = document.getElementById('cat-icon-select');
  const catColorInput = document.getElementById('cat-color-input');

  // Profile Form Elements
  const profileBizName = document.getElementById('profile-biz-name');
  const profileOwnerName = document.getElementById('profile-owner-name');
  const profilePhone = document.getElementById('profile-phone');

  // ==========================================
  // INJEKSI STATIC UI ICONS (DOKTRIN ICONOGRAPHY)
  // ==========================================
  function injectStaticIcons() {
    if (!icons) return;

    const navTx = document.getElementById('nav-icon-tx');
    const navReports = document.getElementById('nav-icon-reports');
    const navNotes = document.getElementById('nav-icon-notes');
    const navCat = document.getElementById('nav-icon-cat');
    const navWisdom = document.getElementById('nav-icon-wisdom');
    if (navTx) navTx.innerHTML = icons.get('receipt', { size: 18 });
    if (navReports) navReports.innerHTML = icons.get('barChart', { size: 18 });
    if (navNotes) navNotes.innerHTML = icons.get('fileText', { size: 18 });
    if (navCat) navCat.innerHTML = icons.get('tag', { size: 18 });
    if (navWisdom) navWisdom.innerHTML = icons.get('compass', { size: 18 });

    const iconQuickInc = document.getElementById('icon-quick-income');
    const iconQuickExp = document.getElementById('icon-quick-expense');
    if (iconQuickInc) iconQuickInc.innerHTML = icons.get('plus', { size: 18 });
    if (iconQuickExp) iconQuickExp.innerHTML = icons.get('minus', { size: 18 });

    const searchHolder = document.getElementById('icon-search-holder');
    if (searchHolder) searchHolder.innerHTML = icons.get('search', { size: 16 });

    const printAction = document.getElementById('icon-print-action');
    const chartTrend = document.getElementById('icon-chart-trend');
    const chartDonut = document.getElementById('icon-chart-donut');
    if (printAction) printAction.innerHTML = icons.get('printer', { size: 18 });
    if (chartTrend) chartTrend.innerHTML = icons.get('barChart', { size: 18 });
    if (chartDonut) chartDonut.innerHTML = icons.get('pieChart', { size: 18 });

    const btnNoteIcon = document.getElementById('icon-btn-note');
    if (btnNoteIcon) btnNoteIcon.innerHTML = icons.get('pencil', { size: 18 });

    const btnCatIcon = document.getElementById('icon-btn-cat');
    const groupInc = document.getElementById('icon-group-inc');
    const groupExp = document.getElementById('icon-group-exp');
    if (btnCatIcon) btnCatIcon.innerHTML = icons.get('plus', { size: 18 });
    if (groupInc) groupInc.innerHTML = icons.get('trendingUp', { size: 18 });
    if (groupExp) groupExp.innerHTML = icons.get('trendingDown', { size: 18 });

    const modalInc = document.getElementById('icon-modal-income');
    const modalExp = document.getElementById('icon-modal-expense');
    const exportBtn = document.getElementById('icon-export-btn');
    const importBtn = document.getElementById('icon-import-btn');
    if (modalInc) modalInc.innerHTML = icons.get('plus', { size: 16 });
    if (modalExp) modalExp.innerHTML = icons.get('minus', { size: 16 });
    if (exportBtn) exportBtn.innerHTML = icons.get('download', { size: 18 });
    if (importBtn) importBtn.innerHTML = icons.get('upload', { size: 18 });

    if (iconLoadMore) iconLoadMore.innerHTML = icons.get('chevronDown', { size: 16 });
    if (iconPagePrev) iconPagePrev.innerHTML = icons.get('chevronLeft', { size: 14 });
    if (iconPageNext) iconPageNext.innerHTML = icons.get('chevronRight', { size: 14 });

    if (confirmModalIcon) confirmModalIcon.innerHTML = icons.get('trash2', { size: 28 });

    // Wisdom View Icons
    const iconQuote = document.getElementById('icon-quote-sparkles');
    const iconPillar1 = document.getElementById('icon-pillar-1');
    const iconPillar2 = document.getElementById('icon-pillar-2');
    const iconPillar3 = document.getElementById('icon-pillar-3');
    const iconPillar4 = document.getElementById('icon-pillar-4');
    const iconFlowsHeart = document.getElementById('icon-flows-heart');

    if (iconQuote) iconQuote.innerHTML = icons.get('sparkles', { size: 24 });
    if (iconPillar1) iconPillar1.innerHTML = icons.get('coffee', { size: 18 });
    if (iconPillar2) iconPillar2.innerHTML = icons.get('shield', { size: 18 });
    if (iconPillar3) iconPillar3.innerHTML = icons.get('clock', { size: 18 });
    if (iconPillar4) iconPillar4.innerHTML = icons.get('alertCircle', { size: 18 });
    if (iconFlowsHeart) iconFlowsHeart.innerHTML = icons.get('heart', { size: 20 });
  }

  // ==========================================
  // SANITASI KEAMANAN (ANTI-XSS)
  // ==========================================
  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ==========================================
  // FORMAT UTILITIES
  // ==========================================
  function formatMoney(num) {
    if (i18n) return i18n.formatCurrency(num);
    const n = Math.abs(Number(num)) || 0;
    return 'Rp ' + new Intl.NumberFormat('id-ID').format(n);
  }

  function formatDate(dateStr) {
    if (i18n) return i18n.formatDate(dateStr);
    return dateStr;
  }

  function showToast(message, iconName = 'check', duration = 3200) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    const iconSvg = icons ? icons.get(iconName, { size: 18 }) : '';
    toast.innerHTML = `<span>${iconSvg}</span> <span>${escapeHTML(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // ==========================================
  // MULTIBILINGUAL I18N SYSTEM
  // ==========================================
  function applyLanguage(lang) {
    if (!i18n) return;
    i18n.setLanguage(lang);

    // Update active button state
    langBtns.forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // 1. Update text nodes with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      el.textContent = i18n.t(key);
    });

    // 2. Update placeholders with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      el.setAttribute('placeholder', i18n.t(key));
    });

    // 3. Update titles with data-i18n-title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      el.setAttribute('title', i18n.t(key));
    });

    // 4. Update currency symbol in hero
    if (heroCurrencySymbolEl) {
      heroCurrencySymbolEl.textContent = i18n.translations[lang].currency_symbol || 'Rp';
    }

    // Refresh UI components with new language
    populateCategoryDropdowns();
    updatePrintHeaders();
    refreshAll();
  }

  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      applyLanguage(lang);
    });
  });

  // ==========================================
  // CUSTOM CONFIRMATION MODAL
  // ==========================================
  function openConfirmModal(titleKey, descKey, onConfirm) {
    confirmModalTitle.textContent = i18n ? i18n.t(titleKey) : titleKey;
    confirmModalDesc.textContent = i18n ? i18n.t(descKey) : descKey;
    confirmCallback = onConfirm;
    openModal(modalConfirm);
  }

  btnConfirmCancel.addEventListener('click', () => {
    closeModal(modalConfirm);
    confirmCallback = null;
  });

  btnConfirmProceed.addEventListener('click', () => {
    if (typeof confirmCallback === 'function') {
      confirmCallback();
    }
    closeModal(modalConfirm);
    confirmCallback = null;
  });

  // ==========================================
  // TAB ROUTING
  // ==========================================
  function switchTab(targetTabId) {
    navItems.forEach(item => {
      const isTarget = item.getAttribute('data-target') === targetTabId;
      if (isTarget) {
        item.classList.add('active');
        item.setAttribute('aria-selected', 'true');
      } else {
        item.classList.remove('active');
        item.setAttribute('aria-selected', 'false');
      }
    });

    tabViews.forEach(view => {
      if (view.id === targetTabId) {
        view.classList.add('active');
      } else {
        view.classList.remove('active');
      }
    });

    if (targetTabId === 'view-reports') {
      setTimeout(() => renderCharts(), 60);
    }
  }

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const target = item.getAttribute('data-target');
      switchTab(target);
    });
  });

  // ==========================================
  // HERO WALLET RENDERING
  // ==========================================
  function renderHeroSummary() {
    const summary = store.getSummary();
    const walletCard = document.getElementById('hero-wallet-card');
    const deficitBadge = document.getElementById('hero-deficit-badge');
    const isDeficit = summary.balance < 0;

    if (deficitBadge) {
      deficitBadge.style.display = isDeficit ? 'inline-block' : 'none';
    }
    if (walletCard) {
      if (isDeficit) walletCard.classList.add('is-deficit');
      else walletCard.classList.remove('is-deficit');
    }

    const rawVal = new Intl.NumberFormat(
      i18n && i18n.currentLang === 'ja' ? 'ja-JP' : (i18n && i18n.currentLang === 'en' ? 'en-US' : 'id-ID')
    ).format(Math.abs(summary.balance));

    heroBalanceEl.textContent = (isDeficit ? '- ' : '') + rawVal;
    heroIncomeEl.textContent = '+ ' + formatMoney(summary.monthlyIncome);
    heroExpenseEl.textContent = '- ' + formatMoney(summary.monthlyExpense);
  }

  // ==========================================
  // TRANSACTION LIST RENDERING
  // ==========================================
  function renderTransactions() {
    const filterType = txFilterType.value;
    const filterCat = txFilterCategory.value;
    const search = txSearchInput.value;

    const txs = store.getTransactions(filterType, search, filterCat);
    const countSuffix = i18n ? i18n.t('tx_count_suffix') : 'Transaksi';
    txCountBadge.textContent = `${txs.length} ${countSuffix}`;

    if (txs.length === 0) {
      if (txLoadMoreWrap) txLoadMoreWrap.style.display = 'none';

      const emptyTitle = i18n ? i18n.t('empty_tx_title') : 'Belum Ada Transaksi';
      const emptyDesc = i18n ? i18n.t('empty_tx_desc') : 'Yuk catat transaksi pertamamu!';
      const btnText = i18n ? i18n.t('btn_record_income') : 'Catat Uang Masuk';

      txListContainer.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon-wrap">
            ${icons.get('wallet', { size: 32 })}
          </div>
          <h4 class="empty-title">${escapeHTML(emptyTitle)}</h4>
          <p class="empty-desc">${escapeHTML(emptyDesc)}</p>
          <button class="btn btn-primary" id="btn-empty-add-income">
            ${icons.get('plus', { size: 16 })} ${escapeHTML(btnText)}
          </button>
        </div>
      `;

      const emptyBtn = document.getElementById('btn-empty-add-income');
      if (emptyBtn) {
        emptyBtn.addEventListener('click', () => openTransactionModal('income'));
      }
      return;
    }

    // Progressive disclosure: batasi tampilan awal sesuai txDisplayLimit
    const visibleTxs = txs.slice(0, txDisplayLimit);
    const delLabel = i18n ? i18n.t('btn_delete') : 'Hapus';

    txListContainer.innerHTML = visibleTxs.map(tx => {
      const cat = store.getCategoryById(tx.categoryId);
      const isIncome = tx.type === 'income';
      const sign = isIncome ? '+' : '-';
      const badgeClass = isIncome ? 'income' : 'expense';
      const iconKey = cat.icon || (isIncome ? 'banknote' : 'receipt');

      return `
        <div class="tx-card">
          <div class="tx-left">
            <div class="tx-badge-icon ${badgeClass}">
              ${icons.get(iconKey, { size: 20 })}
            </div>
            <div class="tx-info">
              <span class="tx-title">${escapeHTML(tx.note) || escapeHTML(cat.name)}</span>
              <div class="tx-meta">
                <span>${icons.get('calendar', { size: 12 })} ${formatDate(tx.date)} ${tx.time ? '• ' + escapeHTML(tx.time) : ''}</span>
                <span class="tx-category-tag">
                  ${icons.get('tag', { size: 10 })} ${escapeHTML(cat.name)}
                </span>
              </div>
            </div>
          </div>
          <div class="tx-right">
            <span class="tx-amount ${badgeClass}">
              ${sign} ${formatMoney(tx.amount)}
            </span>
            <button class="tx-delete-btn" data-id="${escapeHTML(tx.id)}" title="${escapeHTML(delLabel)}">
              ${icons.get('trash2', { size: 14 })} ${escapeHTML(delLabel)}
            </button>
          </div>
        </div>
      `;
    }).join('');

    // Toggle tombol "Muat Lebih Banyak" jika ada transaksi tersisa
    if (txLoadMoreWrap) {
      if (txs.length > txDisplayLimit) {
        txLoadMoreWrap.style.display = 'flex';
        const remaining = txs.length - txDisplayLimit;
        if (textLoadMore) {
          const tpl = i18n ? i18n.t('btn_load_more_remaining') : 'Tampilkan Lebih Banyak ({count} tersisa)';
          textLoadMore.textContent = tpl.replace('{count}', remaining);
        }
      } else {
        txLoadMoreWrap.style.display = 'none';
      }
    }

    // Attach delete listeners
    txListContainer.querySelectorAll('.tx-delete-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openConfirmModal(
          'confirm_delete_tx_title',
          'confirm_delete_tx_desc',
          () => {
            store.deleteTransaction(id);
            showToast(i18n ? i18n.t('toast_tx_deleted') : 'Catatan transaksi telah dihapus.', 'trash2');
            refreshAll();
          }
        );
      });
    });
  }

  // ==========================================
  // REPORTS & CHARTS RENDERING
  // ==========================================
  function renderCharts() {
    const summary = store.getSummary();
    const trendData = store.getLast7DaysTrend();

    chartEngine.renderTrendBarChart('canvas-trend', trendData);
    chartEngine.renderExpenseDonutChart(
      'canvas-donut',
      'donut-legend-container',
      summary.expenseByCategory,
      summary.totalExpense,
      store.getCategories('expense')
    );
  }

  function renderReportTable(forPrint = false) {
    const allTxs = store.getTransactions('all', '', 'all');
    const summary = store.getSummary();

    if (allTxs.length === 0) {
      const emptyMsg = i18n ? i18n.t('table_empty') : 'Belum ada catatan keuangan yang tersimpan.';
      reportTableBody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">
            ${escapeHTML(emptyMsg)}
          </td>
        </tr>
      `;
      if (reportPaginationBar) reportPaginationBar.style.display = 'none';
    } else {
      let displayTxs = allTxs;
      const totalPages = Math.max(1, Math.ceil(allTxs.length / REPORT_PAGE_SIZE));

      if (!forPrint) {
        if (reportCurrentPage > totalPages) reportCurrentPage = totalPages;
        if (reportCurrentPage < 1) reportCurrentPage = 1;

        const startIndex = (reportCurrentPage - 1) * REPORT_PAGE_SIZE;
        displayTxs = allTxs.slice(startIndex, startIndex + REPORT_PAGE_SIZE);

        if (reportPaginationBar) {
          reportPaginationBar.style.display = 'flex';
          const infoTpl = i18n ? i18n.t('pagination_page_info') : 'Halaman {page} dari {total} ({count} Transaksi)';
          if (reportPaginationInfo) {
            reportPaginationInfo.textContent = infoTpl
              .replace('{page}', reportCurrentPage)
              .replace('{total}', totalPages)
              .replace('{count}', allTxs.length);
          }

          if (btnReportPrev) btnReportPrev.disabled = (reportCurrentPage <= 1);
          if (btnReportNext) btnReportNext.disabled = (reportCurrentPage >= totalPages);

          // Render angka halaman jika lebih dari 1 halaman
          if (reportPageNumbers) {
            if (totalPages > 1) {
              let pagesHtml = '';
              for (let p = 1; p <= totalPages; p++) {
                pagesHtml += `<button class="page-num-btn ${p === reportCurrentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
              }
              reportPageNumbers.innerHTML = pagesHtml;

              reportPageNumbers.querySelectorAll('.page-num-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                  const targetP = Number(e.currentTarget.getAttribute('data-page'));
                  if (targetP !== reportCurrentPage) {
                    reportCurrentPage = targetP;
                    renderReportTable();
                  }
                });
              });
            } else {
              reportPageNumbers.innerHTML = '';
            }
          }
        }
      } else {
        if (reportPaginationBar) reportPaginationBar.style.display = 'none';
      }

      reportTableBody.innerHTML = displayTxs.map(tx => {
        const cat = store.getCategoryById(tx.categoryId);
        const isInc = tx.type === 'income';
        return `
          <tr>
            <td>${formatDate(tx.date)}</td>
            <td><strong>${escapeHTML(cat.name)}</strong></td>
            <td>${escapeHTML(tx.note) || '-'}</td>
            <td style="text-align: right; color: var(--income); font-weight: 600;">
              ${isInc ? formatMoney(tx.amount) : '-'}
            </td>
            <td style="text-align: right; color: var(--expense); font-weight: 600;">
              ${!isInc ? formatMoney(tx.amount) : '-'}
            </td>
          </tr>
        `;
      }).join('');
    }

    tableTotalIncome.textContent = formatMoney(summary.totalIncome);
    tableTotalExpense.textContent = formatMoney(summary.totalExpense);
    tableTotalBalance.textContent = formatMoney(summary.balance);
  }

  // ==========================================
  // NOTES (MEMO & KASBON) RENDERING
  // ==========================================
  function renderNotes() {
    const notes = store.getNotes();

    if (notes.length === 0) {
      const emptyTitle = i18n ? i18n.t('empty_notes_title') : 'Buku Catatan Masih Kosong';
      const emptyDesc = i18n ? i18n.t('empty_notes_desc') : 'Catat kasbon atau pengingat penting.';
      const btnText = i18n ? i18n.t('btn_write_note') : 'Tulis Catatan';

      notesGridContainer.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon-wrap">
            ${icons.get('fileText', { size: 32 })}
          </div>
          <h4 class="empty-title">${escapeHTML(emptyTitle)}</h4>
          <p class="empty-desc">${escapeHTML(emptyDesc)}</p>
          <button class="btn btn-secondary" id="btn-empty-add-note">
            ${icons.get('pencil', { size: 16 })} ${escapeHTML(btnText)}
          </button>
        </div>
      `;
      const emptyNoteBtn = document.getElementById('btn-empty-add-note');
      if (emptyNoteBtn) {
        emptyNoteBtn.addEventListener('click', () => openNoteModal());
      }
      return;
    }

    const pinLabel = i18n ? i18n.t('btn_pin') : 'Pin';
    const unpinLabel = i18n ? i18n.t('btn_unpin') : 'Lepas';
    const editLabel = i18n ? i18n.t('btn_edit') : 'Ubah';

    notesGridContainer.innerHTML = notes.map(note => {
      const tagLower = (note.tag || '').toLowerCase();
      let badgeClass = 'badge-umum';
      let cardBorder = '';
      let displayTag = note.tag;

      if (tagLower.includes('kasbon') || tagLower.includes('receivable') || tagLower.includes('ツケ') || tagLower.includes('売掛')) {
        badgeClass = 'badge-kasbon';
        cardBorder = 'kasbon';
        displayTag = i18n ? i18n.t('badge_kasbon') : note.tag;
      } else if (tagLower.includes('belanja') || tagLower.includes('procurement') || tagLower.includes('仕入') || tagLower.includes('買出')) {
        badgeClass = 'badge-belanja';
        cardBorder = 'belanja';
        displayTag = i18n ? i18n.t('badge_belanja') : note.tag;
      } else if (tagLower.includes('penting') || tagLower.includes('priority') || tagLower.includes('重要')) {
        badgeClass = 'badge-penting';
        displayTag = i18n ? i18n.t('badge_penting') : note.tag;
      }

      const dateStr = formatDate(new Date(note.updatedAt).toISOString().split('T')[0]);

      return `
        <div class="note-card ${cardBorder}">
          <div>
            <div class="note-header">
              <h3 class="note-title">
                ${note.isPinned ? icons.get('pin', { size: 16, className: 'pinned' }) : ''}
                ${escapeHTML(note.title)}
              </h3>
              <span class="note-badge ${badgeClass}">${escapeHTML(displayTag)}</span>
            </div>
            <p class="note-content">${escapeHTML(note.content)}</p>
          </div>
          <div class="note-footer">
            <span>${icons.get('clock', { size: 12 })} ${dateStr}</span>
            <div style="display: flex; align-items: center; gap: 4px;">
              <button class="tx-delete-btn note-edit-btn" data-id="${escapeHTML(note.id)}" title="${escapeHTML(editLabel)}">
                ${icons.get('pencil', { size: 13 })} ${escapeHTML(editLabel)}
              </button>
              <button class="tx-delete-btn note-pin-btn" data-id="${escapeHTML(note.id)}" title="${note.isPinned ? unpinLabel : pinLabel}">
                ${note.isPinned ? icons.get('x', { size: 14 }) + ' ' + unpinLabel : icons.get('pin', { size: 14 }) + ' ' + pinLabel}
              </button>
              <button class="tx-delete-btn note-del-btn" data-id="${escapeHTML(note.id)}" title="Hapus">
                ${icons.get('trash2', { size: 14 })}
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');

    notesGridContainer.querySelectorAll('.note-edit-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openNoteModal(id);
      });
    });

    notesGridContainer.querySelectorAll('.note-pin-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const note = store.notes.find(n => n.id === id);
        if (note) {
          store.updateNote(id, { isPinned: !note.isPinned });
          renderNotes();
        }
      });
    });

    notesGridContainer.querySelectorAll('.note-del-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openConfirmModal(
          'confirm_delete_note_title',
          'confirm_delete_note_desc',
          () => {
            store.deleteNote(id);
            showToast(i18n ? i18n.t('toast_note_deleted') : 'Catatan telah dihapus.', 'trash2');
            renderNotes();
          }
        );
      });
    });
  }

  // ==========================================
  // CATEGORIES RENDERING & POPULATION
  // ==========================================
  function renderCategories() {
    const incCats = store.getCategories('income');
    const expCats = store.getCategories('expense');
    const defaultBadgeText = i18n ? i18n.t('category_default_badge') : 'Bawaan';

    incomeCatList.innerHTML = incCats.map(c => `
      <div class="category-pill">
        <div class="cat-left">
          <div class="cat-icon-badge" style="color: ${c.color};">
            ${icons.get(c.icon || 'tag', { size: 18 })}
          </div>
          <span>${escapeHTML(c.name)}</span>
        </div>
        ${!c.isDefault ? `<button class="tx-delete-btn cat-del-btn" data-id="${escapeHTML(c.id)}">${icons.get('trash2', { size: 14 })}</button>` : `<span class="cat-default-badge">${escapeHTML(defaultBadgeText)}</span>`}
      </div>
    `).join('');

    expenseCatList.innerHTML = expCats.map(c => `
      <div class="category-pill">
        <div class="cat-left">
          <div class="cat-icon-badge" style="color: ${c.color};">
            ${icons.get(c.icon || 'tag', { size: 18 })}
          </div>
          <span>${escapeHTML(c.name)}</span>
        </div>
        ${!c.isDefault ? `<button class="tx-delete-btn cat-del-btn" data-id="${escapeHTML(c.id)}">${icons.get('trash2', { size: 14 })}</button>` : `<span class="cat-default-badge">${escapeHTML(defaultBadgeText)}</span>`}
      </div>
    `).join('');

    document.querySelectorAll('.cat-del-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openConfirmModal(
          'confirm_delete_cat_title',
          'confirm_delete_cat_desc',
          () => {
            store.deleteCategory(id);
            showToast(i18n ? i18n.t('toast_cat_deleted') : 'Kategori berhasil dihapus.', 'trash2');
            populateCategoryDropdowns();
            refreshAll();
          }
        );
      });
    });
  }

  function populateCategoryDropdowns() {
    const allCats = store.getCategories('all');
    const allLabel = i18n ? i18n.t('filter_all_cats') : 'Semua Kategori';
    const incLabel = i18n ? i18n.t('filter_income') : 'Masuk';
    const expLabel = i18n ? i18n.t('filter_expense') : 'Keluar';

    txFilterCategory.innerHTML = `<option value="all">${escapeHTML(allLabel)}</option>` +
      allCats.map(c => `<option value="${escapeHTML(c.id)}">${escapeHTML(c.name)} (${c.type === 'income' ? incLabel : expLabel})</option>`).join('');

    updateModalCategoryOptions();
  }

  function updateModalCategoryOptions() {
    const currentType = txTypeVal.value;
    const cats = store.getCategories(currentType);
    txCategorySelect.innerHTML = cats.map(c => `
      <option value="${escapeHTML(c.id)}">${escapeHTML(c.name)}</option>
    `).join('');
  }

  // ==========================================
  // MODALS MANAGEMENT
  // ==========================================
  function openModal(modalEl) {
    if (modalEl) {
      modalEl.classList.add('open');
      document.body.classList.add('modal-open');
    }
  }

  function closeModal(modalEl) {
    if (modalEl) {
      modalEl.classList.remove('open');
      const openModals = document.querySelectorAll('.modal-overlay.open');
      if (openModals.length === 0) {
        document.body.classList.remove('modal-open');
      }
    }
  }

  // Global Escape key listener to close modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModals = document.querySelectorAll('.modal-overlay.open');
      openModals.forEach(m => closeModal(m));
    }
  });

  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.getAttribute('data-close');
      closeModal(document.getElementById(modalId));
    });
  });

  [modalTx, modalNote, modalCategory, modalBackup, modalConfirm].forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal(modal);
    });
  });

  // 1. Open Transaction Modal
  function openTransactionModal(type = 'income') {
    setTransactionType(type);
    txAmountInput.value = '';
    txNoteInput.value = '';
    
    const now = new Date();
    const localYear = now.getFullYear();
    const localMonth = String(now.getMonth() + 1).padStart(2, '0');
    const localDay = String(now.getDate()).padStart(2, '0');
    const localHours = String(now.getHours()).padStart(2, '0');
    const localMins = String(now.getMinutes()).padStart(2, '0');

    txDateInput.value = `${localYear}-${localMonth}-${localDay}`;
    txTimeInput.value = `${localHours}:${localMins}`;

    const titleEl = document.getElementById('modal-tx-title');
    if (titleEl && i18n) {
      titleEl.textContent = type === 'income' ? i18n.t('modal_tx_income_title') : i18n.t('modal_tx_expense_title');
    }
    openModal(modalTx);
    setTimeout(() => txAmountInput.focus(), 150);
  }

  function setTransactionType(type) {
    txTypeVal.value = type;
    if (type === 'income') {
      btnTypeIncome.className = 'type-btn active income';
      btnTypeExpense.className = 'type-btn';
    } else {
      btnTypeIncome.className = 'type-btn';
      btnTypeExpense.className = 'type-btn active expense';
    }
    updateModalCategoryOptions();
  }

  btnTypeIncome.addEventListener('click', () => setTransactionType('income'));
  btnTypeExpense.addEventListener('click', () => setTransactionType('expense'));

  document.getElementById('btn-quick-income').addEventListener('click', () => openTransactionModal('income'));
  document.getElementById('btn-quick-expense').addEventListener('click', () => openTransactionModal('expense'));

  txAmountInput.addEventListener('input', (e) => {
    const input = e.target;
    const rawVal = input.value.replace(/\D/g, '');
    if (!rawVal) {
      input.value = '';
      return;
    }
    const formatted = new Intl.NumberFormat(
      i18n && i18n.currentLang === 'ja' ? 'ja-JP' : (i18n && i18n.currentLang === 'en' ? 'en-US' : 'id-ID')
    ).format(rawVal);

    if (input.value !== formatted) {
      input.value = formatted;
    }
  });

  formTx.addEventListener('submit', (e) => {
    e.preventDefault();
    const rawAmount = txAmountInput.value.replace(/\D/g, '');
    const amount = Number(rawAmount);

    if (!amount || amount <= 0) {
      showToast(i18n ? i18n.t('toast_invalid_amount') : 'Mohon masukkan nominal uang yang valid.', 'alertCircle');
      return;
    }

    const type = txTypeVal.value;
    store.addTransaction({
      type,
      amount,
      categoryId: txCategorySelect.value,
      date: txDateInput.value,
      time: txTimeInput.value,
      note: txNoteInput.value
    });

    closeModal(modalTx);
    showToast(i18n ? i18n.t('toast_tx_added') : 'Catatan kas berhasil disimpan!', 'check');
    refreshAll();
  });

  // 2. Open Note Modal (Create & Edit)
  function openNoteModal(editId = null) {
    const titleEl = document.getElementById('modal-note-title');
    const submitBtnSpan = formNote.querySelector('button[type="submit"] span');
    const hiddenId = document.getElementById('note-edit-id');

    if (editId) {
      const note = store.notes.find(n => n.id === editId);
      if (!note) return;
      hiddenId.value = note.id;
      noteTitleInput.value = note.title;
      noteTagSelect.value = note.tag || 'Umum';
      noteContentInput.value = note.content;
      notePinCheckbox.checked = !!note.isPinned;
      if (titleEl && i18n) titleEl.textContent = i18n.t('modal_note_edit_title');
      if (submitBtnSpan) submitBtnSpan.textContent = i18n ? i18n.t('btn_save_note') : 'Perbarui Catatan';
    } else {
      hiddenId.value = '';
      formNote.reset();
      if (titleEl && i18n) titleEl.textContent = i18n.t('modal_note_title');
      if (submitBtnSpan) submitBtnSpan.textContent = i18n ? i18n.t('btn_save_note') : 'Simpan ke Buku Catatan';
    }

    openModal(modalNote);
    setTimeout(() => noteTitleInput.focus(), 150);
  }

  document.getElementById('btn-add-note').addEventListener('click', () => openNoteModal());

  formNote.addEventListener('submit', (e) => {
    e.preventDefault();
    const editId = document.getElementById('note-edit-id').value;

    if (editId) {
      store.updateNote(editId, {
        title: noteTitleInput.value,
        tag: noteTagSelect.value,
        content: noteContentInput.value,
        isPinned: notePinCheckbox.checked
      });
      showToast(i18n ? i18n.t('toast_note_updated') : 'Catatan berhasil diperbarui!', 'check');
    } else {
      store.addNote({
        title: noteTitleInput.value,
        tag: noteTagSelect.value,
        content: noteContentInput.value,
        isPinned: notePinCheckbox.checked
      });
      showToast(i18n ? i18n.t('toast_note_added') : 'Catatan berhasil ditambahkan ke buku!', 'check');
    }

    closeModal(modalNote);
    renderNotes();
  });

  // 3. Open Category Modal
  document.getElementById('btn-add-category').addEventListener('click', () => {
    formCategory.reset();
    openModal(modalCategory);
  });

  formCategory.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = catNameInput.value.trim();
    if (!name) return;

    store.addCategory({
      name,
      type: catTypeSelect.value,
      icon: catIconSelect.value || (catTypeSelect.value === 'income' ? 'banknote' : 'receipt'),
      color: catColorInput.value
    });

    closeModal(modalCategory);
    showToast(i18n ? i18n.t('toast_cat_added') : `Kategori "${name}" berhasil dibuat!`, 'tag');
    populateCategoryDropdowns();
    renderCategories();
  });

  // 4. Backup & Profile Modal
  document.getElementById('btn-backup-modal').addEventListener('click', () => {
    profileBizName.value = store.profile.businessName || '';
    profileOwnerName.value = store.profile.ownerName || '';
    profilePhone.value = store.profile.phone || '';
    openModal(modalBackup);
  });

  document.getElementById('btn-save-profile').addEventListener('click', () => {
    store.profile.businessName = profileBizName.value.trim() || 'Usaha Dagang Berkah';
    store.profile.ownerName = profileOwnerName.value.trim() || 'Juragan Mandiri';
    store.profile.phone = profilePhone.value.trim() || '';
    store.saveProfile();
    updatePrintHeaders();
    showToast(i18n ? i18n.t('toast_profile_saved') : 'Profil usaha berhasil disimpan.', 'check');
  });

  document.getElementById('btn-export-data').addEventListener('click', () => {
    const jsonStr = store.exportDataJSON();
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const dateStr = new Date().toISOString().split('T')[0];
    a.href = url;
    a.download = `BukuKas_Vault_${dateStr}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast(i18n ? i18n.t('toast_backup_exported') : 'File cadangan berhasil diunduh!', 'download');
  });

  document.getElementById('file-import-input').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const res = store.importDataJSON(event.target.result);
      if (res.success) {
        showToast(i18n ? i18n.t('toast_backup_imported') : `Berhasil memulihkan ${res.count} transaksi!`, 'check');
        closeModal(modalBackup);
        refreshAll();
      } else {
        showToast('Gagal memulihkan: ' + res.message, 'alertCircle');
      }
      // Reset input value so re-importing the same file triggers change event
      e.target.value = '';
    };
    reader.readAsText(file);
  });

  // ==========================================
  // PRINTABLE PDF REPORT
  // ==========================================
  function updatePrintHeaders() {
    const bizEl = document.getElementById('print-biz-name');
    const ownerEl = document.getElementById('print-biz-owner');
    const phoneEl = document.getElementById('print-biz-phone');
    const signOwnerEl = document.getElementById('print-sign-owner');
    const printDateEl = document.getElementById('print-date');

    if (bizEl) bizEl.textContent = store.profile.businessName || 'Usaha Dagang Berkah';
    if (ownerEl) ownerEl.textContent = store.profile.ownerName || 'Juragan Mandiri';
    if (phoneEl) phoneEl.textContent = store.profile.phone || '-';
    if (signOwnerEl) signOwnerEl.textContent = store.profile.ownerName || (i18n ? i18n.t('print_owner_default') : 'Juragan Mandiri');
    if (printDateEl) {
      const todayStr = new Date().toISOString().split('T')[0];
      printDateEl.textContent = formatDate(todayStr);
    }
  }

  function triggerPrintReport() {
    updatePrintHeaders();
    renderReportTable(true); // render all rows for print

    // Remember previous active tab
    const currentActiveItem = document.querySelector('.nav-item.active');
    const previousTabId = currentActiveItem ? currentActiveItem.getAttribute('data-target') : 'view-transactions';

    switchTab('view-reports');

    requestAnimationFrame(() => {
      setTimeout(() => {
        window.print();
        renderReportTable(false); // restore pagination after print
        if (previousTabId !== 'view-reports') {
          setTimeout(() => switchTab(previousTabId), 300);
        }
      }, 120);
    });
  }

  document.getElementById('btn-print-action').addEventListener('click', triggerPrintReport);
  document.getElementById('btn-header-print').addEventListener('click', triggerPrintReport);

  // Search & Filter event listeners (reset limit on query change)
  txSearchInput.addEventListener('input', () => {
    txDisplayLimit = 10;
    renderTransactions();
  });
  txFilterType.addEventListener('change', () => {
    txDisplayLimit = 10;
    renderTransactions();
  });
  txFilterCategory.addEventListener('change', () => {
    txDisplayLimit = 10;
    renderTransactions();
  });

  // Load More Button Listener
  if (btnLoadMoreTx) {
    btnLoadMoreTx.addEventListener('click', () => {
      txDisplayLimit += TX_PAGE_STEP;
      renderTransactions();
    });
  }

  // Report Table Pagination Listeners
  if (btnReportPrev) {
    btnReportPrev.addEventListener('click', () => {
      if (reportCurrentPage > 1) {
        reportCurrentPage--;
        renderReportTable();
      }
    });
  }

  if (btnReportNext) {
    btnReportNext.addEventListener('click', () => {
      const allTxs = store.getTransactions('all', '', 'all');
      const totalPages = Math.ceil(allTxs.length / REPORT_PAGE_SIZE);
      if (reportCurrentPage < totalPages) {
        reportCurrentPage++;
        renderReportTable();
      }
    });
  }

  // Native Print Event Hook
  window.addEventListener('beforeprint', () => renderReportTable(true));
  window.addEventListener('afterprint', () => renderReportTable(false));

  window.addEventListener('resize', () => {
    const reportsTab = document.getElementById('view-reports');
    if (reportsTab && reportsTab.classList.contains('active')) {
      renderCharts();
    }
  });

  // Master Refresh
  function refreshAll() {
    renderHeroSummary();
    renderTransactions();
    renderReportTable();
    renderNotes();
    renderCategories();
    renderCharts();
  }

  // First Run Boot
  injectStaticIcons();
  applyLanguage(i18n ? i18n.currentLang : 'id');
});
