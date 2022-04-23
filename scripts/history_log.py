from datetime import datetime
import os

def update_history(city):

  # prevent refresh page spam
  with open('logs/history.log', 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()

  # logs
  date = str(datetime.now())
  searched_for = city['city']
  temp = str(city['temp'])
  log_string = "[" + date + "] " + searched_for + " " + temp + "\n"

  if log_string.split(" ")[2] + temp != last_line.split(" ")[2] + temp:

    with open('logs/history.log', 'a', encoding='utf-8') as f:
      f.write(log_string)

def output_logs():
  temparr = []
  with open('logs/history.log') as f:
    for line in (f.readlines() [-5:]):
      temparr.append(line.strip().split(' '))
  return temparr