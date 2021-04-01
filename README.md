# computer

## set up

```
python3 -m venv ../venv/computer_env
source ../venv/computer_env/bin/activate
# for some reason some of these failed to install, you may need to install dependencies manually with pip install ...
pip install -r requirements.txt

# opencv doesn't play nice with venv
sudo apt-get install python3-opencv
# update this with your python version
cp /usr/lib/python3/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so ../venv/computer_env/lib/python3.6/site-packages/

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

# run computer (from root)
python ./computer.py

