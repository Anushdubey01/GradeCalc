from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_new_cgpa(data):
    current_cgpa = float(data['current_cgpa'])
    total_credits_completed = int(data['total_credits_completed'])
    total_credits_required = int(data['total_credits_required'])
    num_courses = int(data['num_courses'])

    grade_points = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5}
    total_credit_points_before = current_cgpa * total_credits_completed

    for i in range(num_courses):
        improved_grade = data.get(f'grade_{i + 1}', 'E')  # Default to 'E' if grade is not provided
        course_credits = int(data.get(f'credits_{i + 1}', 0))  # Default to 0 credits if not provided
        total_credit_points_before -= grade_points['E'] * course_credits
        total_credit_points_before += grade_points[improved_grade] * course_credits

    new_cgpa = total_credit_points_before / total_credits_completed
    new_cgpa = round(new_cgpa, 2)  # Round to two decimal places
    return new_cgpa

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_cgpa', methods=['POST'])
def calculate_cgpa():
    try:
        data = request.form

        # Validate input
        validate_input(data)

        new_cgpa = calculate_new_cgpa(data)
        return render_template('result.html', new_cgpa=new_cgpa, data=data)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('index.html', error_message=error_message)

def validate_input(data):
    for key in ['current_cgpa', 'total_credits_completed', 'total_credits_required', 'num_courses']:
        if key not in data or not data[key].strip():
            raise ValueError(f"{key} is required.")

        if not data[key].replace('.', '', 1).isdigit():
            raise ValueError(f"{key} should be a valid number.")

    for i in range(int(data['num_courses'])):
        grade_key = f'grade_{i + 1}'
        credits_key = f'credits_{i + 1}'

        if grade_key not in data or credits_key not in data:
            raise ValueError(f"Missing input for Course {i + 1}.")

        if data[credits_key].strip() and not data[credits_key].isdigit():
            raise ValueError(f"{credits_key} should be a valid number.")

if __name__ == '__main__':
    app.run(debug=True)
