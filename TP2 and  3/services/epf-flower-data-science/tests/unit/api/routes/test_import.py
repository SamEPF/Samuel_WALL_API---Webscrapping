try:
    import firebase_admin
    print("firebase_admin is installed and importable.")
except ModuleNotFoundError:
    print("firebase_admin is not installed.")