class TimeUtils:
  @staticmethod
  def convert_to_seconds(time_str):
      parts = time_str.split(':')
      minutes = int(parts[0])
      second = int(parts[1])
      seconds = minutes * 60 + second 
      return seconds

  @staticmethod
  def convert_to_hms(seconds):
      hours = seconds // 3600
      minutes = (seconds % 3600) // 60
      seconds = seconds % 60
      return f'{hours:02d}h:{minutes:02d}m:{seconds:02d}s'