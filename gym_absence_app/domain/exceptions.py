"""
Domain Exceptions - Gym Absence System
Mengikuti standar Clean Code: Custom Error Classes dengan penanganan semantik yang jelas.
"""

class GymAppException(Exception):
    """Base exception class for all domain-specific errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MemberNotFoundError(GymAppException):
    """Raised when a member ID or lookup fails to find an existing record."""
    pass


class MemberAlreadyCheckedInTodayError(GymAppException):
    """Raised when a member attempts to check in more than once on the same day."""
    pass


class ClassQuotaExceededError(GymAppException):
    """Raised when a Class member has reached the maximum 8 attendance sessions within their 1-month period."""
    pass


class MemberAlreadyExistsError(GymAppException):
    """Raised when attempting to insert a member with an existing ID."""
    pass


class MemberActiveCannotBeDeletedError(GymAppException):
    """Raised when trying to delete an active member (Rule 7: only inactive can be deleted)."""
    pass


class InvalidMemberDataError(GymAppException):
    """Raised when input validation for member data fails."""
    pass


class DatabaseError(GymAppException):
    """Raised when an infrastructure database error occurs."""
    pass
