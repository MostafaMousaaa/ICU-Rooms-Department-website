from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def test_form():
    if request.method == 'POST':
        form_data = {key: value for key, value in request.form.items()}
        files_data = {key: f"{request.files[key].filename} ({request.files[key].content_type})" 
                     for key in request.files if request.files[key].filename}
        
        return render_template_string('''
            <h1>Form Data Received:</h1>
            <h2>Form Fields:</h2>
            <pre>{{ form_data }}</pre>
            
            <h2>Files:</h2>
            <pre>{{ files_data }}</pre>
            
            <a href="{{ url_for('test_form') }}">Try Again</a>
        ''', form_data=form_data, files_data=files_data)
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Profile Form</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; }
                input, select, textarea { padding: 8px; width: 100%; }
                button { padding: 10px 20px; background: #0d6efd; color: white; border: none; cursor: pointer; }
                .card { border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <h1>Test Profile Form</h1>
            
            <div class="card">
                <h2>Patient Profile Form</h2>
                <form method="POST" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="first_name">First Name*:</label>
                        <input type="text" id="first_name" name="first_name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="last_name">Last Name*:</label>
                        <input type="text" id="last_name" name="last_name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="date_of_birth">Date of Birth*:</label>
                        <input type="date" id="date_of_birth" name="date_of_birth" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="gender">Gender*:</label>
                        <select id="gender" name="gender" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="blood_group">Blood Group:</label>
                        <select id="blood_group" name="blood_group">
                            <option value="">Select Blood Group</option>
                            <option value="A+">A+</option>
                            <option value="A-">A-</option>
                            <option value="B+">B+</option>
                            <option value="B-">B-</option>
                            <option value="AB+">AB+</option>
                            <option value="AB-">AB-</option>
                            <option value="O+">O+</option>
                            <option value="O-">O-</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number*:</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="address">Address:</label>
                        <textarea id="address" name="address" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="photo">Profile Photo:</label>
                        <input type="file" id="photo" name="photo" accept="image/*">
                    </div>
                    
                    <button type="submit">Submit Form</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
