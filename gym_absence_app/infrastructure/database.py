"""
Database Infrastructure Layer
Mengelola koneksi SQLite, eksekusi query parameterized aman, dan inisialisasi skema.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from domain.exceptions import DatabaseError


class DatabaseManager:
    """Mengelola koneksi SQLite secara aman dan thread-safe."""

    def __init__(self, db_path: str = "gym_absence.db"):
        self.db_path = db_path
        self._ensure_directory()
        self.initialize_schema()

    def _ensure_directory(self) -> None:
        """Memastikan direktori file database tersedia."""
        db_file = Path(self.db_path)
        if db_file.parent and str(db_file.parent) != ".":
            db_file.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager untuk koneksi SQLite dengan auto-commit dan auto-rollback."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Terjadi kesalahan database SQLite: {str(e)}") from e
        finally:
            if conn:
                conn.close()

    def initialize_schema(self) -> None:
        """Membuat tabel members dan attendances jika belum ada."""
        schema_sql = """
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            package TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            sessions_used INTEGER DEFAULT 0,
            max_sessions INTEGER DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS attendances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            attendance_time TEXT NOT NULL,
            FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_members_name ON members(full_name);
        CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone);
        CREATE INDEX IF NOT EXISTS idx_attendances_member_date ON attendances(member_id, attendance_date);
        """
        with self.get_connection() as conn:
            conn.executescript(schema_sql)

            # Auto-migration: pastikan kolom baru ada jika database sudah ada sebelumnya
            cursor = conn.execute("PRAGMA table_info(members);")
            columns = [row["name"] for row in cursor.fetchall()]
            if "sessions_used" not in columns:
                conn.execute("ALTER TABLE members ADD COLUMN sessions_used INTEGER DEFAULT 0;")
            if "max_sessions" not in columns:
                conn.execute("ALTER TABLE members ADD COLUMN max_sessions INTEGER DEFAULT NULL;")
