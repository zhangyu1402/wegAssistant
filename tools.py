def s_to_i(s: str):
    if s is None:
        return None
    try:
        return int(s)
    except Exception:
        ss = s.split(" ")
        try:
            return int(ss[0])
        except Exception:
            return None
