"""
View Absensi Kehadiran Member (Rule 4 & 5)
Input nomor ID -> Tekan Tombol Kehadiran -> Pop Up Berhasil Absen -> Kembali ke Halaman Utama.
"""
import customtkinter as ctk
from datetime import datetime
from application.services import GymService
from domain.exceptions import GymAppException
from presentation.theme import GymTheme
from presentation.dialogs import AttendanceSuccessDialog, MessageDialog


class AttendanceView(ctk.CTkFrame):
    """Tampilan Presensi Cepat Member Gym."""

    def __init__(self, parent, gym_service: GymService, on_navigate_home=None):
        super().__init__(parent, fg_color="transparent")
        self.gym_service = gym_service
        self.on_navigate_home = on_navigate_home
        self._build_ui()

    def _build_ui(self):
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        lbl_title = ctk.CTkLabel(
            header_frame,
            text="PRESENSI KEHADIRAN MEMBER",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_title.pack(anchor="w")

        lbl_desc = ctk.CTkLabel(
            header_frame,
            text="Masukkan nomor ID Member untuk mencatat kehadiran hari ini.",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        )
        lbl_desc.pack(anchor="w", pady=(2, 0))

        # Main Bento Container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=4)
        content_frame.grid_columnconfigure(1, weight=5)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left Card: Input ID & Tombol Absen
        checkin_card = ctk.CTkFrame(
            content_frame,
            fg_color=GymTheme.BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=GymTheme.BORDER_COLOR
        )
        checkin_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)

        ctk.CTkLabel(
            checkin_card,
            text="INPUT ID KEHADIRAN",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.SECONDARY
        ).pack(anchor="w", padx=25, pady=(25, 10))

        ctk.CTkLabel(
            checkin_card,
            text="Nomor ID Member (Contoh: 001, 002, 1000):",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=25, pady=(5, 5))

        # ID Entry Field
        self.entry_id = ctk.CTkEntry(
            checkin_card,
            placeholder_text="Ketik Nomor ID...",
            font=(GymTheme.FONT_FAMILY, 16, "bold"),
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.TEXT_PRIMARY,
            height=48,
            corner_radius=8
        )
        self.entry_id.pack(fill="x", padx=25, pady=(0, 15))
        self.entry_id.bind("<Return>", lambda event: self._submit_attendance())

        # Tombol Kehadiran (Rule 4: Tombol Kehadiran dengan Warna Primer #c00707)
        self.btn_submit = ctk.CTkButton(
            checkin_card,
            text="✓ TOMBOL KEHADIRAN / ABSEN",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            height=48,
            corner_radius=8,
            command=self._submit_attendance
        )
        self.btn_submit.pack(fill="x", padx=25, pady=(5, 20))

        # Instructions helper
        helper_box = ctk.CTkFrame(checkin_card, fg_color=GymTheme.BG_SURFACE, corner_radius=8)
        helper_box.pack(fill="x", padx=25, pady=(10, 20))

        instructions = (
            "📌 Informasi Alur & Aturan:\n"
            "• Tekan tombol kehadiran setelah mengisi ID.\n"
            "• Maksimal 1 kali absensi per hari.\n"
            "• Paket Class: Maksimal 8 sesi latihan coach.\n"
            "• Paket Open Gym: Akses bebas 1 bulan."
        )
        ctk.CTkLabel(
            helper_box,
            text=instructions,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED,
            justify="left"
        ).pack(padx=15, pady=12, anchor="w")

        # Right Card: Riwayat Absensi Terkini
        history_card = ctk.CTkFrame(
            content_frame,
            fg_color=GymTheme.BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=GymTheme.BORDER_COLOR
        )
        history_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)

        lbl_hist_title = ctk.CTkLabel(
            history_card,
            text="RIWAYAT KEHADIRAN TERBARU",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_hist_title.pack(anchor="w", padx=20, pady=(20, 10))

        # Scrollable Frame for Attendance Logs
        self.log_scroll = ctk.CTkScrollableFrame(
            history_card,
            fg_color=GymTheme.BG_SURFACE,
            corner_radius=8
        )
        self.log_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.refresh_attendance_logs()

    def _submit_attendance(self):
        """Mengeksekusi proses absensi berdasarkan nomor ID."""
        raw_id = self.entry_id.get().strip()
        if not raw_id:
            MessageDialog(self, "Validasi Input", "Silakan masukkan Nomor ID Member terlebih dahulu.", is_error=True)
            self.entry_id.focus_set()
            return

        try:
            member, attendance = self.gym_service.record_attendance(raw_id)
            self.entry_id.delete(0, "end")
            self.refresh_attendance_logs()

            # Pop-up Berhasil Absen (Rule 5)
            def on_close():
                if self.on_navigate_home:
                    self.on_navigate_home()
                self.entry_id.focus_set()

            AttendanceSuccessDialog(
                parent=self,
                member_name=member.full_name,
                member_id=member.id,
                package=member.package,
                session_info=member.quota_display,
                on_close_callback=on_close
            )
        except GymAppException as e:
            MessageDialog(self, "Gagal Absen", str(e), is_error=True)
            self.entry_id.focus_set()

    def refresh_attendance_logs(self):
        """Memperbarui daftar riwayat absensi terbaru."""
        for child in self.log_scroll.winfo_children():
            child.destroy()

        logs = self.gym_service.get_recent_attendances(limit=15)
        if not logs:
            lbl_empty = ctk.CTkLabel(
                self.log_scroll,
                text="Belum ada data kehadiran hari ini.",
                font=GymTheme.FONT_BODY,
                text_color=GymTheme.TEXT_MUTED
            )
            lbl_empty.pack(pady=40)
            return

        for item in logs:
            row = ctk.CTkFrame(self.log_scroll, fg_color=GymTheme.BG_CARD, corner_radius=6)
            row.pack(fill="x", pady=4, padx=5)

            # Left badge (ID)
            id_badge = ctk.CTkLabel(
                row,
                text=f"ID {item['member_id']}",
                font=GymTheme.FONT_BADGE,
                text_color=GymTheme.SECONDARY,
                fg_color=GymTheme.BG_MAIN,
                corner_radius=4,
                width=65,
                height=26
            )
            id_badge.pack(side="left", padx=(10, 10), pady=8)

            # Middle text
            info_txt = f"{item['full_name']} • {item['package']}"
            lbl_info = ctk.CTkLabel(
                row,
                text=info_txt,
                font=GymTheme.FONT_BODY_BOLD,
                text_color=GymTheme.TEXT_PRIMARY
            )
            lbl_info.pack(side="left", padx=5)

            # Right time
            time_txt = f"{item['attendance_time']} ({item['attendance_date']})"
            lbl_time = ctk.CTkLabel(
                row,
                text=time_txt,
                font=GymTheme.FONT_BODY,
                text_color=GymTheme.TEXT_MUTED
            )
            lbl_time.pack(side="right", padx=12)
