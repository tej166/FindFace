from flask import Flask, render_template, request, redirect, url_for
import face_recognition
import os

app = Flask(__name__)

# Dummy database for storing user data
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')    
 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form['user_type']
        users[username] = {'type': user_type}
        if user_type == "victim":
            return redirect(url_for('upload_image', username="VICTIM_"+ username))
        else:
           return redirect(url_for('upload_image', username=username)) 
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')    

@app.route('/upload_image/<username>', methods=['GET', 'POST'])
def upload_image(username):
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image_file = request.files['image']
        if image_file.filename == '':
            return redirect(request.url)
        if not username.startswith('VICTIM_'):
            image_path = f"uploads/{username}.png"
            image_file.save(image_path)
            return redirect(url_for('check_match', username=username))
        else:
            image_path = f"victim/{username}.png"
            image_file.save(image_path)
            return "Image Uploaded"
    return render_template('upload_image.html', username=username)      

@app.route('/check_match/<username>')
def check_match(username):
    user_type = users[username]['type']
    arr= os.listdir('victim/')
    for imageUrl in arr:
        train_image = 'victim/'+imageUrl
        train_img = face_recognition.load_image_file(train_image)
        train_encoding = face_recognition.face_encodings(train_img)[0]
        test_image = f"uploads/{username}.png"
        test_img = face_recognition.load_image_file(test_image)
        test_encoding = face_recognition.face_encodings(test_img)[0]
        result = face_recognition.compare_faces([train_encoding], test_encoding)
        if result[0]:
            return 'Match found'
    return 'No match found'

    if result[0]:
        return 'Match found'
    else:
        return 'No match found'

if __name__ == '__main__':
    app.run(debug=True)