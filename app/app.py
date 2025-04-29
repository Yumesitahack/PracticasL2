import os
from flask import Flask, request, render_template

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def count_file_contents(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()
        num_lines = len(lines)
        num_words = len(content.split())
        num_chars = len(content)
    return content, num_lines, num_words, num_chars

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
       
        content, num_lines, num_words, num_chars = count_file_contents(file_path)

       
        return (f'<h2>Contenido del archivo: {file.filename}</h2>'
                f'<pre>{content}</pre>'
                f'<h3>Datos del archivo:</h3>'
                f'<p>Número de líneas: {num_lines}</p>' 
                f'<p>Número de palabras: {num_words}</p>' 
                f'<p>Número de caracteres: {num_chars}</p>')
        
if __name__ == '__main__':
    app.run(debug=True)
