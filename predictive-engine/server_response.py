class Intention(object):
    name = ''
    prob = 0

class ChatRecognition(object):
    intention = Intention()
    context = []
    follwup = ''
    status = ''