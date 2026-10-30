"""
Main GUI Application Window
Mengintegrasikan seluruh view, styling modern SaaS Dark Mode, dan navigasi tab.
"""
import customtkinter as ctk
from application.services import GymService
from infrastructure.database import DatabaseManager
from infrastructure.repository import SQLiteMemberRepository, SQLiteAttendanceRepository
from presentation.theme import GymTheme
from presentation.views.attendance_view import AttendanceView
from presentation.views.registration_view import RegistrationView
from presentation.views.member_list_view import MemberListView
from presentation.views.analytics_view import AnalyticsView


class GymAbsenceApp(ctk.CTk):
    """Jendela Utama Aplikasi Absensi Gym."""

    def __init__(self, db_path: str = "gym_absence.db"):
        super().__init__()

        # Appearance Settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Window Configuration
        self.title("Nivans Gym — Sistem Absensi & Keanggotaan Member")
        self.geometry("1140x740")
        self.minsize(1020, 660)
        self.configure(fg_color=GymTheme.BG_MAIN)

        # Initialize Services & Repositories
        self.db_manager = DatabaseManager(db_path)
        self.member_repo = SQLiteMemberRepository(self.db_manager)
        self.attendance_repo = SQLiteAttendanceRepository(self.db_manager)
        self.gym_service = GymService(self.member_repo, self.attendance_repo)

        self._build_shell()

    def _build_shell(self):
        """Membangun layout shell: Topbar / Header + Tab Navigation + Content Area."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Top Bar / Header
        top_bar = ctk.CTkFrame(self, fg_color=GymTheme.BG_SURFACE, height=72, corner_radius=0)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        # Branding Header
        brand_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        brand_frame.grid(row=0, column=0, sticky="w", padx=25, pady=12)

        lbl_logo = ctk.CTkLabel(
            brand_frame,
            text="NIVANS GYM",
            font=(GymTheme.FONT_FAMILY, 20, "bold"),
            text_color=GymTheme.PRIMARY
        )
        lbl_logo.pack(side="left")

        lbl_slash = ctk.CTkLabel(
            brand_frame,
            text=" | ",
            font=(GymTheme.FONT_FAMILY, 16, "bold"),
            text_color=GymTheme.SECONDARY
        )
        lbl_slash.pack(side="left")

        lbl_tagline = ctk.CTkLabel(
            brand_frame,
            text="SISTEM ABSENSI & MANAJEMEN MEMBER",
            font=(GymTheme.FONT_FAMILY, 13, "bold"),
            text_color=GymTheme.TEXT_MUTED
        )
        lbl_tagline.pack(side="left")

        # Nav Segmented Buttons (4 Tabs)
        self.nav_tabs = ctk.CTkSegmentedButton(
            top_bar,
            values=[
                "📌 Absensi Kehadiran",
                "📝 Pendaftaran Member",
                "📋 Data Member & Admin",
                "📊 Statistik & Grafik"
            ],
            font=GymTheme.FONT_BODY_BOLD,
            selected_color=GymTheme.PRIMARY,
            selected_hover_color=GymTheme.PRIMARY_HOVER,
            unselected_color=GymTheme.BG_MAIN,
            unselected_hover_color="#3a3a3a",
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=8,
            command=self._on_tab_switched
        )
        self.nav_tabs.grid(row=0, column=1, sticky="e", padx=25, pady=12)

        # 2. Main Content Container
        self.content_frame = ctk.CTkFrame(self, fg_color=GymTheme.BG_MAIN, corner_radius=0)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=15)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize Sub-Views
        self.attendance_view = AttendanceView(
            self.content_frame,
            gym_service=self.gym_service,
            on_navigate_home=self.navigate_to_attendance
        )
        self.registration_view = RegistrationView(
            self.content_frame,
            gym_service=self.gym_service,
            on_member_registered=self._on_member_registered
        )
        self.member_list_view = MemberListView(
            self.content_frame,
            gym_service=self.gym_service
        )
        self.analytics_view = AnalyticsView(
            self.content_frame,
            gym_service=self.gym_service
        )

        # Default Active Tab
        self.nav_tabs.set("📌 Absensi Kehadiran")
        self._show_view(self.attendance_view)

    def _show_view(self, target_view: ctk.CTkFrame):
        """Menampilkan view yang dipilih dan menyembunyikan yang lain."""
        for v in [self.attendance_view, self.registration_view, self.member_list_view, self.analytics_view]:
            v.grid_forget()
        target_view.grid(row=0, column=0, sticky="nsew")

    def _on_tab_switched(self, selected_value: str):
        """Handler perpindahan tab."""
        if selected_value == "📌 Absensi Kehadiran":
            self.attendance_view.refresh_attendance_logs()
            self._show_view(self.attendance_view)
        elif selected_value == "📝 Pendaftaran Member":
            self.registration_view.refresh_form_defaults()
            self._show_view(self.registration_view)
        elif selected_value == "📋 Data Member & Admin":
            self.member_list_view.load_members()
            self._show_view(self.member_list_view)
        elif selected_value == "📊 Statistik & Grafik":
            self.analytics_view.refresh_analytics()
            self._show_view(self.analytics_view)

    def navigate_to_attendance(self):
        """Navigasi otomatis kembali ke halaman utama absensi (Rule 5)."""
        self.nav_tabs.set("📌 Absensi Kehadiran")
        self.attendance_view.refresh_attendance_logs()
        self._show_view(self.attendance_view)

    def _on_member_registered(self):
        """Callback ketika member baru sukses terdaftar."""
        self.member_list_view.load_members()
        self.attendance_view.refresh_attendance_logs()
        self.analytics_view.refresh_analytics()


def create_app(db_path: str = "gym_absence.db") -> GymAbsenceApp:
    """Factory function untuk inisialisasi aplikasi."""
    return GymAbsenceApp(db_path=db_path)
