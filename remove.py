from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    try:
        input_image = Image.open(file.stream).convert("RGBA")
        input_image = input_image.resize((512, 512))  # reduce memory usage
        output_image = remove(input_image)

        buffer = io.BytesIO()
        output_image.save(buffer, format='PNG')
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png', download_name='cleaned.png')
    except Exception as e:
        return f"Error during processing: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env var
    app.run(host='0.0.0.0', port=port)
