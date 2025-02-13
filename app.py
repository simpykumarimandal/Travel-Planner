from flask import Flask, render_template, request, jsonify
from model import generate_travel_plan

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    destination = request.form['location']
    interest = request.form['interest']
    num_days = int(request.form['days'])
    budget = float(request.form['budget'])
    num_destinations_per_day = int(request.form['num_destinations_per_day'])

    travel_plan = generate_travel_plan(destination, num_days, budget, interest, num_destinations_per_day)
    
    return render_template('result.html', travel_plan=travel_plan)

if __name__ == '__main__':
    app.run(debug=True)
