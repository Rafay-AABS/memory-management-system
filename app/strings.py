"""
String constants for the Memory Management System.
"""

# API Response Messages
API_SUCCESS = "Operation completed successfully"
API_ERROR = "An error occurred"
API_INVALID_INPUT = "Invalid input provided"
API_NOT_FOUND = "Resource not found"

# Intent Detection Messages
INTENT_DETECTED = "Intent detected: {}"
INTENT_NOT_FOUND = "Unable to detect intent"
INTENT_AMBIGUOUS = "Multiple intents detected, please clarify"

# Note Management Messages
NOTE_CREATED = "Note created successfully"
NOTE_UPDATED = "Note updated successfully"
NOTE_DELETED = "Note deleted successfully"
NOTE_NOT_FOUND = "Note not found"
NOTE_RETRIEVED = "Note retrieved successfully"

# Parser Messages
PARSE_SUCCESS = "Input parsed successfully"
PARSE_ERROR = "Error parsing input: {}"
PARSE_INVALID_FORMAT = "Invalid format provided"

# Composer Messages
COMPOSE_SUCCESS = "Response composed successfully"
COMPOSE_ERROR = "Error composing response: {}"

# Rephrase Messages
REPHRASE_SUCCESS = "Text rephrased successfully"
REPHRASE_ERROR = "Error rephrasing text: {}"

# Validation Messages
VALIDATION_REQUIRED_FIELD = "Required field missing: {}"
VALIDATION_INVALID_TYPE = "Invalid type for field: {}"
VALIDATION_OUT_OF_RANGE = "Value out of acceptable range: {}"

# Error Messages
ERROR_GENERIC = "An unexpected error occurred"
ERROR_DATABASE = "Database error: {}"
ERROR_CONNECTION = "Connection error: {}"
ERROR_TIMEOUT = "Operation timed out"
ERROR_PERMISSION = "Permission denied"

# Status Messages
STATUS_PROCESSING = "Processing request..."
STATUS_READY = "System ready"
STATUS_BUSY = "System busy, please wait"
STATUS_IDLE = "System idle"

# Log Messages
LOG_INFO = "INFO: {}"
LOG_WARNING = "WARNING: {}"
LOG_ERROR = "ERROR: {}"
LOG_DEBUG = "DEBUG: {}"
