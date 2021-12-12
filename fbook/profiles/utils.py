import uuid

#generator do etykiety, każdy user powinien posiadać oryginalną nazwę w przypadku identycznego imienia i nazwiska
def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-','').lower()
    return code