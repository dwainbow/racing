class Lap():
    def __init__(self, lap_number, lap_time):
        self.lap_number = lap_number
        self.lap_time = self.parse_lap_time(lap_time)
    
    def parse_lap_time(self, lap_time):
        minutes = lap_time // 60000
        seconds = (lap_time % 60000) // 1000
        milliseconds = lap_time % 1000
        return f"{minutes}:{seconds}.{milliseconds}"
    