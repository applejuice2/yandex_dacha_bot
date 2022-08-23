class Event:
    """Класс для описания мероприятия"""
    def __init__(self, name, date, time, genre, availabla_tickets):
        self.name = name
        self.date = date
        self.time = time
        self.genre = genre
        self.available_tickets = availabla_tickets
    
    def __repr__(self):
        return f'{self.name}{self.date}'
