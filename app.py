from flask import Flask, request, render_template
import os  # For file path manipulation
import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'input' not in request.files:
            return render_template('index.html', output="") # Redirect to same page if no file
        # Save image
        file = request.files['input']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Use genai
        sample_file = genai.upload_file(path=filepath)
        os.remove(filepath)
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-002")
        text = "OCR this image"
        response = model.generate_content([text, sample_file])
        return render_template('index.html', output=response.text)

    # Render the form on GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)