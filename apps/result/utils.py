def score_grade(score):
    if score <= 34:
        return "F9"
    elif score <= 44:
        return "P8"
    elif score <= 54:
        return "P7"
    elif score <= 59:
        return "C6"
    elif score <= 64:
        return "C5"
    elif score <=69:
        return "C4"
    elif score <= 74:
        return "C3"
    elif score <=79:
        return "D2"
    else:
        return "D1"
