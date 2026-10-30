"""
Application Service Layer
Mengorkestrasikan Use Cases dan aturan bisnis aplikasi Gym Absence.
Tidak bergantung pada UI toolkit (CustomTkinter / CLI / Web) agar mudah di-test.
"""
from datetime import date, datetime, timedelta
from typing import List, Optional
from domain.entities import Member, Attendance, PackageType, Gender, MemberStatus
from domain.exceptions import (
    MemberNotFoundError,
    MemberAlreadyExistsError,
    MemberAlreadyCheckedInTodayError,
    ClassQuotaExceededError,
    MemberActiveCannotBeDeletedError,
    InvalidMemberDataError,
)
from infrastructure.repository import SQLiteMemberRepository, SQLiteAttendanceRepository


class GymService:
    """Service pengelola operasi bisnis member dan absensi gym."""

    def __init__(
        self,
        member_repo: SQLiteMemberRepository,
        attendance_repo: SQLiteAttendanceRepository
    ):
        self.member_repo = member_repo
        self.attendance_repo = attendance_repo

    def get_next_member_id(self) -> str:
        """Mengambil usulan nomor ID berikutnya (001 ... 999 -> 1000)."""
        return self.member_repo.get_next_member_id()

    def register_member(
        self,
        full_name: str,
        gender: str,
        address: str,
        phone: str,
        package: str,
        custom_id: Optional[str] = None,
        registration_date: Optional[date] = None,
    ) -> Member:
        """
        Mendaftarkan member baru.
        Validasi input lengkap, kalkulasi masa aktif 1 bulan (30 hari).
        Paket Class mendapatkan kuota 8 sesi latihan bersama coach.
        Paket Open Gym bebas absensi selama rentang 1 bulan aktif.
        """
        # Validasi nama lengkap
        cleaned_name = full_name.strip()
        if not cleaned_name or len(cleaned_name) < 2:
            raise InvalidMemberDataError("Nama lengkap wajib diisi (minimal 2 karakter).")

        # Validasi jenis kelamin
        valid_genders = [g.value for g in Gender]
        if gender not in valid_genders:
            raise InvalidMemberDataError(f"Jenis kelamin tidak valid. Pilihan: {', '.join(valid_genders)}")

        # Validasi alamat
        cleaned_address = address.strip()
        if not cleaned_address:
            raise InvalidMemberDataError("Alamat wajib diisi.")

        # Validasi no hp
        cleaned_phone = "".join(filter(str.isdigit, phone.strip()))
        if len(cleaned_phone) < 9 or len(cleaned_phone) > 15:
            raise InvalidMemberDataError("Nomor HP harus berupa angka valid (9 - 15 digit).")

        # Validasi paket
        valid_packages = [p.value for p in PackageType]
        if package not in valid_packages:
            raise InvalidMemberDataError(f"Paket tidak valid. Pilihan: {', '.join(valid_packages)}")

        # Tanggal registrasi & kedaluwarsa (1 bulan / 30 hari)
        reg_date = registration_date or date.today()
        exp_date = reg_date + timedelta(days=30)

        # ID Member
        member_id = custom_id.strip() if custom_id and custom_id.strip() else self.get_next_member_id()

        # Cek apakah ID sudah ada
        if self.member_repo.get_by_id(member_id):
            raise MemberAlreadyExistsError(f"Member dengan ID '{member_id}' sudah terdaftar.")

        # Kuota sesi: Class = 8 sesi, Open Gym = None (Unlimited)
        max_sess = 8 if package == PackageType.CLASS.value else None

        new_member = Member(
            id=member_id,
            full_name=cleaned_name,
            gender=gender,
            address=cleaned_address,
            phone=cleaned_phone,
            package=package,
            registration_date=reg_date,
            expiry_date=exp_date,
            sessions_used=0,
            max_sessions=max_sess,
        )

        return self.member_repo.add(new_member)

    def record_attendance(self, member_id: str, current_dt: Optional[datetime] = None) -> tuple[Member, Attendance]:
        """
        Mencatat kehadiran member berdasarkan ID.
        Aturan:
        1. ID harus terdaftar.
        2. Member harus berstatus Active (belum kedaluwarsa).
        3. Khusus Member Class: Batas maksimal absensi adalah 8 sesi dalam 1 bulan.
        4. Member hanya dapat absen 1 kali per hari. Jika sudah absen hari ini, ditolak.
        """
        mid = member_id.strip()
        if not mid:
            raise InvalidMemberDataError("Nomor ID member tidak boleh kosong.")

        member = self.member_repo.get_by_id(mid)
        if not member:
            raise MemberNotFoundError(f"Nomor ID '{mid}' tidak terdaftar sebagai member.")

        now = current_dt or datetime.now()
        today = now.date()

        # Cek status masa aktif waktu (1 bulan)
        if today > member.expiry_date:
            raise InvalidMemberDataError(
                f"Member '{member.full_name}' (ID: {member.id}) berstatus Non-Active "
                f"(masa aktif telah kedaluwarsa pada {member.expiry_date.strftime('%d %B %Y')}). "
                "Silakan perpanjang paket terlebih dahulu di panel Admin."
            )

        # Cek kuota sesi khusus Member Class (Maksimal 8x)
        if member.package == PackageType.CLASS.value and member.max_sessions is not None:
            if member.sessions_used >= member.max_sessions:
                raise ClassQuotaExceededError(
                    f"Member Class '{member.full_name}' (ID: {member.id}) telah mencapai BATAS MAKSIMAL ABSENSI "
                    f"({member.sessions_used}/{member.max_sessions} sesi latihan bersama Coach).\n"
                    "Kuota sesi bulan ini telah habis. Silakan perpanjang paket untuk mendapatkan 8 sesi baru."
                )

        # Cek apakah sudah absen hari ini (Rule: 1x absen per hari)
        existing = self.attendance_repo.get_attendance_for_member_on_date(member.id, today)
        if existing:
            time_str = existing.attendance_time.strftime("%H:%M:%S")
            raise MemberAlreadyCheckedInTodayError(
                f"Member '{member.full_name}' (ID: {member.id}) SUDAH melakukan absensi hari ini pada pukul {time_str}.\n"
                "Sesuai aturan gym, absensi hanya dapat dilakukan 1 kali per hari."
            )

        attendance = Attendance(
            member_id=member.id,
            attendance_date=today,
            attendance_time=now.time(),
        )

        recorded = self.attendance_repo.record_attendance(attendance)

        # Increment sesi terpakai di database & objek domain
        self.member_repo.increment_sessions_used(member.id)
        member.sessions_used += 1

        return member, recorded

    def get_member_attendance_calendar(self, member_id: str, year: int, month: int) -> dict:
        """
        Mengambil data kalender absensi member untuk bulan dan tahun yang ditentukan.
        Mengembalikan info member, daftar tanggal hadir, dan total kehadiran.
        """
        member = self.member_repo.get_by_id(member_id.strip())
        if not member:
            raise MemberNotFoundError(f"Member dengan ID '{member_id}' tidak ditemukan.")

        attended_days = self.attendance_repo.get_monthly_attendance_dates_for_member(member.id, year, month)
        return {
            "member": member,
            "year": year,
            "month": month,
            "attended_days": attended_days,
            "total_attended": len(attended_days),
        }

    def get_dashboard_analytics(self) -> dict:
        """
        Mengumpulkan metrik analitik pengunjung gym untuk visualisasi dashboard:
        - Total pengunjung hari ini
        - Tren kunjungan 7 hari terakhir
        - Rasio paket member (Open Gym vs Class)
        - Jam teramai (Peak Hours)
        - Member teraktif
        - Status keanggotaan (Active vs Non-Active)
        - Rata-rata kunjungan harian
        """
        all_members = self.member_repo.get_all()
        active_members = sum(1 for m in all_members if m.is_active())
        inactive_members = len(all_members) - active_members

        today_count = self.attendance_repo.get_today_attendance_count()
        trend = self.attendance_repo.get_daily_attendance_trend(days=7)
        pkg_dist = self.attendance_repo.get_package_attendance_distribution()
        peak_hours = self.attendance_repo.get_peak_hours_analysis()
        top_member = self.attendance_repo.get_top_attending_member()

        # Hitung rata-rata kunjungan mingguan
        total_week_visits = sum(item["count"] for item in trend)
        weekly_avg = round(total_week_visits / len(trend), 1) if trend else 0.0

        # Hitung rasio paket
        total_pkg_visits = pkg_dist.get("Open Gym", 0) + pkg_dist.get("Class", 0)
        open_gym_pct = round((pkg_dist.get("Open Gym", 0) / total_pkg_visits) * 100) if total_pkg_visits > 0 else 50
        class_pct = 100 - open_gym_pct if total_pkg_visits > 0 else 50

        return {
            "today_visitors": today_count,
            "total_members": len(all_members),
            "active_members": active_members,
            "inactive_members": inactive_members,
            "daily_trend": trend,
            "weekly_average": weekly_avg,
            "peak_hours": peak_hours,
            "top_member": top_member,
            "package_distribution": pkg_dist,
            "open_gym_pct": open_gym_pct,
            "class_pct": class_pct,
        }

    def extend_member_package(self, member_id: str, months: int = 1, reference_date: Optional[date] = None) -> Member:
        """
        Admin memperpanjang masa aktif paket member.
        Menambahkan 30 hari ke tanggal kedaluwarsa.
        """
        member = self.member_repo.get_by_id(member_id.strip())
        if not member:
            raise MemberNotFoundError(f"Member dengan ID '{member_id}' tidak ditemukan.")

        member.extend_package(months=months, reference_date=reference_date)
        self.member_repo.update_expiry(member.id, member.expiry_date)
        return member

    def delete_inactive_member(self, member_id: str, reference_date: Optional[date] = None) -> None:
        """
        Admin menghapus data member yang sudah tidak aktif (Rule 7).
        Jika member masih aktif, penghapusan ditolak.
        """
        member = self.member_repo.get_by_id(member_id.strip())
        if not member:
            raise MemberNotFoundError(f"Member dengan ID '{member_id}' tidak ditemukan.")

        ref = reference_date or date.today()
        if member.is_active(ref):
            raise MemberActiveCannotBeDeletedError(
                f"Member '{member.full_name}' (ID: {member.id}) masih berstatus ACTIVE (berlaku hingga {member.expiry_date}). "
                "Sesuai aturan keamanan data, hanya member berstatus Non-Active yang dapat dihapus."
            )

        self.member_repo.delete(member.id)

    def search_members(self, query: str = "") -> List[Member]:
        """Mencari data member berdasarkan nomor ID atau nama."""
        if not query or not query.strip():
            return self.member_repo.get_all()
        return self.member_repo.search(query.strip())

    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        """Mengambil data member by ID."""
        return self.member_repo.get_by_id(member_id.strip())

    def get_recent_attendances(self, limit: int = 30) -> List[dict]:
        """Mengambil riwayat absensi terbaru."""
        return self.attendance_repo.get_recent_attendances(limit=limit)
