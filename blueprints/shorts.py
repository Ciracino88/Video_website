from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from S3 import s3_class
from tqdm import tqdm
import os

shorts_bp = Blueprint('shorts', __name__)

@shorts_bp.route('/shorts', methods=["GET", "POST"])
def shorts():
    if request.method == 'POST':
        if (upload_file(request.files) != None):
            return redirect(url_for('shorts'))
    return render_template('shorts.html')

allowed_extensions = {'mp4', 'mov', 'avi'}
s3 = s3_class()


class Progress_percentage:
    def __init__(self, file_size):
        self.file_size = file_size
        self._seen_so_far = 0
        self._tqdm = tqdm(total=self.file_size, unit='B', unit_scale=True, desc='Upload progress')

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
        percentage = (self._seen_so_far / self.file_size) * 100
        print(f"upload progress: {percentage:.2f}%")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_file_to_s3(file, bucket, object_name=None):

    if object_name is None:
        object_name = file.filename

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    try:
        s3.inst.upload_fileobj(file, bucket, object_name, Callback=Progress_percentage(file_size))

        return f"https://{bucket}.s3.{s3.region_name}/{object_name}"

    except Exception as e:
        print(e)
        return None

def upload_file(files):
    if 'file' not in files:
        return None

    file = files['file']

    if file.filename == '':
        return None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        s3_url = upload_file_to_s3(file, s3.bucket_name, filename)

        if s3_url:
            return s3_url

        else:
            return None

    else:
        return None