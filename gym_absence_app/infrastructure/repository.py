"""
Repository Pattern Implementation
Memisahkan data access dari business logic sesuai prinsip Dependency Inversion dan Single Responsibility.
"""
from datetime import date, time
from typing import List, Optional
from domain.entities import Member, Attendance
from domain.exceptions import MemberAlreadyExistsError, MemberNotFoundError, DatabaseError
from infrastructure.database import DatabaseManager


class SQLiteMemberRepository:
    """Implementasi akses data Member dengan database SQLite."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_next_member_id(self) -> str:
        """
        Menghitung ID member berikutnya berdasarkan aturan:
        Mulai dari 001 sampai 999, lalu lanjut ke 1000, 1001, dst.
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT id FROM members;")
            rows = cursor.fetchall()
            max_num = 0
            for row in rows:
                raw_id = row["id"]
                if raw_id.isdigit():
                    val = int(raw_id)
                    if val > max_num:
                        max_num = val

            next_num = max_num + 1
            if next_num < 1000:
                return f"{next_num:03d}"
            return str(next_num)

    def add(self, member: Member) -> Member:
        """Menyimpan data member baru ke database."""
        sql = """
        INSERT INTO members (id, full_name, gender, address, phone, package, registration_date, expiry_date, sessions_used, max_sessions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with self.db.get_connection() as conn:
                conn.execute(sql, (
                    member.id,
                    member.full_name,
                    member.gender,
                    member.address,
                    member.phone,
                    member.package,
                    member.registration_date.isoformat(),
                    member.expiry_date.isoformat(),
                    member.sessions_used,
                    member.max_sessions,
                ))
            return member
        except DatabaseError as e:
            if "UNIQUE constraint failed" in str(e):
                raise MemberAlreadyExistsError(f"Member dengan ID '{member.id}' sudah terdaftar.") from e
            raise

    def get_by_id(self, member_id: str) -> Optional[Member]:
        """Mengambil data member berdasarkan ID."""
        sql = "SELECT * FROM members WHERE id = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (member_id.strip(),))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_member(row)

    def get_all(self) -> List[Member]:
        """Mengambil seluruh data member terurut berdasarkan ID."""
        sql = "SELECT * FROM members ORDER BY CAST(id AS INTEGER) ASC, id ASC;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql)
            return [self._row_to_member(row) for row in cursor.fetchall()]

    def search(self, keyword: str) -> List[Member]:
        """
        Mencari data member berdasarkan Nomor ID atau Nama Member.
        Case-insensitive & wildcard search.
        """
        kw = f"%{keyword.strip().lower()}%"
        sql = """
        SELECT * FROM members 
        WHERE LOWER(id) LIKE ? OR LOWER(full_name) LIKE ?
        ORDER BY CAST(id AS INTEGER) ASC, id ASC;
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (kw, kw))
            return [self._row_to_member(row) for row in cursor.fetchall()]

    def update_expiry(self, member_id: str, new_expiry_date: date) -> None:
        """Memperbarui tanggal kedaluwarsa member & mereset kuota sesi (perpanjangan paket)."""
        sql = "UPDATE members SET expiry_date = ?, sessions_used = 0 WHERE id = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (new_expiry_date.isoformat(), member_id))
            if cursor.rowcount == 0:
                raise MemberNotFoundError(f"Member dengan ID '{member_id}' tidak ditemukan.")

    def increment_sessions_used(self, member_id: str) -> None:
        """Menambah jumlah sesi absensi yang telah terpakai."""
        sql = "UPDATE members SET sessions_used = sessions_used + 1 WHERE id = ?;"
        with self.db.get_connection() as conn:
            conn.execute(sql, (member_id,))

    def delete(self, member_id: str) -> None:
        """Menghapus data member dari database."""
        sql = "DELETE FROM members WHERE id = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (member_id,))
            if cursor.rowcount == 0:
                raise MemberNotFoundError(f"Member dengan ID '{member_id}' tidak ditemukan.")

    @staticmethod
    def _row_to_member(row) -> Member:
        keys = row.keys()
        sessions = row["sessions_used"] if ("sessions_used" in keys and row["sessions_used"] is not None) else 0
        pkg = row["package"]
        if "max_sessions" in keys and row["max_sessions"] is not None:
            max_sess = row["max_sessions"]
        else:
            max_sess = 8 if pkg == "Class" else None

        return Member(
            id=row["id"],
            full_name=row["full_name"],
            gender=row["gender"],
            address=row["address"],
            phone=row["phone"],
            package=pkg,
            registration_date=date.fromisoformat(row["registration_date"]),
            expiry_date=date.fromisoformat(row["expiry_date"]),
            sessions_used=sessions,
            max_sessions=max_sess,
        )


class SQLiteAttendanceRepository:
    """Implementasi akses data Kehadiran / Absensi."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def record_attendance(self, attendance: Attendance) -> Attendance:
        """Mencatat kehadiran member."""
        sql = """
        INSERT INTO attendances (member_id, attendance_date, attendance_time)
        VALUES (?, ?, ?);
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (
                attendance.member_id,
                attendance.attendance_date.isoformat(),
                attendance.attendance_time.strftime("%H:%M:%S"),
            ))
            attendance.id = cursor.lastrowid
            return attendance

    def get_attendance_for_member_on_date(self, member_id: str, check_date: date) -> Optional[Attendance]:
        """Cek apakah member sudah pernah absen pada tanggal tertentu."""
        sql = "SELECT * FROM attendances WHERE member_id = ? AND attendance_date = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (member_id, check_date.isoformat()))
            row = cursor.fetchone()
            if not row:
                return None
            time_parts = [int(p) for p in row["attendance_time"].split(":")]
            return Attendance(
                id=row["id"],
                member_id=row["member_id"],
                attendance_date=date.fromisoformat(row["attendance_date"]),
                attendance_time=time(*time_parts),
            )

    def get_monthly_attendance_dates_for_member(self, member_id: str, year: int, month: int) -> dict[int, str]:
        """
        Mengambil tanggal dan jam absensi seorang member untuk bulan tertentu.
        Mengembalikan dictionary: {tanggal (int): 'HH:MM:SS'}.
        """
        prefix = f"{year:04d}-{month:02d}-%"
        sql = """
        SELECT attendance_date, attendance_time 
        FROM attendances 
        WHERE member_id = ? AND attendance_date LIKE ?
        ORDER BY attendance_date ASC;
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (member_id, prefix))
            records = {}
            for row in cursor.fetchall():
                att_date = date.fromisoformat(row["attendance_date"])
                records[att_date.day] = row["attendance_time"]
            return records

    def get_recent_attendances(self, limit: int = 50) -> List[dict]:
        """Mengambil riwayat absensi terbaru beserta nama member."""
        sql = """
        SELECT a.id, a.member_id, m.full_name, m.package, a.attendance_date, a.attendance_time
        FROM attendances a
        LEFT JOIN members m ON a.member_id = m.id
        ORDER BY a.attendance_date DESC, a.attendance_time DESC
        LIMIT ?;
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (limit,))
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "member_id": row["member_id"],
                    "full_name": row["full_name"] or "Unknown",
                    "package": row["package"] or "-",
                    "attendance_date": row["attendance_date"],
                    "attendance_time": row["attendance_time"],
                })
            return results

    def get_daily_attendance_trend(self, days: int = 7) -> List[dict]:
        """
        Mengambil tren absensi harian selama N hari terakhir.
        Mengembalikan list [{date: 'YYYY-MM-DD', day_name: 'Sen', count: N}].
        """
        from datetime import date, timedelta
        day_abbr = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
        today = date.today()
        dates = [today - timedelta(days=i) for i in reversed(range(days))]

        date_strings = [d.isoformat() for d in dates]
        placeholders = ",".join(["?"] * len(date_strings))
        sql = f"""
        SELECT attendance_date, COUNT(*) as visit_count
        FROM attendances
        WHERE attendance_date IN ({placeholders})
        GROUP BY attendance_date;
        """

        counts_map = {}
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, date_strings)
            for row in cursor.fetchall():
                counts_map[row["attendance_date"]] = row["visit_count"]

        trend = []
        for d in dates:
            iso = d.isoformat()
            trend.append({
                "date": iso,
                "display_date": d.strftime("%d/%m"),
                "day_name": day_abbr[d.weekday()],
                "count": counts_map.get(iso, 0)
            })
        return trend

    def get_package_attendance_distribution(self) -> dict:
        """Menghitung distribusi kehadiran berdasarkan paket member (Open Gym vs Class)."""
        sql = """
        SELECT m.package, COUNT(a.id) as count
        FROM attendances a
        JOIN members m ON a.member_id = m.id
        GROUP BY m.package;
        """
        dist = {"Open Gym": 0, "Class": 0}
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql)
            for row in cursor.fetchall():
                pkg = row["package"]
                if pkg in dist:
                    dist[pkg] = row["count"]
        return dist

    def get_peak_hours_analysis(self) -> str:
        """Menganalisis rentang jam kedatangan teramai."""
        sql = """
        SELECT SUBSTR(attendance_time, 1, 2) as hour_part, COUNT(*) as count
        FROM attendances
        GROUP BY hour_part
        ORDER BY count DESC
        LIMIT 1;
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql)
            row = cursor.fetchone()
            if not row or row["count"] == 0:
                return "Belum Ada Data"
            hour = int(row["hour_part"])
            return f"{hour:02d}:00 - {(hour + 1):02d}:00"

    def get_top_attending_member(self) -> Optional[dict]:
        """Mengambil member dengan kehadiran terbanyak."""
        sql = """
        SELECT m.id, m.full_name, m.package, COUNT(a.id) as total_visits
        FROM attendances a
        JOIN members m ON a.member_id = m.id
        GROUP BY a.member_id
        ORDER BY total_visits DESC
        LIMIT 1;
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql)
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "name": row["full_name"],
                "package": row["package"],
                "total_visits": row["total_visits"]
            }

    def get_today_attendance_count(self) -> int:
        """Menghitung jumlah pengunjung absensi hari ini."""
        from datetime import date
        today_iso = date.today().isoformat()
        sql = "SELECT COUNT(*) as count FROM attendances WHERE attendance_date = ?;"
        with self.db.get_connection() as conn:
            cursor = conn.execute(sql, (today_iso,))
            row = cursor.fetchone()
            return row["count"] if row else 0
