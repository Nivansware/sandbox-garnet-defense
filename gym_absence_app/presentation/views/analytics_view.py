"""
Analytics View - Dashboard & Grafik Pengunjung Member
Standar Premium SaaS UI/UX: Bento Grid, Calm Design, Native Vector Chart (60 FPS).
Menampilkan tren kunjungan harian, jam teramai, rasio paket, dan KPI statistik.
"""
import customtkinter as ctk
import tkinter as tk
from typing import List, Dict
from application.services import GymService
from presentation.theme import GymTheme


class VectorBarChart(ctk.CTkFrame):
    """
    Komponen Grafik Batang Vektor Berkecepatan Tinggi (Native Canvas).
    Render tajam tanpa buram resolusi, tanpa lag, dengan rounded bars dan highlight hari puncak.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=GymTheme.BG_SURFACE, corner_radius=10, **kwargs)
        self.canvas = tk.Canvas(
            self,
            bg=GymTheme.BG_SURFACE,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)
        self.canvas.bind("<Configure>", lambda e: self._redraw())
        self.data: List[Dict] = []

    def set_data(self, data: List[Dict]):
        """Memperbarui data grafik: list [{day_name: 'Sen', display_date: '08/09', count: 12}]."""
        self.data = data
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        if not self.data:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 80:
            return

        # Margins
        pad_bottom = 45
        pad_top = 35
        pad_left = 35
        pad_right = 20

        chart_w = w - pad_left - pad_right
        chart_h = h - pad_top - pad_bottom

        counts = [d["count"] for d in self.data]
        max_count = max(counts) if counts and max(counts) > 0 else 5
        # Round up max_count to pleasant number
        y_max = max_count if max_count % 2 == 0 else max_count + 1

        # Draw subtle horizontal guideline lines
        for step in [0, 0.5, 1.0]:
            y_pos = pad_top + chart_h * (1.0 - step)
            val = int(y_max * step)
            self.canvas.create_line(
                pad_left, y_pos, w - pad_right, y_pos,
                fill="#383838", dash=(2, 4), width=1
            )
            self.canvas.create_text(
                pad_left - 8, y_pos,
                text=str(val),
                fill=GymTheme.TEXT_MUTED,
                font=(GymTheme.FONT_FAMILY, 9),
                anchor="e"
            )

        n_bars = len(self.data)
        col_width = chart_w / n_bars
        bar_width = min(46, col_width * 0.58)

        # Baseline
        base_y = pad_top + chart_h
        self.canvas.create_line(
            pad_left, base_y, w - pad_right, base_y,
            fill="#444444", width=1.5
        )

        for i, item in enumerate(self.data):
            count = item["count"]
            col_center_x = pad_left + (i * col_width) + (col_width / 2)
            x0 = col_center_x - (bar_width / 2)
            x1 = col_center_x + (bar_width / 2)

            bar_h = (count / y_max) * chart_h if y_max > 0 else 0
            y0 = base_y - bar_h
            y1 = base_y

            # Peak highlight color: Amber Gold if highest and > 0, else Primary Wine Red
            is_peak = (count == max_count and count > 0)
            fill_color = GymTheme.SECONDARY if is_peak else GymTheme.PRIMARY
            border_color = GymTheme.SECONDARY_HOVER if is_peak else GymTheme.PRIMARY_HOVER

            if bar_h > 0:
                # Draw rounded rectangle effect
                self._draw_rounded_bar(x0, y0, x1, y1, fill_color, border_color)

                # Value badge on top of bar
                self.canvas.create_text(
                    col_center_x, y0 - 10,
                    text=str(count),
                    fill=GymTheme.SECONDARY if is_peak else GymTheme.TEXT_PRIMARY,
                    font=(GymTheme.FONT_FAMILY, 10, "bold")
                )
            else:
                # Empty zero indicator
                self.canvas.create_text(
                    col_center_x, base_y - 10,
                    text="0",
                    fill="#555555",
                    font=(GymTheme.FONT_FAMILY, 9)
                )

            # Day label below baseline
            day_txt = f"{item['day_name']}\n{item['display_date']}"
            self.canvas.create_text(
                col_center_x, base_y + 18,
                text=day_txt,
                fill=GymTheme.SECONDARY if is_peak else GymTheme.TEXT_MUTED,
                font=(GymTheme.FONT_FAMILY, 9, "bold" if is_peak else "normal"),
                justify="center"
            )

    def _draw_rounded_bar(self, x0, y0, x1, y1, fill_col, border_col):
        """Menggambar batang dengan sudut atas membulat."""
        radius = min(6, (x1 - x0) / 2, (y1 - y0))
        # Main bar body
        self.canvas.create_rectangle(
            x0, y0 + radius, x1, y1,
            fill=fill_col, outline="", tags="bar"
        )
        # Top rounded cap
        self.canvas.create_oval(
            x0, y0, x1, y0 + radius * 2,
            fill=fill_col, outline="", tags="bar"
        )


class AnalyticsView(ctk.CTkFrame):
    """Dashboard Analitik Pengunjung Member Gym."""

    def __init__(self, parent, gym_service: GymService):
        super().__init__(parent, fg_color="transparent")
        self.gym_service = gym_service
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Title & Refresh Button
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(10, 15))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_box,
            text="DASHBOARD & GRAFIK PENGUNJUNG",
            font=GymTheme.FONT_TITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Visualisasi data kehadiran, tren mingguan, jam tersibuk, dan distribusi paket member.",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        ).pack(anchor="w", pady=(2, 0))

        btn_refresh = ctk.CTkButton(
            header,
            text="⟳ Perbarui Grafik",
            font=GymTheme.FONT_BODY_BOLD,
            fg_color=GymTheme.BG_CARD,
            hover_color="#444444",
            text_color=GymTheme.SECONDARY,
            border_width=1,
            border_color=GymTheme.SECONDARY,
            height=36,
            corner_radius=6,
            command=self.refresh_analytics
        )
        btn_refresh.grid(row=0, column=1, sticky="e")

        # 1. Top KPI Row (4 Bento Summary Cards)
        kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        for i in range(4):
            kpi_row.grid_columnconfigure(i, weight=1)

        # Card 1: Kunjungan Hari Ini
        self.card_today, self.lbl_val_today = self._create_kpi_card(
            kpi_row, col=0, title="KUNJUNGAN HARI INI", icon="🔥", default_val="0", sub="Member Hadir"
        )
        # Card 2: Rata-rata Kunjungan
        self.card_avg, self.lbl_val_avg = self._create_kpi_card(
            kpi_row, col=1, title="RATA-RATA HARIAN", icon="📈", default_val="0.0", sub="Kunjungan / Hari"
        )
        # Card 3: Jam Teramai
        self.card_peak, self.lbl_val_peak = self._create_kpi_card(
            kpi_row, col=2, title="JAM TERAMAI (PEAK)", icon="⏱", default_val="-", sub="Rentang Jam Tersibuk"
        )
        # Card 4: Member Teraktif
        self.card_top, self.lbl_val_top = self._create_kpi_card(
            kpi_row, col=3, title="MEMBER TERAKTIF", icon="👑", default_val="-", sub="Kunjungan Terbanyak"
        )

        # 2. Main Bento Content Area (Chart + Side Widgets)
        content_grid = ctk.CTkFrame(self, fg_color="transparent")
        content_grid.grid(row=2, column=0, sticky="nsew")
        content_grid.grid_columnconfigure(0, weight=6) # 60% Left
        content_grid.grid_columnconfigure(1, weight=4) # 40% Right
        content_grid.grid_rowconfigure(0, weight=1)

        # Left Bento Card: Tren Grafik Batang
        chart_card = ctk.CTkFrame(content_grid, fg_color=GymTheme.BG_CARD, corner_radius=12, border_width=1, border_color=GymTheme.BORDER_COLOR)
        chart_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        chart_card.grid_columnconfigure(0, weight=1)
        chart_card.grid_rowconfigure(1, weight=1)

        chart_head = ctk.CTkFrame(chart_card, fg_color="transparent")
        chart_head.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            chart_head,
            text="📊 Tren Kunjungan Harian (7 Hari Terakhir)",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(side="left")

        # Legend indicator
        legend_frame = ctk.CTkFrame(chart_head, fg_color="transparent")
        legend_frame.pack(side="right")
        ctk.CTkLabel(legend_frame, text="■", text_color=GymTheme.PRIMARY, font=(GymTheme.FONT_FAMILY, 14)).pack(side="left", padx=(0, 3))
        ctk.CTkLabel(legend_frame, text="Harian", text_color=GymTheme.TEXT_MUTED, font=GymTheme.FONT_BADGE).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(legend_frame, text="■", text_color=GymTheme.SECONDARY, font=(GymTheme.FONT_FAMILY, 14)).pack(side="left", padx=(0, 3))
        ctk.CTkLabel(legend_frame, text="Puncak", text_color=GymTheme.TEXT_MUTED, font=GymTheme.FONT_BADGE).pack(side="left")

        # Vector Chart Widget
        self.bar_chart = VectorBarChart(chart_card)
        self.bar_chart.grid(row=1, column=0, sticky="nsew", padx=15, pady=(5, 15))

        # Right Bento Column: Distribution & Stats
        right_col = ctk.CTkFrame(content_grid, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)
        right_col.grid_columnconfigure(0, weight=1)
        right_col.grid_rowconfigure(0, weight=1)
        right_col.grid_rowconfigure(1, weight=1)

        # Right Bento Card 1: Distribusi Paket
        pkg_card = ctk.CTkFrame(right_col, fg_color=GymTheme.BG_CARD, corner_radius=12, border_width=1, border_color=GymTheme.BORDER_COLOR)
        pkg_card.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        ctk.CTkLabel(
            pkg_card,
            text="🏷 Distribusi Paket Pengunjung",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=18, pady=(15, 10))

        # Open Gym Bar
        open_gym_row = ctk.CTkFrame(pkg_card, fg_color="transparent")
        open_gym_row.pack(fill="x", padx=18, pady=4)
        ctk.CTkLabel(open_gym_row, text="Open Gym", font=GymTheme.FONT_BODY_BOLD, text_color=GymTheme.TEXT_PRIMARY).pack(side="left")
        self.lbl_open_gym_val = ctk.CTkLabel(open_gym_row, text="0 Kunjungan (0%)", font=GymTheme.FONT_BODY, text_color=GymTheme.PRIMARY)
        self.lbl_open_gym_val.pack(side="right")

        self.progress_open_gym = ctk.CTkProgressBar(pkg_card, fg_color=GymTheme.BG_SURFACE, progress_color=GymTheme.PRIMARY, height=10, corner_radius=5)
        self.progress_open_gym.pack(fill="x", padx=18, pady=(2, 12))

        # Class Bar
        class_row = ctk.CTkFrame(pkg_card, fg_color="transparent")
        class_row.pack(fill="x", padx=18, pady=4)
        ctk.CTkLabel(class_row, text="Class Program", font=GymTheme.FONT_BODY_BOLD, text_color=GymTheme.TEXT_PRIMARY).pack(side="left")
        self.lbl_class_val = ctk.CTkLabel(class_row, text="0 Kunjungan (0%)", font=GymTheme.FONT_BODY, text_color=GymTheme.SECONDARY)
        self.lbl_class_val.pack(side="right")

        self.progress_class = ctk.CTkProgressBar(pkg_card, fg_color=GymTheme.BG_SURFACE, progress_color=GymTheme.SECONDARY, height=10, corner_radius=5)
        self.progress_class.pack(fill="x", padx=18, pady=(2, 15))

        # Right Bento Card 2: Status Member Aktif vs Non-Aktif
        member_stats_card = ctk.CTkFrame(right_col, fg_color=GymTheme.BG_CARD, corner_radius=12, border_width=1, border_color=GymTheme.BORDER_COLOR)
        member_stats_card.grid(row=1, column=0, sticky="nsew", pady=(0, 0))

        ctk.CTkLabel(
            member_stats_card,
            text="👥 Status Keanggotaan Member",
            font=GymTheme.FONT_SUBTITLE,
            text_color=GymTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=18, pady=(15, 10))

        self.lbl_active_stat = ctk.CTkLabel(
            member_stats_card,
            text="● Member Active: 0",
            font=GymTheme.FONT_BODY_BOLD,
            text_color="#4ade80"
        )
        self.lbl_active_stat.pack(anchor="w", padx=20, pady=2)

        self.lbl_inactive_stat = ctk.CTkLabel(
            member_stats_card,
            text="● Member Non-Active: 0",
            font=GymTheme.FONT_BODY_BOLD,
            text_color="#f87171"
        )
        self.lbl_inactive_stat.pack(anchor="w", padx=20, pady=2)

        self.lbl_total_stat = ctk.CTkLabel(
            member_stats_card,
            text="Total Terdaftar: 0 Member",
            font=GymTheme.FONT_BODY,
            text_color=GymTheme.TEXT_MUTED
        )
        self.lbl_total_stat.pack(anchor="w", padx=20, pady=(6, 15))

        self.refresh_analytics()

    def _create_kpi_card(self, parent, col: int, title: str, icon: str, default_val: str, sub: str):
        """Membuat kartu metrik ringkas Bento Grid."""
        card = ctk.CTkFrame(parent, fg_color=GymTheme.BG_CARD, corner_radius=10, border_width=1, border_color=GymTheme.BORDER_COLOR)
        card.grid(row=0, column=col, sticky="nsew", padx=4, pady=0)

        head_frame = ctk.CTkFrame(card, fg_color="transparent")
        head_frame.pack(fill="x", padx=14, pady=(12, 0))

        ctk.CTkLabel(
            head_frame,
            text=f"{icon} {title}",
            font=GymTheme.FONT_BADGE,
            text_color=GymTheme.TEXT_MUTED
        ).pack(side="left")

        val_lbl = ctk.CTkLabel(
            card,
            text=default_val,
            font=(GymTheme.FONT_FAMILY, 22, "bold"),
            text_color=GymTheme.TEXT_PRIMARY
        )
        val_lbl.pack(anchor="w", padx=14, pady=(4, 0))

        ctk.CTkLabel(
            card,
            text=sub,
            font=(GymTheme.FONT_FAMILY, 10),
            text_color=GymTheme.TEXT_MUTED
        ).pack(anchor="w", padx=14, pady=(0, 12))

        return card, val_lbl

    def refresh_analytics(self):
        """Mengambil data analitik terbaru dari GymService dan memperbarui UI."""
        data = self.gym_service.get_dashboard_analytics()

        # Update Top KPIs
        self.lbl_val_today.configure(text=str(data["today_visitors"]))
        self.lbl_val_avg.configure(text=str(data["weekly_average"]))
        self.lbl_val_peak.configure(text=data["peak_hours"])

        top_m = data["top_member"]
        if top_m:
            self.lbl_val_top.configure(text=f"{top_m['name'][:12]} ({top_m['total_visits']}x)")
        else:
            self.lbl_val_top.configure(text="-")

        # Update Chart Data
        self.bar_chart.set_data(data["daily_trend"])

        # Update Package Ratio
        pkg = data["package_distribution"]
        open_count = pkg.get("Open Gym", 0)
        class_count = pkg.get("Class", 0)
        open_pct = data["open_gym_pct"]
        class_pct = data["class_pct"]

        self.lbl_open_gym_val.configure(text=f"{open_count} Kunjungan ({open_pct}%)")
        self.lbl_class_val.configure(text=f"{class_count} Kunjungan ({class_pct}%)")
        self.progress_open_gym.set(open_pct / 100.0)
        self.progress_class.set(class_pct / 100.0)

        # Update Member Counts
        total_m = data["total_members"]
        active_m = data["active_members"]
        inactive_m = data["inactive_members"]

        self.lbl_active_stat.configure(text=f"● Member Active: {active_m}")
        self.lbl_inactive_stat.configure(text=f"● Member Non-Active: {inactive_m}")
        self.lbl_total_stat.configure(text=f"Total Terdaftar: {total_m} Member")
