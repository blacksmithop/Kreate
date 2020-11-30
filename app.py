from PIL import Image, ImageOps
from flask import Flask, flash, request, redirect, render_template, send_file, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask_assets import Environment, Bundle
from io import BytesIO, StringIO


UPLOAD_FOLDER = 'static\\uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

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
            flash('❌ No file part', 'error')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('❌ No file selected', 'info')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            im = Image.open(BytesIO(file.read()))
            im = ImageOps.invert(image=im)
            im_out = BytesIO()
            im.save(im_out, 'JPEG')
            im_out.seek(0)
            flash("✅ Inverted image")
            return send_file(im_out, attachment_filename=f'invert_{filename}',
                             as_attachment=True, mimetype='image/jpeg')
        else:
            flash(f"❓ Only files of the type {', '.join(ALLOWED_EXTENSIONS)} are allowed", 'warning')
    return render_template('index.html')


@app.route('/facts')
def type_facts():
    return render_template('facts.html', value='there you go')


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return redirect(f'https://http.cat/{code}')


@app.errorhandler(500)
def page_not_found(e):
    flash('🛑 Unsupported operation', 'error')
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    flash('🚫 Endpoint does not exist', 'error')
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run()
