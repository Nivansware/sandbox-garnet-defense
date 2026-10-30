"""
Unit Test Suite - Gym Absence System
Mengikuti metodologi TDD & Extreme Agile Autonomy Doktrin AI Garnet.
Menguji 100% logika bisnis: registrasi, format ID, validasi, absensi, perpanjangan, penghapusan, pencarian.
"""
import os
import unittest
from datetime import date, datetime, time, timedelta
from domain.entities import Member, Attendance, PackageType, Gender, MemberStatus
from domain.exceptions import (
    MemberNotFoundError,
    MemberAlreadyExistsError,
    MemberAlreadyCheckedInTodayError,
    ClassQuotaExceededError,
    MemberActiveCannotBeDeletedError,
    InvalidMemberDataError,
)
from infrastructure.database import DatabaseManager
from infrastructure.repository import SQLiteMemberRepository, SQLiteAttendanceRepository
from application.services import GymService


class TestGymAbsenceSystem(unittest.TestCase):
    """Test suite komprehensif untuk validasi spesifikasi GYM-Absence-member.md."""

    TEST_DB = "test_gym_absence.db"

    def setUp(self):
        """Inisialisasi database test yang terisolasi."""
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)
        self.db_manager = DatabaseManager(self.TEST_DB)
        self.member_repo = SQLiteMemberRepository(self.db_manager)
        self.attendance_repo = SQLiteAttendanceRepository(self.db_manager)
        self.service = GymService(self.member_repo, self.attendance_repo)

    def tearDown(self):
        """Pembersihan database test."""
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_member_id_formatting_sequence(self):
        """
        Memverifikasi aturan penomoran ID Member:
        Mulai dari 001, jika masuk 999 maka selanjutnya 1000.
        """
        # Awal harus 001
        self.assertEqual(self.service.get_next_member_id(), "001")

        # Daftarkan member 001
        m1 = self.service.register_member(
            full_name="Budi Santoso",
            gender="Laki-laki",
            address="Jl. Sudirman 10",
            phone="081234567890",
            package="Open Gym"
        )
        self.assertEqual(m1.id, "001")
        self.assertEqual(self.service.get_next_member_id(), "002")

        # Daftarkan member dengan ID 999 manual
        m_999 = self.service.register_member(
            full_name="Siti Rahma",
            gender="Perempuan",
            address="Jl. Melati 5",
            phone="081298765432",
            package="Class",
            custom_id="999"
        )
        self.assertEqual(m_999.id, "999")

        # ID berikutnya setelah 999 harus 1000
        self.assertEqual(self.service.get_next_member_id(), "1000")

        # Daftarkan member 1000
        m_1000 = self.service.register_member(
            full_name="Agus Wijaya",
            gender="Laki-laki",
            address="Jl. Merdeka 1",
            phone="081311223344",
            package="Open Gym"
        )
        self.assertEqual(m_1000.id, "1000")
        self.assertEqual(self.service.get_next_member_id(), "1001")

    def test_member_registration_and_status(self):
        """
        Memverifikasi:
        - Biodata lengkap tersimpan.
        - Status Active jika tanggal daftar kurang dari 1 bulan.
        - Status Non-Active jika sudah melewati 1 bulan.
        """
        today = date(2026, 9, 8)
        member = self.service.register_member(
            full_name="Rian Pratama",
            gender="Laki-laki",
            address="Jl. Gatot Subroto No. 44",
            phone="085712345678",
            package="Open Gym",
            registration_date=today
        )

        self.assertEqual(member.id, "001")
        self.assertEqual(member.full_name, "Rian Pratama")
        self.assertEqual(member.package, "Open Gym")
        self.assertEqual(member.expiry_date, today + timedelta(days=30))

        # Cek status hari ini -> Active
        self.assertTrue(member.is_active(today))
        self.assertEqual(member.status_label, "Active")

        # Cek status 15 hari kemudian -> masih Active
        self.assertTrue(member.is_active(today + timedelta(days=15)))

        # Cek status 31 hari kemudian -> Non-Active
        future_date = today + timedelta(days=31)
        self.assertFalse(member.is_active(future_date))

    def test_registration_validation_errors(self):
        """Memverifikasi validasi input biodata member."""
        # Nama kosong
        with self.assertRaises(InvalidMemberDataError):
            self.service.register_member("", "Laki-laki", "Alamat", "08123456789", "Open Gym")

        # Gender tidak valid
        with self.assertRaises(InvalidMemberDataError):
            self.service.register_member("Doni", "Alien", "Alamat", "08123456789", "Open Gym")

        # HP tidak valid (huruf)
        with self.assertRaises(InvalidMemberDataError):
            self.service.register_member("Doni", "Laki-laki", "Alamat", "abc", "Open Gym")

        # Paket tidak valid
        with self.assertRaises(InvalidMemberDataError):
            self.service.register_member("Doni", "Laki-laki", "Alamat", "08123456789", "VIP Platinum")

    def test_attendance_success(self):
        """Memverifikasi kehadiran member aktif berhasil dicatat."""
        member = self.service.register_member(
            full_name="Lisa Permata",
            gender="Perempuan",
            address="Jl. Diponegoro",
            phone="081987654321",
            package="Class"
        )

        check_in_time = datetime(2026, 9, 8, 9, 30, 0)
        ret_member, attendance = self.service.record_attendance(member.id, current_dt=check_in_time)

        self.assertEqual(ret_member.id, member.id)
        self.assertEqual(attendance.member_id, member.id)
        self.assertEqual(attendance.attendance_date, check_in_time.date())
        self.assertEqual(attendance.attendance_time, check_in_time.time())

        # Cek query riwayat absensi
        history = self.service.get_recent_attendances()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["member_id"], member.id)
        self.assertEqual(history[0]["full_name"], "Lisa Permata")

    def test_attendance_fails_for_inactive_member(self):
        """Memverifikasi member yang sudah expired (Non-Active) tidak bisa absen."""
        past_date = date(2026, 1, 1)
        member = self.service.register_member(
            full_name="Eko Kadaluarsa",
            gender="Laki-laki",
            address="Jl. Lawu",
            phone="081211112222",
            package="Open Gym",
            registration_date=past_date
        )

        today = datetime(2026, 9, 8, 10, 0, 0)
        with self.assertRaises(InvalidMemberDataError) as ctx:
            self.service.record_attendance(member.id, current_dt=today)
        self.assertIn("Non-Active", str(ctx.exception))

    def test_attendance_fails_for_unknown_id(self):
        """Memverifikasi absensi gagal jika ID tidak terdaftar."""
        with self.assertRaises(MemberNotFoundError):
            self.service.record_attendance("99999")

    def test_attendance_fails_if_already_checked_in_today(self):
        """
        Memverifikasi aturan 1x absensi per hari:
        Jika member sudah absen hari ini, maka absensi berikutnya di hari yang sama harus ditolak.
        """
        member = self.service.register_member(
            full_name="Kevin Sanjaya",
            gender="Laki-laki",
            address="Jl. Gelora 12",
            phone="081234445555",
            package="Open Gym"
        )

        time_morning = datetime(2026, 9, 8, 8, 30, 0)
        # Absen pertama hari ini -> Berhasil
        ret_member, att = self.service.record_attendance(member.id, current_dt=time_morning)
        self.assertEqual(ret_member.id, member.id)

        # Absen kedua di hari yang sama -> Harus DITOLAK
        time_afternoon = datetime(2026, 9, 8, 15, 0, 0)
        with self.assertRaises(MemberAlreadyCheckedInTodayError) as ctx:
            self.service.record_attendance(member.id, current_dt=time_afternoon)
        self.assertIn("SUDAH melakukan absensi hari ini", str(ctx.exception))

    def test_get_member_attendance_calendar(self):
        """Memverifikasi pengambilan data kalender absensi bulanan member."""
        member = self.service.register_member(
            full_name="Siti Nurhaliza",
            gender="Perempuan",
            address="Jl. Melati 3",
            phone="085711223344",
            package="Class"
        )

        # Catat absensi pada beberapa hari di bulan September 2026
        self.service.record_attendance(member.id, current_dt=datetime(2026, 9, 2, 9, 0, 0))
        self.service.record_attendance(member.id, current_dt=datetime(2026, 9, 5, 10, 15, 0))
        self.service.record_attendance(member.id, current_dt=datetime(2026, 9, 8, 16, 45, 0))

        cal_data = self.service.get_member_attendance_calendar(member.id, year=2026, month=9)

        self.assertEqual(cal_data["member"].id, member.id)
        self.assertEqual(cal_data["year"], 2026)
        self.assertEqual(cal_data["month"], 9)
        self.assertEqual(cal_data["total_attended"], 3)
        self.assertIn(2, cal_data["attended_days"])
        self.assertIn(5, cal_data["attended_days"])
        self.assertIn(8, cal_data["attended_days"])
        self.assertEqual(cal_data["attended_days"][2], "09:00:00")

    def test_class_package_8_sessions_limit_and_reset(self):
        """
        Memverifikasi aturan paket Class:
        1. Kuota awal = 8 sesi.
        2. Setiap absensi menambah sesi terpakai.
        3. Absensi ke-9 ditolak dengan ClassQuotaExceededError.
        4. Setelah diperpanjang oleh admin, kuota kembali di-reset ke 8 sesi baru.
        """
        member = self.service.register_member(
            full_name="Dewi Sartika",
            gender="Perempuan",
            address="Jl. Juanda 45",
            phone="081900112233",
            package="Class"
        )
        self.assertEqual(member.max_sessions, 8)
        self.assertEqual(member.sessions_used, 0)

        # Lakukan absensi selama 8 hari berturut-turut
        start_date = date(2026, 9, 1)
        for day_offset in range(8):
            dt = datetime.combine(start_date + timedelta(days=day_offset), time(9, 0))
            m_res, _ = self.service.record_attendance(member.id, current_dt=dt)
            self.assertEqual(m_res.sessions_used, day_offset + 1)

        # Cek data member setelah 8 sesi
        updated_m = self.service.get_member_by_id(member.id)
        self.assertEqual(updated_m.sessions_used, 8)
        self.assertFalse(updated_m.is_active())
        self.assertIn("Kuota 8/8 Habis", updated_m.status_label)

        # Absensi ke-9 pada hari berikutnya harus DITOLAK
        day_9 = datetime.combine(start_date + timedelta(days=8), time(9, 0))
        with self.assertRaises(ClassQuotaExceededError) as ctx:
            self.service.record_attendance(member.id, current_dt=day_9)
        self.assertIn("BATAS MAKSIMAL ABSENSI", str(ctx.exception))

        # Admin memperpanjang paket Class -> Sesi di-reset ke 0 dan masa aktif ditambah 30 hari
        renewed_m = self.service.extend_member_package(member.id, months=1)
        self.assertEqual(renewed_m.sessions_used, 0)
        self.assertTrue(renewed_m.is_active())

        # Sekarang member bisa absen kembali untuk sesi ke-1 di periode baru
        m_after_renew, _ = self.service.record_attendance(member.id, current_dt=day_9)
        self.assertEqual(m_after_renew.sessions_used, 1)

    def test_admin_extend_package(self):
        """Memverifikasi admin bisa memperpanjang masa aktif paket."""
        past_date = date(2026, 1, 1)
        member = self.service.register_member(
            full_name="Bambang Sukses",
            gender="Laki-laki",
            address="Jl. Kenanga",
            phone="081233445566",
            package="Open Gym",
            registration_date=past_date
        )

        today = date(2026, 9, 8)
        self.assertFalse(member.is_active(today))

        # Admin memperpanjang paket
        updated_member = self.service.extend_member_package(member.id, months=1, reference_date=today)

        # Status harus kembali Active, berlaku hingga today + 30 hari
        self.assertTrue(updated_member.is_active(today))
        self.assertEqual(updated_member.expiry_date, today + timedelta(days=30))

        # Member sekarang bisa absen kembali
        ret_member, att = self.service.record_attendance(member.id, current_dt=datetime(2026, 9, 8, 14, 0, 0))
        self.assertEqual(ret_member.id, member.id)

    def test_admin_delete_rules(self):
        """
        Memverifikasi aturan penghapusan (Rule 7):
        - Admin HANYA bisa menghapus data member yang SUDAH TIDAK AKTIF.
        - Member AKTIF dilarang keras dihapus.
        """
        today = date(2026, 9, 8)
        active_member = self.service.register_member(
            full_name="Active Boy",
            gender="Laki-laki",
            address="Jl. Sehat",
            phone="081299998888",
            package="Open Gym",
            registration_date=today
        )

        # Coba hapus member aktif -> harus DITOLAK
        with self.assertRaises(MemberActiveCannotBeDeletedError):
            self.service.delete_inactive_member(active_member.id, reference_date=today)

        # Buat member yang sudah kadaluarsa
        expired_member = self.service.register_member(
            full_name="Inactive Girl",
            gender="Perempuan",
            address="Jl. Santai",
            phone="081277776666",
            package="Class",
            registration_date=date(2026, 1, 1)
        )

        # Hapus member tidak aktif -> harus BERHASIL
        self.service.delete_inactive_member(expired_member.id, reference_date=today)

        # Verifikasi sudah terhapus
        self.assertIsNone(self.service.get_member_by_id(expired_member.id))

    def test_search_members_by_id_and_name(self):
        """Memverifikasi fitur pencarian berdasarkan ID dan Nama (Rule 8)."""
        self.service.register_member("Ahmad Fauzi", "Laki-laki", "Alamat 1", "08111111111", "Open Gym")
        self.service.register_member("Fauziah Zahra", "Perempuan", "Alamat 2", "08222222222", "Class")
        self.service.register_member("Budi Gunawan", "Laki-laki", "Alamat 3", "08333333333", "Open Gym")

        # Cari berdasarkan ID
        res_id = self.service.search_members("001")
        self.assertEqual(len(res_id), 1)
        self.assertEqual(res_id[0].full_name, "Ahmad Fauzi")

        # Cari berdasarkan nama keyword 'fauzi'
        res_name = self.service.search_members("fauzi")
        self.assertEqual(len(res_name), 2)

        # Cari nama yang tidak ada
        res_empty = self.service.search_members("XYZ999")
        self.assertEqual(len(res_empty), 0)

    def test_dashboard_analytics_aggregation(self):
        """Memverifikasi agregasi metrik dashboard dan grafik kunjungan."""
        m1 = self.service.register_member("Fitriani", "Perempuan", "Alamat 1", "081122334455", "Open Gym")
        m2 = self.service.register_member("Bagus", "Laki-laki", "Alamat 2", "081233445566", "Class")

        # Catat kunjungan
        today = datetime.now()
        self.service.record_attendance(m1.id, current_dt=today)

        analytics = self.service.get_dashboard_analytics()

        self.assertEqual(analytics["today_visitors"], 1)
        self.assertEqual(analytics["total_members"], 2)
        self.assertEqual(analytics["active_members"], 2)
        self.assertEqual(analytics["inactive_members"], 0)
        self.assertEqual(len(analytics["daily_trend"]), 7)
        self.assertIsNotNone(analytics["top_member"])
        self.assertEqual(analytics["top_member"]["name"], "Fitriani")
        self.assertGreaterEqual(analytics["open_gym_pct"], 0)


if __name__ == "__main__":
    unittest.main()
