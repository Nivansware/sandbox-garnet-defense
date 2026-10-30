"""
NIVANS GYM - Sistem Absensi & Manajemen Member
Entry Point Utama Aplikasi Desktop
Prinsip: Clean Code, Layered Architecture, Anti-AI Slop Aesthetic.
"""
import os
import sys

# Memastikan direktori root aplikasi berada di sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from presentation.app import create_app


def main():
    """Fungsi eksekusi utama aplikasi."""
    db_file_path = os.path.join(BASE_DIR, "gym_absence.db")
    app = create_app(db_path=db_file_path)
    app.mainloop()


if __name__ == "__main__":
    main()
