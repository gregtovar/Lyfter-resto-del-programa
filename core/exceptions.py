"""
Custom exception hierarchy for the Personal Finance Manager.

Keeping all business-logic exceptions in one place lets both the Console UI
and the GUI import a single module and decide, independently, how each error
should be displayed to the user.


All are dynamic values based on CSV file, nothing is hardcoded

"""


#
# Class definition
#
#
# As requested by LYFTER
#


class FinanceManagerError(Exception):
    """Base class for all application-specific errors."""


class ValidationError(FinanceManagerError):
    """Raised when user-supplied data fails a validation rule."""


class NotFoundError(FinanceManagerError):
    """Raised when a requested record (category, type, transaction) does not exist."""


class CategoryInUseError(FinanceManagerError):
    """Raised when trying to delete a category that is still referenced by transactions."""


class TypeInUseError(FinanceManagerError):
    """Raised when trying to delete a transaction type that is still referenced by transactions."""


class FileOperationError(FinanceManagerError):
    """Raised when a CSV file cannot be read or written safely."""
