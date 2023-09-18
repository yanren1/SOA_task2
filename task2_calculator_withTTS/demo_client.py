from flask import Flask, render_template, request
from cal import calculate
from get_soap import getSoapN2wMethod

import torch
from transformers import AutoTokenizer,VitsModel
import scipy
from playsound import playsound
import os

tts_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tts_model.to(device)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def calculator():
    display = ""
    n2d = ""
    n2w = ""

    if request.method == 'POST':
        display = request.form['display']
        if display == 'Error':
            display = ''

        if 'digit' in request.form:
            if not display:
                display += request.form['digit']

            elif display[-1] in "+-*/^":
                display = request.form['display'].split(' ')
                display += [request.form['digit']]
                display = ' '.join(display)
            else:
                display = request.form['display'].split(' ')
                if request.form['digit'] == '.' and request.form['digit'] ==  display[-1][-1]:
                    display = ' '.join(display)
                else:
                    display[-1] += request.form['digit']
                    display = ' '.join(display)

        elif 'operation' in request.form:
            if not request.form['display']:
                display = ['0']
            else:
                display = request.form['display'].split(' ')

            if display[-1] not in "+-*/^" and display:
                display += [request.form['operation']]
            else:
                display = display[:-1] + [request.form['operation']]
            display = ' '.join(display)

        elif 'Del' in request.form:
            if not display:
                pass
            else:
                display = request.form['display'].split(' ')
                if display[-1] in "+-*/^":
                    display = display[:-1]
                else:
                    display[-1] = display[-1][:-1]
                display = ' '.join(display)

        elif 'calculate' in request.form:
            try:
                display = calculate(display)
                n2d = getSoapN2wMethod('NumberToDollars', display)
                n2w = getSoapN2wMethod('NumberToWords', display)

                inputs = tts_tokenizer("equals " + n2d, return_tensors="pt")
                with torch.no_grad():
                    output = tts_model(**inputs.to(device)).waveform

                scipy.io.wavfile.write("tts.wav", rate=tts_model.config.sampling_rate, data=output[0].cpu().numpy())

                playsound("tts.wav")
                os.unlink("tts.wav")

            except:
                display = 'Error'
                n2d = 'Error'
                n2w = 'Error'


        elif 'clear' in request.form:
            display = ''


    return render_template('calculator.html', display=display, n2d=n2d, n2w=n2w)

if __name__ == '__main__':
    app.run(debug=True)

