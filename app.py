from crypt import methods
import os
from flask import Flask, redirect, render_template, url_for, request, session, g

# db
from flask_sqlalchemy import SQLAlchemy

# custom functions
from city_search import find_city
from get_weather import get_weather_results
from get_coordinates import get_coordinates
from get_meteostat import get_meteostat_data_detailed
from history_log import update_history
from history_log import output_logs
from user_log import log_user_action
app = Flask(__name__)

# secret key needed for log in sessions
app.secret_key = '420blazeit420'

# sqlite
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# city table (association: user has many cities)
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    temp = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cities', lazy=True))
    
    def __repr__(self):
        return '<Category %r>' % self.name


# for logged in user session
@app.before_request
def before_request():
  
  g.user = None

  if 'user_id' in session:
    user = User.query.get(int(session['user_id']))
    g.user = user


#redirect root to /welcome
@app.route("/")
def redirect_page():
    return redirect(url_for("welcome"))


@app.route("/welcome/")
def welcome():
    return render_template("welcome.html")


#return welcome home or welcome back using same template.
@app.route("/welcome/home")
def welcome_home():
    return render_template("_welcome.html", value = "home")

@app.route("/welcome/back")
def welcome_back():
    return render_template("_welcome.html", value = "back")


#retrieve weather based on search and save state between searches
@app.route("/weather", methods=["POST", "GET"])
def weather():
  user = request.args.get("user_id")
  city_id = request.args.get("city_id")
  city_state = request.args.get("state")
  
  #when the weather.html form is submitted
  if request.method == "POST":

    city_search = request.form["city"]

    #for keeping state
    if city_id != None:
      found_city = get_weather_results(str(city_id))
    else:
      found_city = get_weather_results(str(3489854))
      
    #to stop humans from grabbing all the city.list.json (>200k) results
    if len(city_search) > 1:
      items = find_city(city_search)
    else:
      items = None

    return render_template("weather.html", 
    items = items, search = city_search, city=found_city, city_id = city_id, user=user)
  
  else:
    #for keeping state
    if city_id != None:
      found_city = get_weather_results(str(city_id))
      update_history(found_city)
    else:
      found_city = get_weather_results(str(3489854))
    found_city['state'] = city_state

    #args: items - cities matching search keyword, city_search - search query
    # found_city - API info about city, city_id - id from weather API
    return render_template("weather.html", 
    items = None, search = None, city=found_city, city_id = city_id, user=user)


@app.route("/weather_history")
def get_weather_history():
  city_name = request.args.get("name").replace('_', ' ')
  country = request.args.get("cont")
  state = request.args.get("state")
  #get coordinates
  found_city = get_coordinates(city_name, country, state)
  #meteostat data
  data_in_html = get_meteostat_data_detailed(found_city['city'], float(found_city['lat']), float(found_city['lon']))
  return render_template('weather_history.html', city = data_in_html)


# logs
@app.route("/log")
def get_log_history():
  search_history = output_logs()
  return render_template('log.html', logs = search_history)


# log in page
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    session.pop('user_id', None)

    username = request.form['username']
    password = request.form['password']
  
    user = [x for x in User.query.all() if x.username == username]
    if user:
      user = user[0]
      if user.password == password:
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))

    return redirect(url_for('login'))

  return render_template('login.html')

# logout
@app.route("/logout")
def logout():
  session.pop('user_id', None)
  return redirect(url_for('login'))

# user dashboard
@app.route("/dashboard")
def dashboard():
  if not g.user:
    return redirect(url_for('login'))
  return render_template('dashboard.html')

#view other user dashboards
@app.route("/cities/<username>")
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if g.user:
      if g.user.username == username:
        return render_template('dashboard.html')
    return render_template('user_cities.html', user=user)


# add city to dashboard
@app.route("/add")
def add_weather_to_dashboard():
  if g.user:
    city_id = request.args.get('id')
    user = User.query.filter_by(username=g.user.username).first_or_404()
    found_city = get_weather_results(str(city_id))
    city = City(city_id=str(city_id), name=found_city['city'], country_code=found_city['country_code'],
    temp=found_city['temp'], user=user)
    log_user_action(g.user, "add", city)
    db.session.add(city)
    db.session.commit()
  return redirect(url_for('dashboard'))


#loads the form for updating city name from dashboard
@app.route("/update", methods=["GET"])
def form_for_city_name():
  if g.user:
    id = request.args.get('id')
    city = City.query.filter_by(user_id=g.user.id).filter_by(id=id).first_or_404()
    return render_template('update_city_form.html', city=city)


# updates city name in dashboard
@app.route("/update", methods=["POST"])
def update_city_name():
  if g.user:
    city_id = request.args.get('id')
    city_name = request.form['cname']
    city = City.query.filter_by(id = city_id)
    log_user_action(g.user, "update", city[0], city_name)
    city.update({City.name: city_name})
    db.session.commit()
  return redirect(url_for('dashboard'))

# deletes an entry from the dashboard
@app.route("/delete")
def delete():
  if g.user:
    id = request.args.get('id')
    city = City.query.filter_by(id = id)
    log_user_action(g.user, "delete", city[0])
    city.delete()
    db.session.commit()
  return redirect(url_for('dashboard'))


# refresh dashboard temp
@app.route("/dashboard/refresh")
def refresh():
  if g.user:
    for item in g.user.cities:
      found_city = get_weather_results(item.city_id)
      temp = found_city['temp']
      City.query.filter_by(id = item.id).update({City.temp: temp})
    db.session.commit()
    log_user_action(g.user, "refresh")
  return redirect(url_for('dashboard'))

if __name__ == "__main__":
  app.run(debug=True, port=5000)