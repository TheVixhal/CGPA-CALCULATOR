from flask import Flask, render_template, request

app = Flask(__name__)

# Function to convert percentage to CGPA grade points
def percentage_to_grade_point(percentage):
    return percentage / 9.5

# Function to calculate CGPA for the current semester
def calculate_cgpa(grades, credits):
    total_points = 0
    total_credits = 0
    
    for grade, credit in zip(grades, credits):
        total_points += grade * credit
        total_credits += credit
    
    cgpa = total_points / total_credits if total_credits != 0 else 0
    return round(cgpa, 2)

# Function to calculate overall CGPA
def calculate_overall_cgpa(previous_cgpa, previous_credits, current_grades, current_credits):
    current_cgpa = calculate_cgpa(current_grades, current_credits)
    
    previous_total_points = previous_cgpa * previous_credits
    current_total_points = sum(grade * credit for grade, credit in zip(current_grades, current_credits))
    
    overall_cgpa = (previous_total_points + current_total_points) / (previous_credits + sum(current_credits))
    return round(overall_cgpa, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    is_first_term = request.form['is_first_term']
    
    if is_first_term == 'no':
        previous_cgpa = float(request.form['previous_cgpa'])
        previous_credits = int(request.form['previous_credits'])
    else:
        previous_cgpa = 0
        previous_credits = 0

    num_subjects = int(request.form['num_subjects'])
    current_grades = []
    current_credits = []
    
    for i in range(num_subjects):
        percentage = float(request.form[f'percentage_{i+1}'])
        grade_point = percentage_to_grade_point(percentage)
        credit = int(request.form[f'credit_{i+1}'])
        current_grades.append(grade_point)
        current_credits.append(credit)

    if is_first_term == 'no':
        overall_cgpa = calculate_overall_cgpa(previous_cgpa, previous_credits, current_grades, current_credits)
        return render_template('result.html', overall_cgpa=overall_cgpa)
    else:
        current_cgpa = calculate_cgpa(current_grades, current_credits)
        return render_template('result.html', overall_cgpa=current_cgpa)

if __name__ == '__main__':
    app.run(debug=True)
