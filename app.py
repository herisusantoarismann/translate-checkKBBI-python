# import Library
from flask import Flask, render_template, request, redirect
from googletrans import Translator
from kbbi import KBBI, TidakDitemukan
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import auth

# inisialisasi Flask
app = Flask(__name__)
translator = Translator()
factory = StemmerFactory()
stemmer = factory.create_stemmer()
auth = auth.auth

def terjemah(kalimat):
    terjemahan = []
    translation = translator.translate(kalimat, src="id", dest="en")
    terjemahan = translation.text

    return terjemahan

def kbbi(kata):
    try:
        hasil = KBBI(kata, auth)
        hasil = hasil.__str__(contoh=False, terkait=False)
    except TidakDitemukan as e:
        hasil = e.objek
        hasil = {"hasil":hasil.saran_entri}

    return hasil

def stemming(kata):
    kata = stemmer.stem(kata)

    return kata

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    kalimat = request.form['kalimat']
    hasil_translate = terjemah(kalimat)
    return hasil_translate

@app.route('/kbbi', methods=['POST'])
def check():
    kata = request.form['kata']
    kata_stem = stemming(kata)
    arti = kbbi(kata_stem)
    return arti

if __name__ == "__main__":
    app.run(debug = True)
