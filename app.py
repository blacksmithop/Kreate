from PIL import Image, ImageOps
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
from flask_assets import Environment, Bundle
from io import BytesIO, StringIO


UPLOAD_FOLDER = 'static\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', filters='pyscss', output='main.css')
assets.register('scss_all', scss)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            im = Image.open(BytesIO(file.read()))
            im = ImageOps.invert(image=im)
            im_out = BytesIO()
            im.save(im_out, 'JPEG')
            im_out.seek(0)
            return send_file(im_out, attachment_filename=f'invert_{filename}', as_attachment=True, mimetype='image/jpeg')
        else:
            flash(f"Only files of the type {', '.join(ALLOWED_EXTENSIONS)} are allowed")
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
