
def agohuman( c, dt, precision=2, past_tense="{} ago", future_tense="in {}" ):
    import ago
    return ago.human( dt, precision, past_tense, future_tense )
