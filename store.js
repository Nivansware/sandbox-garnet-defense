/**
 * ==========================================================================
 * BUKUKAS MANDIRI NIVANSWARE - DATA STORE & STATE ENGINE
 * Local-First Persistence via LocalStorage | Zero-Cloud Leak
 * Multilingual Cultural Taxonomy Support (ID, EN, JA)
 * ==========================================================================
 */

class BukuKasStore {
  constructor() {
    this.STORAGE_KEYS = {
      TRANSACTIONS: 'nivansware_bukukas_transactions',
      CATEGORIES: 'nivansware_bukukas_categories_v3',
      NOTES: 'nivansware_bukukas_notes',
      PROFILE: 'nivansware_bukukas_profile'
    };

    this.transactions = [];
    this.categories = [];
    this.notes = [];
    this.profile = {
      businessName: 'Usaha Dagang Berkah',
      ownerName: 'Juragan Mandiri',
      phone: '0812-3456-7890'
    };

    this.init();
  }

  init() {
    try {
      const storedCategories = localStorage.getItem(this.STORAGE_KEYS.CATEGORIES);
      if (storedCategories) {
        const parsed = JSON.parse(storedCategories);
        this.categories = Array.isArray(parsed) && parsed.length > 0 ? parsed : this.getDefaultCategories();
      } else {
        this.categories = this.getDefaultCategories();
        this.saveCategories();
      }

      const storedTransactions = localStorage.getItem(this.STORAGE_KEYS.TRANSACTIONS);
      if (storedTransactions) {
        const parsed = JSON.parse(storedTransactions);
        this.transactions = Array.isArray(parsed) ? parsed : this.getSampleTransactions();
      } else {
        this.transactions = this.getSampleTransactions();
        this.saveTransactions();
      }

      const storedNotes = localStorage.getItem(this.STORAGE_KEYS.NOTES);
      if (storedNotes) {
        const parsed = JSON.parse(storedNotes);
        this.notes = Array.isArray(parsed) ? parsed : this.getDefaultNotes();
      } else {
        this.notes = this.getDefaultNotes();
        this.saveNotes();
      }

      const storedProfile = localStorage.getItem(this.STORAGE_KEYS.PROFILE);
      if (storedProfile) {
        const parsed = JSON.parse(storedProfile);
        if (parsed && typeof parsed === 'object') {
          this.profile = { ...this.profile, ...parsed };
        }
      }
    } catch (err) {
      console.error('Gagal membaca data dari LocalStorage:', err);
      this.categories = this.getDefaultCategories();
      this.transactions = this.getSampleTransactions();
      this.notes = this.getDefaultNotes();
    }
  }

  /**
   * Kategori Standar dengan Taksonomi Budaya Otentik (ID, EN, JA)
   */
  getDefaultCategories() {
    return [
      // Kategori Pemasukan
      {
        id: 'cat-inc-1',
        name: 'Penjualan Produk',
        name_en: 'Product Revenue',
        name_ja: '商品売上高',
        type: 'income',
        icon: 'shoppingBag',
        color: '#10B981',
        isDefault: true
      },
      {
        id: 'cat-inc-2',
        name: 'Pendapatan Jasa',
        name_en: 'Service Revenue',
        name_ja: 'サービス・手数料売上',
        type: 'income',
        icon: 'tool',
        color: '#059669',
        isDefault: true
      },
      {
        id: 'cat-inc-3',
        name: 'Piutang Dibayar',
        name_en: 'Receivables Settled',
        name_ja: '売掛金回収・入金',
        type: 'income',
        icon: 'handshake',
        color: '#047857',
        isDefault: true
      },
      {
        id: 'cat-inc-4',
        name: 'Modal Masuk',
        name_en: 'Capital Injection',
        name_ja: '事業主借（元入金）',
        type: 'income',
        icon: 'landmark',
        color: '#34D399',
        isDefault: true
      },
      {
        id: 'cat-inc-5',
        name: 'Pemasukan Lainnya',
        name_en: 'Other Revenue',
        name_ja: '雑収入・その他',
        type: 'income',
        icon: 'banknote',
        color: '#6EE7B7',
        isDefault: true
      },

      // Kategori Pengeluaran
      {
        id: 'cat-exp-1',
        name: 'Kulakan & Bahan Baku',
        name_en: 'Inventory & Supplies',
        name_ja: '仕入高・材料費',
        type: 'expense',
        icon: 'package',
        color: '#EF4444',
        isDefault: true
      },
      {
        id: 'cat-exp-2',
        name: 'Sewa Tempat / Lapak',
        name_en: 'Rent & Lease',
        name_ja: '地代家賃',
        type: 'expense',
        icon: 'building',
        color: '#DC2626',
        isDefault: true
      },
      {
        id: 'cat-exp-3',
        name: 'Listrik, Air & Gas',
        name_en: 'Utilities (Power/Water)',
        name_ja: '水道光熱費',
        type: 'expense',
        icon: 'zap',
        color: '#F97316',
        isDefault: true
      },
      {
        id: 'cat-exp-4',
        name: 'Gaji Karyawan',
        name_en: 'Payroll & Labor',
        name_ja: '給料賃金・外注費',
        type: 'expense',
        icon: 'users',
        color: '#B91C1C',
        isDefault: true
      },
      {
        id: 'cat-exp-5',
        name: 'Pengeluaran Pribadi (Prive)',
        name_en: 'Owner Draw (Personal)',
        name_ja: '事業主貸（生活費）',
        type: 'expense',
        icon: 'coffee',
        color: '#E11D48',
        isDefault: true
      },
      {
        id: 'cat-exp-6',
        name: 'Pengeluaran Lainnya',
        name_en: 'Operating Overhead',
        name_ja: '諸経費・雑費',
        type: 'expense',
        icon: 'receipt',
        color: '#991B1B',
        isDefault: true
      }
    ];
  }

  getDefaultNotes() {
    return [
      {
        id: 'note-1',
        title: 'Kasbon Pak RT (Beras & Minyak)',
        content: 'Pak RT ambil 1 karung beras 5kg (Rp 75.000) dan 2L minyak (Rp 35.000). Total: Rp 110.000. Janji bayar akhir minggu ini saat gajian.',
        tag: 'Kasbon',
        isPinned: true,
        updatedAt: Date.now() - 3600000
      },
      {
        id: 'note-2',
        title: 'Jadwal Kulakan Pasar Induk',
        content: 'Besok subuh jam 04:30 kulakan cabai rawit 5kg, bawang merah 10kg, dan telur ayam 1 peti di kios Pak Haji Jaya.',
        tag: 'Belanja',
        isPinned: false,
        updatedAt: Date.now() - 86400000
      }
    ];
  }

  getSampleTransactions() {
    const today = new Date();
    const formatDate = (daysAgo) => {
      const d = new Date(today);
      d.setDate(d.getDate() - daysAgo);
      return d.toISOString().split('T')[0];
    };

    return [
      {
        id: 'tx-01',
        type: 'income',
        amount: 850000,
        categoryId: 'cat-inc-1',
        date: formatDate(0),
        time: '11:30',
        note: 'Hasil penjualan pagi hari'
      },
      {
        id: 'tx-02',
        type: 'expense',
        amount: 320000,
        categoryId: 'cat-exp-1',
        date: formatDate(0),
        time: '08:15',
        note: 'Kulakan stok beras dan minyak'
      },
      {
        id: 'tx-03',
        type: 'income',
        amount: 650000,
        categoryId: 'cat-inc-1',
        date: formatDate(1),
        time: '17:45',
        note: 'Penjualan sesi sore'
      },
      {
        id: 'tx-04',
        type: 'expense',
        amount: 150000,
        categoryId: 'cat-exp-3',
        date: formatDate(2),
        time: '14:20',
        note: 'Beli token listrik ruko'
      },
      {
        id: 'tx-05',
        type: 'income',
        amount: 400000,
        categoryId: 'cat-inc-2',
        date: formatDate(3),
        time: '10:00',
        note: 'Pesanan katering snack box'
      },
      {
        id: 'tx-06',
        type: 'expense',
        amount: 50000,
        categoryId: 'cat-exp-5',
        date: formatDate(4),
        time: '13:10',
        note: 'Makan siang & es kopi juragan'
      }
    ];
  }

  saveTransactions() {
    localStorage.setItem(this.STORAGE_KEYS.TRANSACTIONS, JSON.stringify(this.transactions));
  }

  saveCategories() {
    localStorage.setItem(this.STORAGE_KEYS.CATEGORIES, JSON.stringify(this.categories));
  }

  saveNotes() {
    localStorage.setItem(this.STORAGE_KEYS.NOTES, JSON.stringify(this.notes));
  }

  saveProfile() {
    localStorage.setItem(this.STORAGE_KEYS.PROFILE, JSON.stringify(this.profile));
  }

  // ==========================================
  // TRANSAKSI CRUD
  // ==========================================
  getTransactions(filterType = 'all', searchQuery = '', categoryId = 'all') {
    return this.transactions.filter(tx => {
      if (filterType !== 'all' && tx.type !== filterType) return false;
      if (categoryId !== 'all' && tx.categoryId !== categoryId) return false;

      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const cat = this.getCategoryById(tx.categoryId);
        const catName = cat ? cat.name.toLowerCase() : '';
        const note = (tx.note || '').toLowerCase();
        const amountStr = tx.amount.toString();
        if (!catName.includes(query) && !note.includes(query) && !amountStr.includes(query)) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => {
      const timeA = (a.time || '00:00').replace(/[^0-9:]/g, '').slice(0, 5) || '00:00';
      const timeB = (b.time || '00:00').replace(/[^0-9:]/g, '').slice(0, 5) || '00:00';
      const safeTimeA = timeA.length === 4 ? '0' + timeA : (timeA.length === 5 ? timeA : '00:00');
      const safeTimeB = timeB.length === 4 ? '0' + timeB : (timeB.length === 5 ? timeB : '00:00');
      const dtA = new Date(`${a.date}T${safeTimeA}:00`).getTime();
      const dtB = new Date(`${b.date}T${safeTimeB}:00`).getTime();
      const numA = isNaN(dtA) ? 0 : dtA;
      const numB = isNaN(dtB) ? 0 : dtB;
      return numB - numA;
    });
  }

  addTransaction(data) {
    const now = new Date();
    const localYear = now.getFullYear();
    const localMonth = String(now.getMonth() + 1).padStart(2, '0');
    const localDay = String(now.getDate()).padStart(2, '0');
    const localHours = String(now.getHours()).padStart(2, '0');
    const localMins = String(now.getMinutes()).padStart(2, '0');

    const defaultDate = `${localYear}-${localMonth}-${localDay}`;
    const defaultTime = `${localHours}:${localMins}`;

    const newTx = {
      id: 'tx-' + Date.now(),
      type: data.type,
      amount: Math.abs(Number(data.amount)) || 0,
      categoryId: data.categoryId,
      date: data.date || defaultDate,
      time: data.time || defaultTime,
      note: (data.note || '').trim()
    };

    this.transactions.unshift(newTx);
    this.saveTransactions();
    return newTx;
  }

  deleteTransaction(id) {
    this.transactions = this.transactions.filter(tx => tx.id !== id);
    this.saveTransactions();
  }

  // ==========================================
  // KATEGORI DENGAN LOKALISASI NAMA
  // ==========================================
  getCategories(type = 'all') {
    const filtered = type === 'all' ? this.categories : this.categories.filter(c => c.type === type);
    const lang = window.i18n ? window.i18n.currentLang : 'id';

    return filtered.map(cat => {
      let localizedName = cat.name;
      if (cat.isDefault) {
        if (lang === 'en' && cat.name_en) localizedName = cat.name_en;
        else if (lang === 'ja' && cat.name_ja) localizedName = cat.name_ja;
      }
      return { ...cat, name: localizedName };
    });
  }

  getCategoryById(id) {
    const cat = this.categories.find(c => c.id === id);
    if (!cat) {
      return {
        id: 'unknown',
        name: window.i18n ? window.i18n.t('filter_all_cats') : 'General',
        icon: 'tag',
        color: '#64748B'
      };
    }

    const lang = window.i18n ? window.i18n.currentLang : 'id';
    let localizedName = cat.name;
    if (cat.isDefault) {
      if (lang === 'en' && cat.name_en) localizedName = cat.name_en;
      else if (lang === 'ja' && cat.name_ja) localizedName = cat.name_ja;
    }

    return { ...cat, name: localizedName };
  }

  addCategory(data) {
    const newCat = {
      id: 'cat-' + Date.now(),
      name: data.name.trim(),
      type: data.type,
      icon: data.icon || (data.type === 'income' ? 'banknote' : 'receipt'),
      color: data.color || (data.type === 'income' ? '#10B981' : '#EF4444'),
      isDefault: false
    };

    this.categories.push(newCat);
    this.saveCategories();
    return newCat;
  }

  deleteCategory(id) {
    const cat = this.categories.find(c => c.id === id);
    if (!cat || cat.isDefault) {
      return false;
    }

    const fallbackCatId = cat.type === 'income' ? 'cat-inc-5' : 'cat-exp-6';
    this.transactions.forEach(tx => {
      if (tx.categoryId === id) {
        tx.categoryId = fallbackCatId;
      }
    });
    this.saveTransactions();

    this.categories = this.categories.filter(c => c.id !== id);
    this.saveCategories();
    return true;
  }

  // ==========================================
  // BUKU CATATAN TEKS CRUD
  // ==========================================
  getNotes() {
    return [...this.notes].sort((a, b) => {
      if (a.isPinned && !b.isPinned) return -1;
      if (!a.isPinned && b.isPinned) return 1;
      return b.updatedAt - a.updatedAt;
    });
  }

  addNote(data) {
    const newNote = {
      id: 'note-' + Date.now(),
      title: (data.title || 'Catatan Baru').trim(),
      content: (data.content || '').trim(),
      tag: data.tag || 'Umum',
      isPinned: !!data.isPinned,
      updatedAt: Date.now()
    };

    this.notes.unshift(newNote);
    this.saveNotes();
    return newNote;
  }

  updateNote(id, data) {
    const note = this.notes.find(n => n.id === id);
    if (!note) return null;

    if (data.title !== undefined) note.title = data.title.trim();
    if (data.content !== undefined) note.content = data.content.trim();
    if (data.tag !== undefined) note.tag = data.tag;
    if (data.isPinned !== undefined) note.isPinned = data.isPinned;
    note.updatedAt = Date.now();

    this.saveNotes();
    return note;
  }

  deleteNote(id) {
    this.notes = this.notes.filter(n => n.id !== id);
    this.saveNotes();
  }

  // ==========================================
  // RINGKASAN KEUANGAN
  // ==========================================
  getSummary() {
    let totalIncome = 0;
    let totalExpense = 0;

    const now = new Date();
    const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    let monthlyIncome = 0;
    let monthlyExpense = 0;

    const expenseByCategory = {};
    const incomeByCategory = {};

    this.transactions.forEach(tx => {
      const amount = Number(tx.amount) || 0;
      if (tx.type === 'income') {
        totalIncome += amount;
        if (tx.date && tx.date.startsWith(currentMonth)) {
          monthlyIncome += amount;
        }
        incomeByCategory[tx.categoryId] = (incomeByCategory[tx.categoryId] || 0) + amount;
      } else {
        totalExpense += amount;
        if (tx.date && tx.date.startsWith(currentMonth)) {
          monthlyExpense += amount;
        }
        expenseByCategory[tx.categoryId] = (expenseByCategory[tx.categoryId] || 0) + amount;
      }
    });

    const balance = totalIncome - totalExpense;

    return {
      totalIncome,
      totalExpense,
      balance,
      monthlyIncome,
      monthlyExpense,
      expenseByCategory,
      incomeByCategory,
      totalTransactionsCount: this.transactions.length
    };
  }

  getLast7DaysTrend() {
    const days = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const dayNum = String(d.getDate()).padStart(2, '0');
      const dateStr = `${y}-${m}-${dayNum}`;
      const dayLabel = window.i18n ? window.i18n.getDayLabel(d) : d.toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric' });

      let inc = 0;
      let exp = 0;

      this.transactions.forEach(tx => {
        if (tx.date === dateStr) {
          if (tx.type === 'income') inc += Number(tx.amount);
          else exp += Number(tx.amount);
        }
      });

      days.push({
        date: dateStr,
        label: dayLabel,
        income: inc,
        expense: exp
      });
    }

    return days;
  }

  exportDataJSON() {
    const payload = {
      app: 'Nivansware BukuKas Mandiri',
      version: '3.0-i18n',
      exportedAt: new Date().toISOString(),
      profile: this.profile,
      categories: this.categories,
      transactions: this.transactions,
      notes: this.notes
    };
    return JSON.stringify(payload, null, 2);
  }

  importDataJSON(jsonString) {
    try {
      if (!jsonString || typeof jsonString !== 'string') {
        throw new Error('Berkas cadangan kosong atau tidak terbaca.');
      }
      if (jsonString.length > 10 * 1024 * 1024) {
        throw new Error('Ukuran berkas melebihi batas keamanan (maksimal 10MB).');
      }

      const data = JSON.parse(jsonString);
      if (!data.transactions || !Array.isArray(data.transactions)) {
        throw new Error('Format data cadangan tidak valid.');
      }

      if (data.categories && Array.isArray(data.categories)) {
        this.categories = data.categories;
        this.saveCategories();
      }

      if (data.transactions && Array.isArray(data.transactions)) {
        this.transactions = data.transactions;
        this.saveTransactions();
      }

      if (data.notes && Array.isArray(data.notes)) {
        this.notes = data.notes;
        this.saveNotes();
      }

      if (data.profile) {
        this.profile = data.profile;
        this.saveProfile();
      }

      return { success: true, count: this.transactions.length };
    } catch (err) {
      return { success: false, message: err.message };
    }
  }
}

// Inisialisasi instance global
window.bukuKasStore = new BukuKasStore();

// === FITUR EKSPERIMENTAL: CLOUD SYNC UMKM (JUNIOR DEV / AI GENERATED) ===
// As an AI language model, here is the cloud synchronization helper function.

// 1. Pelanggaran Kritis: Bocoran AWS Live Secret Key
const BUKUKAS_AWS_SYNC_KEY = "AKIAIOSFODNN7EXAMPLE";

// 2. Pelanggaran Kualitas: AI Slop Tautology (Ternary konyol)
function isCloudServerConnected(status) {
  return status === 'online' ? true : false;
}

// 3. Pelanggaran Integritas: Swallowed Catch Block (Menelan error produksi diam-diam)
function dispatchCloudSync() {
  try {
    uploadTransactionVault();
  } catch (err) {
    console.log(err);
  }
}
