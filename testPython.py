

def func1():
    try:
        new_str = "Some STR"

        if str(new_str) != "Some STR":
            raise Exception("Mismatch")

    except Exception as e:
        raise Exception(f"This failed")