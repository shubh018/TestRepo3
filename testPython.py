

def func1():
    try:
        new_str = "Some STR"

        if srt(new_str) != "Some STR":
            raise Excpetion("Mismatch")

    except Excpetion as e:
        raise Excpection(f"This failed")