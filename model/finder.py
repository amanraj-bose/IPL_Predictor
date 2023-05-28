def find_any(x, model:dict):
    x = str(x).lower()
    return [i for i, j in model.items() if str(i).startswith(x)]
