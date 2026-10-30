"""
View Pendaftaran Member (Rule 1 & 2)
Users mengisi form biodata lengkap (Nama, Jenis Kelamin, Alamat, No HP)
dan memilih paket 1 bulan (Open Gym / Class). ID otomatis 001..999..1000.
"""
import customtkinter as ctk
from datetime import date, timedelta
from typing import Callable, Optional
from application.services import GymService
from domain.entities import PackageType, Gender
from domain.exceptions import GymAppException
from presentation.theme import GymTheme
from presentation.dialogs import MessageDialog


class RegistrationView(ctk.CTkFrame):
    """Form Pendaftaran Member Baru."""

    def __init__(self, parent, gym_service: GymService, on_member_registered: Optional[Callable] = None):
        super().__init__(parent, fg_color="transparent")
        self.gym_service = gym_service
        self.on_member_registered = on_member_registered
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Title
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        ctk.CTkLabel(
            header,
            text="FORM PENDAFTARAN MEMBER BARU",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Lengkapi biodata member untuk mendapatkan nomor ID dan masa aktif paket 1 bulan.",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        ).pack(anchor="w", pady=(2, 0))

        # Main Bento Scroll Frame
        scroll_form = ctk.CTkScrollableFrame(
            self,
            fg_color=GymTheme.BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=GymTheme.BORDER_COLOR
        )
        scroll_form.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        scroll_form.grid_columnconfigure(0, weight=1)
        scroll_form.grid_columnconfigure(1, weight=1)

        # 1. Nomor ID Member (Auto-generated preview)
        lbl_id = ctk.CTkLabel(
            scroll_form,
            text="Nomor ID Member (Otomatis / Terisi):",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.SECONDARY
        )
        lbl_id.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 4))

        self.entry_id = ctk.CTkEntry(
            scroll_form,
            font=(GymTheme.FONT_FAMILY, 14, "bold"),
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.SECONDARY,
            height=38,
            corner_radius=6
        )
        self.entry_id.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 15))

        # 2. Nama Lengkap
        lbl_name = ctk.CTkLabel(
            scroll_form,
            text="Nama Lengkap:",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_name.grid(row=2, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 4))

        self.entry_name = ctk.CTkEntry(
            scroll_form,
            placeholder_text="Masukkan nama lengkap member...",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=6
        )
        self.entry_name.grid(row=3, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 15))

        # 3. Jenis Kelamin (OptionMenu)
        lbl_gender = ctk.CTkLabel(
            scroll_form,
            text="Jenis Kelamin:",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_gender.grid(row=4, column=0, sticky="w", padx=(30, 10), pady=(0, 4))

        self.combo_gender = ctk.CTkOptionMenu(
            scroll_form,
            values=[Gender.MALE.value, Gender.FEMALE.value],
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            button_color=GymTheme.PRIMARY,
            button_hover_color=GymTheme.PRIMARY_HOVER,
            dropdown_fg_color=GymTheme.BG_CARD,
            dropdown_text_color=GymTheme.TEXT_PRIMARY,
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=6
        )
        self.combo_gender.grid(row=5, column=0, sticky="ew", padx=(30, 10), pady=(0, 15))

        # 4. Nomor HP
        lbl_phone = ctk.CTkLabel(
            scroll_form,
            text="Nomor Handphone (WhatsApp):",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_phone.grid(row=4, column=1, sticky="w", padx=(10, 30), pady=(0, 4))

        self.entry_phone = ctk.CTkEntry(
            scroll_form,
            placeholder_text="Contoh: 081234567890",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=6
        )
        self.entry_phone.grid(row=5, column=1, sticky="ew", padx=(10, 30), pady=(0, 15))

        # 5. Pilihan Paket (Rule 2: Open Gym / Class dalam 1 bulan)
        lbl_pkg = ctk.CTkLabel(
            scroll_form,
            text="Pilihan Paket Member (Masa Aktif 1 Bulan):",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_pkg.grid(row=6, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 4))

        self.combo_package = ctk.CTkOptionMenu(
            scroll_form,
            values=[PackageType.OPEN_GYM.value, PackageType.CLASS.value],
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            button_color=GymTheme.SECONDARY,
            button_hover_color=GymTheme.SECONDARY_HOVER,
            dropdown_fg_color=GymTheme.BG_CARD,
            dropdown_text_color=GymTheme.TEXT_PRIMARY,
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=6
        )
        self.combo_package.grid(row=7, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 15))

        # 6. Alamat Lengkap
        lbl_addr = ctk.CTkLabel(
            scroll_form,
            text="Alamat Lengkap Tempat Tinggal:",
            font=GymTheme.FONT_BODY_BOLD,
            text_color=GymTheme.TEXT_PRIMARY
        )
        lbl_addr.grid(row=8, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 4))

        self.entry_address = ctk.CTkEntry(
            scroll_form,
            placeholder_text="Masukkan alamat lengkap...",
            font=GymTheme.FONT_BODY,
            fg_color=GymTheme.BG_INPUT,
            border_color=GymTheme.BORDER_COLOR,
            text_color=GymTheme.TEXT_PRIMARY,
            height=38,
            corner_radius=6
        )
        self.entry_address.grid(row=9, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 20))

        # Preview Information Box
        preview_box = ctk.CTkFrame(scroll_form, fg_color=GymTheme.BG_SURFACE, corner_radius=8)
        preview_box.grid(row=10, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 20))

        today_str = date.today().strftime("%d %B %Y")
        exp_str = (date.today() + timedelta(days=30)).strftime("%d %B %Y")
        info_text = (
            f"📅 Tanggal Pendaftaran: {today_str}\n"
            f"⏳ Masa Berlaku Paket: 1 Bulan (Berakhir pada: {exp_str})\n"
            f"🏋️ Aturan Paket Class: Maksimal 8 sesi latihan bersama Coach gym.\n"
            f"💪 Aturan Paket Open Gym: Bebas absensi selama rentang 1 bulan (1x per hari).\n"
            f"🔰 Status Awal: Active (Dapat langsung digunakan untuk absensi)"
        )
        ctk.CTkLabel(
            preview_box,
            text=info_text,
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED,
            justify="left"
        ).pack(padx=16, pady=12, anchor="w")

        # Submit Button (Warna Primer #c00707)
        btn_submit = ctk.CTkButton(
            scroll_form,
            text="DAFTAR MEMBER SEKARANG",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.PRIMARY,
            hover_color=GymTheme.PRIMARY_HOVER,
            text_color=GymTheme.TEXT_PRIMARY,
            height=46,
            corner_radius=8,
            command=self._submit_registration
        )
        btn_submit.grid(row=11, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 25))

        self.refresh_form_defaults()

    def refresh_form_defaults(self):
        """Merestart nilai input dan memperbarui auto-generated ID berikutnya."""
        next_id = self.gym_service.get_next_member_id()
        self.entry_id.delete(0, "end")
        self.entry_id.insert(0, next_id)

        self.entry_name.delete(0, "end")
        self.entry_phone.delete(0, "end")
        self.entry_address.delete(0, "end")
        self.combo_gender.set(Gender.MALE.value)
        self.combo_package.set(PackageType.OPEN_GYM.value)

    def _submit_registration(self):
        """Menyimpan data pendaftaran member baru."""
        target_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        gender = self.combo_gender.get()
        phone = self.entry_phone.get().strip()
        package = self.combo_package.get()
        address = self.entry_address.get().strip()

        try:
            member = self.gym_service.register_member(
                full_name=name,
                gender=gender,
                address=address,
                phone=phone,
                package=package,
                custom_id=target_id
            )

            msg = (
                f"Member '{member.full_name}' dengan Nomor ID '{member.id}' "
                f"berhasil terdaftar!\nPaket: {member.package} (Aktif s/d {member.expiry_date})."
            )
            MessageDialog(self, "Pendaftaran Berhasil", msg, is_error=False)

            self.refresh_form_defaults()

            if self.on_member_registered:
                self.on_member_registered()

        except GymAppException as e:
            MessageDialog(self, "Pendaftaran Gagal", str(e), is_error=True)
