import re

with open('result_fc.txt', 'r') as f:
    lines = f.readlines()

time_pattern = re.compile(r'\d{1,2}:\d{2}')

times = [match.group() for line in lines for match in time_pattern.finditer(line)]

total_seconds = 0

for time in times:
    minutes, seconds = map(int, time.split(':'))
    total_seconds += minutes * 60 + seconds

hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

print(f"Total: {hours:02d}h:{minutes:02d}m:{seconds:02d}s")
