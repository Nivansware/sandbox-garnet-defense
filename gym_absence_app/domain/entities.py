"""
Domain Entities and Value Objects
Mengikuti kaidah Domain-Driven Design Lite dan Clean Code (self-documenting, immutability di mana relevan).
"""
from dataclasses import dataclass
from datetime import date, time, timedelta
from enum import Enum
from typing import Optional


class Gender(str, Enum):
    MALE = "Laki-laki"
    FEMALE = "Perempuan"


class PackageType(str, Enum):
    OPEN_GYM = "Open Gym"
    CLASS = "Class"


class MemberStatus(str, Enum):
    ACTIVE = "Active"
    NON_ACTIVE = "Non-Active"


@dataclass
class Attendance:
    """Entitas pencatatan absensi harian member."""
    member_id: str
    attendance_date: date
    attendance_time: time
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "member_id": self.member_id,
            "attendance_date": self.attendance_date.isoformat(),
            "attendance_time": self.attendance_time.strftime("%H:%M:%S"),
        }


@dataclass
class Member:
    """
    Entitas Member Gym.
    Status dihitung dinamis berdasarkan:
    1. Masa aktif 1 bulan (30 hari) dari tanggal registrasi / perpanjangan.
    2. Paket Class: kuota maksimal 8x absensi (sesi coach). Jika 8 sesi habis, status menjadi Non-Active.
    3. Paket Open Gym: bebas absensi (maksimal 1x per hari) selama masa aktif 1 bulan.
    """
    id: str
    full_name: str
    gender: str
    address: str
    phone: str
    package: str
    registration_date: date
    expiry_date: date
    sessions_used: int = 0
    max_sessions: Optional[int] = None

    def __post_init__(self):
        # Set default max_sessions jika belum diset
        if self.max_sessions is None and self.package == PackageType.CLASS.value:
            self.max_sessions = 8

    def is_active(self, reference_date: Optional[date] = None) -> bool:
        """
        Status aktif jika:
        1. Tanggal referensi belum melampaui tanggal kedaluwarsa (1 bulan).
        2. Kuota sesi belum habis (khusus paket Class: maksimal 8 sesi).
        """
        ref = reference_date or date.today()
        time_valid = (ref <= self.expiry_date)
        quota_valid = True
        if self.max_sessions is not None:
            quota_valid = (self.sessions_used < self.max_sessions)
        return time_valid and quota_valid

    @property
    def is_time_expired(self) -> bool:
        return date.today() > self.expiry_date

    @property
    def is_quota_exceeded(self) -> bool:
        if self.max_sessions is not None:
            return self.sessions_used >= self.max_sessions
        return False

    @property
    def status_label(self) -> str:
        """Label status saat ini dengan keterangan kuota."""
        if not self.is_active():
            if self.is_quota_exceeded:
                return f"Non-Active (Kuota {self.max_sessions}/{self.max_sessions} Habis)"
            return "Non-Active (Kedaluwarsa)"
        if self.max_sessions is not None:
            return f"Active ({self.sessions_used}/{self.max_sessions} Sesi)"
        return "Active (Unlimited)"

    @property
    def quota_display(self) -> str:
        """Informasi kuota sesi untuk tampilan tabel/dialog."""
        if self.max_sessions is not None:
            sisa = max(0, self.max_sessions - self.sessions_used)
            return f"{self.sessions_used}/{self.max_sessions} Sesi (Sisa: {sisa})"
        return "Unlimited (1 Bulan)"

    def days_remaining(self, reference_date: Optional[date] = None) -> int:
        """Menghitung sisa hari masa aktif."""
        ref = reference_date or date.today()
        diff = (self.expiry_date - ref).days
        return max(0, diff)

    def extend_package(self, months: int = 1, reference_date: Optional[date] = None) -> None:
        """
        Admin memperpanjang masa aktif paket.
        - Memajukan expiry_date 30 hari.
        - Mereset kuota sesi terpakai (sessions_used = 0) untuk paket Class.
        """
        ref = reference_date or date.today()
        additional_days = 30 * months
        if date.today() <= self.expiry_date:
            self.expiry_date = self.expiry_date + timedelta(days=additional_days)
        else:
            self.expiry_date = ref + timedelta(days=additional_days)
        # Reset sesi saat perpanjangan
        self.sessions_used = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "gender": self.gender,
            "address": self.address,
            "phone": self.phone,
            "package": self.package,
            "registration_date": self.registration_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat(),
            "sessions_used": self.sessions_used,
            "max_sessions": self.max_sessions,
            "status": self.status_label,
            "quota_display": self.quota_display,
            "days_remaining": self.days_remaining(),
        }
