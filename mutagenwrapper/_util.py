def cutoff(s, length=120):
    """Cuts a given string if it is longer than a given length."""
    if length < 5:
        raise ValueError('length must be >= 5') 
    if len(s) <= length:
        return s
    else:
        i = (length - 2) / 2 
        j = (length - 3) / 2 
        return s[:i] + '...' + s[-j:]
