from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/'

@app.route('/')
def index():
    return render_template('openCVGUI.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
        print(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = cv2.imread(file_path)
        #resized_img = cv2.resize(img, (1050, 700))
        resized_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_' + filename)
        cv2.imwrite(resized_file_path, resized_img)
        return redirect(url_for('show_resized_image', filename='resized_' + filename))
    else:
        return redirect(url_for('index'))

@app.route('/show_resized_image/<filename>')
def show_resized_image(filename):
    return render_template('openCVGUI.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)