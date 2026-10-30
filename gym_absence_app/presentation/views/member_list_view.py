"""
View Data Member & Panel Admin (Rule 3, 6, 7, 8)
- Tabel Member: Nomor ID, Nama, Gender, Alamat, No HP, Paket, Tanggal Daftar, Status (Active/Non-Active).
- Fitur Pencarian: Berdasarkan Nomor ID dan Nama Member.
- Fitur Admin: Perpanjang masa aktif paket member yang kedaluwarsa.
- Fitur Admin: Hapus member yang SUDAH TIDAK AKTIF (dengan proteksi data).
"""
import customtkinter as ctk
from tkinter import ttk
from typing import List, Optional
from application.services import GymService
from domain.entities import Member
from domain.exceptions import GymAppException
from presentation.theme import GymTheme
from presentation.dialogs import MessageDialog, ConfirmDialog, MemberCalendarDialog


class MemberListView(ctk.CTkFrame):
    """Tabel Data Member & Kontrol Administrasi."""

    def __init__(self, parent, gym_service: GymService):
        super().__init__(parent, fg_color="transparent")
        self.gym_service = gym_service
        self.selected_member_id: Optional[str] = None
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Title
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(10, 15))

        ctk.CTkLabel(
            header,
            text="DATA MEMBER & PANEL ADMIN",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Kelola data member, pencarian instan, perpanjangan paket, dan pembersihan member non-aktif.",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        ).pack(anchor="w", pady=(2, 0))

        # Top Bar: Search Bar (Rule 8) & Refresh
        search_bar = ctk.CTkFrame(self, fg_color=GymTheme.BG_CARD, corner_radius=8)
        search_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=2)

        ctk.CTkLabel(
            search_bar,
            text="🔍 Cari Member:",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.SECONDARY
        ).pack(side="left", padx=(15, 10), pady=10)

        self.entry_search = ctk.CTkEntry(
            search_bar,
            placeholder_text="Ketik Nomor ID atau Nama Member...",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.TEXT_PRIMARY,
            height=36,
            width=300,
            corner_radius=6
        )
        self.entry_search.pack(side="left", padx=5, pady=10)
        self.entry_search.bind("<KeyRelease>", lambda event: self._on_search_change())

        btn_search = ctk.CTkButton(
            search_bar,
            text="Cari",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.SECONDARY,
            hover_color=GymTheme.SECONDARY_HOVER,
            text_color=GymTheme.TEXT_DARK,
            width=80,
            height=36,
            corner_radius=6,
            command=self._on_search_change
        )
        btn_search.pack(side="left", padx=5, pady=10)

        btn_reset = ctk.CTkButton(
            search_bar,
            text="Reset",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_MAIN,
            hover_color="#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            width=80,
            height=36,
            corner_radius=6,
            command=self._reset_search
        )
        btn_reset.pack(side="left", padx=5, pady=10)

        # Counter stats badge
        self.lbl_count = ctk.CTkLabel(
            search_bar,
            text="Total Member: 0",
            font=GymTheme.FONT_BADGE,
            text_color=GymTheme.TEXT_MUTED
        )
        self.lbl_count.pack(side="right", padx=20, pady=10)

        # Main Table Container (ttk.Treeview with Dark Theme styling)
        table_container = ctk.CTkFrame(self, fg_color=GymTheme.BG_CARD, corner_radius=8)
        table_container.grid(row=2, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Gym.Treeview",
            background=GymTheme.BG_CARD,
            foreground=GymTheme.TEXT_PRIMARY,
            fieldbackground=GymTheme.BG_CARD,
            rowheight=32,
            font=(GymTheme.FONT_FAMILY, 10),
            borderwidth=0
        )
        style.configure(
            "Gym.Treeview.Heading",
            background=GymTheme.BG_SURFACE,
            foreground=GymTheme.SECONDARY,
            font=(GymTheme.FONT_FAMILY, 10, "bold"),
            relief="flat",
            padding=6
        )
        style.map(
            "Gym.Treeview",
            background=[("selected", GymTheme.PRIMARY)],
            foreground=[("selected", GymTheme.TEXT_PRIMARY)]
        )

        columns = ("id", "name", "gender", "phone", "package", "quota", "reg_date", "exp_date", "status")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Gym.Treeview",
            selectmode="browse"
        )

        # Define headings & widths (Rule 3 & Kuota Sesi)
        self.tree.heading("id", text="Nomor ID")
        self.tree.heading("name", text="Nama Lengkap")
        self.tree.heading("gender", text="Jenis Kelamin")
        self.tree.heading("phone", text="No HP")
        self.tree.heading("package", text="Paket")
        self.tree.heading("quota", text="Kuota / Sesi")
        self.tree.heading("reg_date", text="Tgl Daftar")
        self.tree.heading("exp_date", text="Tgl Kedaluwarsa")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=75, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("gender", width=95, anchor="center")
        self.tree.column("phone", width=115, anchor="center")
        self.tree.column("package", width=90, anchor="center")
        self.tree.column("quota", width=120, anchor="center")
        self.tree.column("reg_date", width=95, anchor="center")
        self.tree.column("exp_date", width=105, anchor="center")
        self.tree.column("status", width=140, anchor="center")

        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Bottom Action Bar: Admin Controls (Rule 6 & 7)
        action_bar = ctk.CTkFrame(self, fg_color=GymTheme.BG_CARD, corner_radius=8)
        action_bar.grid(row=3, column=0, sticky="ew", pady=(15, 0), padx=2)

        # Selected member info
        self.lbl_selected = ctk.CTkLabel(
            action_bar,
            text="Pilih member pada tabel untuk mengelola:",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        )
        self.lbl_selected.pack(side="left", padx=15, pady=12)

        # Action Buttons on Right
        self.btn_delete = ctk.CTkButton(
            action_bar,
            text="🗑 Hapus Non-Aktif",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            height=36,
            corner_radius=6,
            state="disabled",
            command=self._confirm_delete_member
        )
        self.btn_delete.pack(side="right", padx=(5, 15), pady=12)

        # Rule 6: Admin bisa memperpanjang masa aktif paket dari member yang telah kedaluarsa
        self.btn_extend = ctk.CTkButton(
            action_bar,
            text="⟳ Perpanjang (+1 Bulan)",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.SECONDARY,
            hover_color=GymTheme.SECONDARY_HOVER,
            text_color=GymTheme.TEXT_DARK,
            height=36,
            corner_radius=6,
            state="disabled",
            command=self._extend_package
        )
        self.btn_extend.pack(side="right", padx=5, pady=12)

        # Fitur Baru: Kalender Tanda Absensi Member
        self.btn_calendar = ctk.CTkButton(
            action_bar,
            text="📅 Kalender Absensi",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.BG_MAIN,
            hover_color="#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=GymTheme.SECONDARY,
            height=36,
            corner_radius=6,
            state="disabled",
            command=self._open_calendar
        )
        self.btn_calendar.pack(side="right", padx=5, pady=12)

        self.load_members()

    def load_members(self, search_query: str = ""):
        """Memuat data member ke tabel."""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        members = self.gym_service.search_members(search_query)
        self.lbl_count.configure(text=f"Total Member: {len(members)}")

        # Configure tags for status colors
        self.tree.tag_configure("active", foreground="#4ade80")
        self.tree.tag_configure("inactive", foreground="#f87171")

        for m in members:
            status_tag = "active" if m.is_active() else "inactive"
            self.tree.insert(
                "",
                "end",
                iid=m.id,
                values=(
                    m.id,
                    m.full_name,
                    m.gender,
                    m.phone,
                    m.package,
                    m.quota_display,
                    m.registration_date.isoformat(),
                    m.expiry_date.isoformat(),
                    m.status_label
                ),
                tags=(status_tag,)
            )

        self._reset_selection_state()

    def _on_search_change(self):
        """Triggered saat user mengetik di search bar (Rule 8)."""
        query = self.entry_search.get()
        self.load_members(query)

    def _reset_search(self):
        self.entry_search.delete(0, "end")
        self.load_members()

    def _on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self._reset_selection_state()
            return

        self.selected_member_id = selected[0]
        member = self.gym_service.get_member_by_id(self.selected_member_id)
        if member:
            self.lbl_selected.configure(
                text=f"Terpilih: {member.full_name} (ID: {member.id}) • {member.package} ({member.quota_display}) • {member.status_label}"
            )
            self.btn_extend.configure(state="normal")
            self.btn_delete.configure(state="normal")
            self.btn_calendar.configure(state="normal")

    def _reset_selection_state(self):
        self.selected_member_id = None
        self.lbl_selected.configure(text="Pilih member pada tabel untuk mengelola:")
        self.btn_extend.configure(state="disabled")
        self.btn_delete.configure(state="disabled")
        self.btn_calendar.configure(state="disabled")

    def _open_calendar(self):
        """Membuka pop-up kalender tanda absensi untuk member terpilih."""
        if not self.selected_member_id:
            return
        MemberCalendarDialog(parent=self, gym_service=self.gym_service, member_id=self.selected_member_id)

    def _extend_package(self):
        """Rule 6: Perpanjang masa aktif paket."""
        if not self.selected_member_id:
            return

        try:
            member = self.gym_service.extend_member_package(self.selected_member_id, months=1)
            quota_note = "Kuota sesi telah di-reset ke 0/8 Sesi." if member.package == "Class" else "Akses bebas 1 bulan diperpanjang."
            MessageDialog(
                self,
                "Perpanjangan Berhasil",
                f"Masa aktif paket member '{member.full_name}' (ID: {member.id}) berhasil diperpanjang 1 bulan!\n"
                f"Berlaku hingga: {member.expiry_date.strftime('%d %B %Y')}.\n{quota_note}",
                is_error=False
            )
            self.load_members(self.entry_search.get())
        except GymAppException as e:
            MessageDialog(self, "Gagal Perpanjang", str(e), is_error=True)

    def _confirm_delete_member(self):
        """Rule 7: Validasi dan konfirmasi penghapusan member non-aktif."""
        if not self.selected_member_id:
            return

        member = self.gym_service.get_member_by_id(self.selected_member_id)
        if not member:
            return

        if member.is_active():
            MessageDialog(
                self,
                "Penghapusan Ditolak",
                f"Member '{member.full_name}' masih berstatus ACTIVE (berlaku s/d {member.expiry_date}).\n"
                "Sesuai aturan keamanan data, hanya member Non-Active yang boleh dihapus.",
                is_error=True
            )
            return

        def do_delete():
            try:
                self.gym_service.delete_inactive_member(member.id)
                MessageDialog(
                    self,
                    "Berhasil Dihapus",
                    f"Data member '{member.full_name}' (ID: {member.id}) telah berhasil dihapus.",
                    is_error=False
                )
                self.load_members(self.entry_search.get())
            except GymAppException as e:
                MessageDialog(self, "Gagal Menghapus", str(e), is_error=True)

        ConfirmDialog(
            parent=self,
            title="Konfirmasi Hapus Member",
            message=f"Apakah Anda yakin ingin menghapus data member '{member.full_name}' (ID: {member.id})?\n"
                    f"Status: {member.status_label}. Tindakan ini permanen.",
            on_confirm=do_delete
        )
