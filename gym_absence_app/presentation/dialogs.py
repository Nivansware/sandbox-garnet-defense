"""
Modern Modal Dialogs
Menyediakan pop-up notifikasi kustom dengan CustomTkinter sesuai aturan Rule 5 & 7.
"""
import customtkinter as ctk
from typing import Callable, Optional
from presentation.theme import GymTheme


class AttendanceSuccessDialog(ctk.CTkToplevel):
    """
    Pop-up Notifikasi Kehadiran (Rule 5):
    Notifikasi: 'Anda berhasil absen pada hari ini' dan kembali ke halaman utama.
    """

    def __init__(self, parent, member_name: str, member_id: str, package: str, session_info: str = "", on_close_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        
        self.title("Kehadiran Berhasil")
        self.geometry("450x350")
        self.resizable(False, False)
        self.configure(fg_color=GymTheme.BG_SURFACE)
        
        # Center the window
        self.transient(parent)
        self.grab_set()
        self._center_window(parent)

        # Container Card
        card = ctk.CTkFrame(
            self,
            fg_color=GymTheme.BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=GymTheme.SECONDARY
        )
        card.pack(padx=20, pady=20, fill="both", expand=True)

        # Icon / Badge Header
        icon_badge = ctk.CTkLabel(
            card,
            text="✓",
            font=(GymTheme.FONT_FAMILY, 38, "bold"),
            text_color=GymTheme.SECONDARY,
            fg_color=GymTheme.BG_MAIN,
            width=64,
            height=64,
            corner_radius=32
        )
        icon_badge.pack(pady=(16, 8))

        # Main Notification Title (Rule 5 Exact Text)
        title_label = ctk.CTkLabel(
            card,
            text="Anda berhasil absen pada hari ini",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY,
            wraplength=380
        )
        title_label.pack(pady=(4, 8))

        # Member Info Subtitle with Session Quota
        if session_info:
            info_text = f"Member: {member_name} (ID: {member_id})\nPaket: {package}  •  Kuota: {session_info}"
        else:
            info_text = f"Member: {member_name} (ID: {member_id})\nPaket: {package}"

        info_label = ctk.CTkLabel(
            card,
            text=info_text,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED,
            justify="center"
        )
        info_label.pack(pady=(0, 15))

        # OK / Kembali ke Halaman Utama Button
        btn_ok = ctk.CTkButton(
            card,
            text="Kembali ke Halaman Utama",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            corner_radius=8,
            height=40,
            command=self._dismiss
        )
        btn_ok.pack(pady=(5, 15), padx=40, fill="x")

        self.protocol("WM_DELETE_WINDOW", self._dismiss)

    def _center_window(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + max(0, (pw - w) // 2)
        y = py + max(0, (ph - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _dismiss(self):
        self.destroy()
        if self.on_close_callback:
            self.on_close_callback()


class MessageDialog(ctk.CTkToplevel):
    """Modern Alert / Info / Error Dialog."""

    def __init__(self, parent, title: str, message: str, is_error: bool = False):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x240")
        self.resizable(False, False)
        self.configure(fg_color=GymTheme.BG_SURFACE)
        self.transient(parent)
        self.grab_set()

        card = ctk.CTkFrame(
            self,
            fg_color=GymTheme.BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=GymTheme.PRIMARY if is_error else GymTheme.SECONDARY
        )
        card.pack(padx=20, pady=20, fill="both", expand=True)

        header_color = GymTheme.PRIMARY if is_error else GymTheme.SECONDARY
        icon_text = "✕" if is_error else "ℹ"

        lbl_icon = ctk.CTkLabel(
            card,
            text=icon_text,
            font=(GymTheme.FONT_FAMILY, 24, "bold"),
            text_color=header_color
        )
        lbl_icon.pack(pady=(15, 5))

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_title.pack(pady=(0, 8))

        lbl_msg = ctk.CTkLabel(
            card,
            text=message,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED,
            wraplength=350,
            justify="center"
        )
        lbl_msg.pack(pady=(0, 15), padx=15)

        btn_close = ctk.CTkButton(
            card,
            text="Tutup",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY if is_error else GymTheme.BG_MAIN,
            hover_color=GymTheme.PRIMARY_HOVER if is_error else "#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            height=36,
            corner_radius=8,
            command=self.destroy
        )
        btn_close.pack(padx=50, fill="x", pady=(0, 15))


class ConfirmDialog(ctk.CTkToplevel):
    """Modern Confirmation Modal for High-Impact Actions (e.g. Deletion)."""

    def __init__(self, parent, title: str, message: str, on_confirm: Callable):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.title(title)
        self.geometry("420x250")
        self.resizable(False, False)
        self.configure(fg_color=GymTheme.BG_SURFACE)
        self.transient(parent)
        self.grab_set()

        card = ctk.CTkFrame(
            self,
            fg_color=GymTheme.BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=GymTheme.PRIMARY
        )
        card.pack(padx=20, pady=20, fill="both", expand=True)

        lbl_icon = ctk.CTkLabel(
            card,
            text="⚠",
            font=(GymTheme.FONT_FAMILY, 28, "bold"),
            text_color=GymTheme.SECONDARY
        )
        lbl_icon.pack(pady=(15, 5))

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_title.pack(pady=(0, 6))

        lbl_msg = ctk.CTkLabel(
            card,
            text=message,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED,
            wraplength=350,
            justify="center"
        )
        lbl_msg.pack(pady=(0, 15), padx=15)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(0, 15))

        btn_cancel = ctk.CTkButton(
            btn_row,
            text="Batal",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_MAIN,
            hover_color="#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            height=36,
            corner_radius=8,
            command=self.destroy
        )
        btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_yes = ctk.CTkButton(
            btn_row,
            text="Ya, Lanjutkan",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            height=36,
            corner_radius=8,
            command=self._confirm
        )
        btn_yes.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def _confirm(self):
        self.destroy()
        self.on_confirm()


class MemberCalendarDialog(ctk.CTkToplevel):
    """
    Dialog Kalender Tanda Absensi Member:
    Menampilkan grid kalender bulanan interaktif, menandai tanggal kehadiran (dengan jam absen),
    serta navigasi antar bulan dan counter total kunjungan.
    """

    MONTH_NAMES = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    DAY_NAMES = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

    def __init__(self, parent, gym_service, member_id: str):
        super().__init__(parent)
        import calendar
        from datetime import date

        self.gym_service = gym_service
        self.member_id = member_id
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month

        self.title("Kalender Kehadiran Member")
        self.geometry("640x660")
        self.minsize(580, 600)
        self.configure(fg_color=GymTheme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._render_calendar()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Info Member
        member = self.gym_service.get_member_by_id(self.member_id)
        header_card = ctk.CTkFrame(self, fg_color=GymTheme.BG_SURFACE, corner_radius=10)
        header_card.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        lbl_name = ctk.CTkLabel(
            header_card,
            text=f"KALENDER ABSENSI: {member.full_name.upper()}",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_name.pack(anchor="w", padx=16, pady=(12, 2))

        sub_info = f"ID: {member.id}  •  Paket: {member.package}  •  Status: {member.status_label}  •  Kuota: {member.quota_display}"
        lbl_sub = ctk.CTkLabel(
            header_card,
            text=sub_info,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.SECONDARY if member.is_active() else GymTheme.TEXT_MUTED
        )
        lbl_sub.pack(anchor="w", padx=16, pady=(0, 12))

        # Month Navigation Bar
        nav_bar = ctk.CTkFrame(self, fg_color=GymTheme.BG_CARD, corner_radius=8)
        nav_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        nav_bar.grid_columnconfigure(1, weight=1)

        btn_prev = ctk.CTkButton(
            nav_bar,
            text="◀ Bulan Lalu",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.BG_MAIN,
            hover_color="#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            width=110,
            height=34,
            command=self._prev_month
        )
        btn_prev.grid(row=0, column=0, padx=10, pady=8)

        self.lbl_month_year = ctk.CTkLabel(
            nav_bar,
            text="",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        )
        self.lbl_month_year.grid(row=0, column=1, pady=8)

        btn_next = ctk.CTkButton(
            nav_bar,
            text="Bulan Depan ▶",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.BG_MAIN,
            hover_color="#444444",
            text_color=GymTheme.TEXT_PRIMARY,
            width=110,
            height=34,
            command=self._next_month
        )
        btn_next.grid(row=0, column=2, padx=10, pady=8)

        # Calendar Container
        self.cal_frame = ctk.CTkFrame(self, fg_color=GymTheme.BG_CARD, corner_radius=10)
        self.cal_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        for col in range(7):
            self.cal_frame.grid_columnconfigure(col, weight=1)

        # Bottom Summary & Close
        bottom_bar = ctk.CTkFrame(self, fg_color=GymTheme.BG_SURFACE, corner_radius=8)
        bottom_bar.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

        self.lbl_summary = ctk.CTkLabel(
            bottom_bar,
            text="Total Kehadiran Bulan Ini: 0 Hari",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.SECONDARY
        )
        self.lbl_summary.pack(side="left", padx=16, pady=10)

        btn_close = ctk.CTkButton(
            bottom_bar,
            text="Tutup Kalender",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            width=120,
            height=34,
            command=self.destroy
        )
        btn_close.pack(side="right", padx=16, pady=10)

    def _render_calendar(self):
        """Merender grid kalender bulan terpilih dengan tanda absensi."""
        import calendar
        from datetime import date

        # Bersihkan widget kalender lama
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        month_str = self.MONTH_NAMES[self.current_month]
        self.lbl_month_year.configure(text=f"🗓 {month_str} {self.current_year}")

        # Header Hari (Sen - Min)
        for idx, day_name in enumerate(self.DAY_NAMES):
            lbl_d = ctk.CTkLabel(
                self.cal_frame,
                text=day_name,
                font=GymTheme.FONT_BADGE,
                text_color=GymTheme.SECONDARY if idx >= 5 else GymTheme.TEXT_MUTED
            )
            lbl_d.grid(row=0, column=idx, pady=(10, 6), sticky="ew")

        # Ambil data kehadiran dari service
        cal_data = self.gym_service.get_member_attendance_calendar(
            self.member_id, self.current_year, self.current_month
        )
        attended_days = cal_data["attended_days"] # {day: time_str}
        total_attended = cal_data["total_attended"]

        self.lbl_summary.configure(
            text=f"Total Kehadiran di Bulan {month_str}: {total_attended} Hari"
        )

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(self.current_year, self.current_month)

        row_idx = 1
        for week in weeks:
            self.cal_frame.grid_rowconfigure(row_idx, weight=1)
            for col_idx, day_date in enumerate(week):
                is_curr_month = (day_date.month == self.current_month)
                has_attended = is_curr_month and (day_date.day in attended_days)

                cell_bg = GymTheme.PRIMARY if has_attended else (GymTheme.BG_INPUT if is_curr_month else GymTheme.BG_CARD)
                border_col = GymTheme.SECONDARY if has_attended else ("#3e3e3e" if is_curr_month else "#2f2f2f")

                cell = ctk.CTkFrame(
                    self.cal_frame,
                    fg_color=cell_bg,
                    corner_radius=8,
                    border_width=1,
                    border_color=border_col
                )
                cell.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky="nsew")

                if is_curr_month:
                    # Day number
                    day_color = GymTheme.TEXT_PRIMARY if has_attended else "#e0e0e0"
                    lbl_day = ctk.CTkLabel(
                        cell,
                        text=str(day_date.day),
                        font=(GymTheme.FONT_FAMILY, 13, "bold" if has_attended else "normal"),
                        text_color=day_color
                    )
                    lbl_day.pack(pady=(4, 0))

                    if has_attended:
                        time_str = attended_days[day_date.day][:5] # HH:MM
                        badge_lbl = ctk.CTkLabel(
                            cell,
                            text=f"✓ {time_str}",
                            font=(GymTheme.FONT_FAMILY, 10, "bold"),
                            text_color=GymTheme.TEXT_PRIMARY,
                            fg_color="#850505",
                            corner_radius=4,
                            height=18
                        )
                        badge_lbl.pack(pady=(2, 4), padx=3)
                    else:
                        # Empty spacer
                        ctk.CTkLabel(cell, text="", height=18).pack(pady=(2, 4))
                else:
                    # Previous/Next month padding
                    lbl_muted = ctk.CTkLabel(
                        cell,
                        text=str(day_date.day),
                        font=(GymTheme.FONT_FAMILY, 11),
                        text_color="#555555"
                    )
                    lbl_muted.pack(pady=(4, 0))
                    ctk.CTkLabel(cell, text="", height=18).pack(pady=(2, 4))

            row_idx += 1

    def _prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._render_calendar()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._render_calendar()

