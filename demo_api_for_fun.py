from flask import Flask, request, jsonify,send_file,render_template
import io
from diffusers import StableDiffusionPipeline
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer,VitsModel
import torch
from PIL import Image
import scipy

# init model and pipe
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe = pipe.to("cuda")

img2text_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
img2text_feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
img2text_tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

tts_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
img2text_model.to(device)
tts_model.to(device)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/methodList', methods=['get'])
def get_methods():
    method_dict = {"text2img":"/text2img",
                    "TTS":"/tts",
                   "img2sound":"/img2sound"}

    return jsonify(method_dict)

@app.route('/text2img', methods=['get'])
def text2img():
    try:
        prompt = request.args.get('prompt')

        image = pipe(prompt).images[0]

        image.save("text2img.png")
        return send_file("text2img.png", as_attachment=True, download_name='text2img.png',
                         mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tts', methods=['get'])
def myTTS():
    try:
        text = request.args.get('text')
        inputs = tts_tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = tts_model(**inputs.to(device)).waveform

        scipy.io.wavfile.write("tts.wav", rate=tts_model.config.sampling_rate, data=output[0].cpu().numpy())
        # return audio file
        return send_file("tts.wav", as_attachment=True, download_name='tts.wav',
                         mimetype='audio/wav')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/img2sound', methods=['POST'])
def caption_image():
    try:
        # get uploaded img file
        image_file = request.files['image']

        # read img and preproc
        image = Image.open(io.BytesIO(image_file.read()))
        images = []

        # img2text part
        if image.mode != "RGB":
            image = image.convert(mode="RGB")
        images.append(image)

        pixel_values = img2text_feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = img2text_model.generate(pixel_values)

        preds = img2text_tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]

        # TTS part
        inputs = tts_tokenizer(preds[0], return_tensors="pt")
        with torch.no_grad():
            output = tts_model(**inputs.to(device)).waveform

        scipy.io.wavfile.write("img2sound.wav", rate=tts_model.config.sampling_rate, data=output[0].cpu().numpy())
        # return audio file
        return send_file("img2sound.wav", as_attachment=True, download_name='img2sound.wav',
                         mimetype='audio/wav')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()