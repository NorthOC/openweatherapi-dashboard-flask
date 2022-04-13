from datetime import datetime
import os

def log_user_action(user, action, city=None, updated_to=None):
  actions = ["refresh", "add", "update", "delete"]

  if action in actions:
    date = str(datetime.now())
    if action == "refresh":
      log_string = "[" + date + "] User " + user.username + " refreshed their dashboard\n"
    elif action == "add":
      log_string = "[" + date + "] User " + user.username + " added " + city.name +\
         ", " + city.country_code + " to their dashboard\n"
    elif action == "update":
      log_string = "[" + date + "] User " + user.username + " updated the city name of " + city.name +\
         " to " + updated_to + "\n"
    elif action == "delete":
      log_string = "[" + date + "] User " + user.username + " deleted city " +\
         city.name + " from their dashboard\n"

    with open('logs/user.log', 'a', encoding='utf-8') as f:
      f.write(log_string)