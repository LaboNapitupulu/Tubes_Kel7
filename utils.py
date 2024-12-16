def handle_error(func):
    try:
        func()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
