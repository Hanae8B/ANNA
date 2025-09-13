# core/permissions.py

permissions = {}

def check_permission(action: str):
    """Return True/False/None if action has recurring permission."""
    return permissions.get(action)

def grant_permission(action: str, recurring: bool = False):
    permissions[action] = True if recurring else None

def revoke_permission(action: str):
    if action in permissions:
        del permissions[action]

def list_permissions():
    return permissions
