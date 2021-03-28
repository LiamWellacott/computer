# computer

## set up

```
python3 -m venv ../venv/computer_env
source ../venv/computer_env/bin/activate
pip install -r requirements.txt

cd rasa
rasa train
cd ..

cd stt
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/models_0.9.tar.gz
tar xvfz models_0.9.tar.gz
rm models_0.9.tar.gz
cd ..
```

## run

```
# run rasa server 
cd rasa
rasa run

# run computer (from roots)
python ./computer.py -m ./models/deepspeech-0.9.3-models.pbmm -s ./models/deepspeech-0.9.3-models.scorer -v 0

