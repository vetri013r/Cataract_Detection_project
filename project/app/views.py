from django.shortcuts import render,redirect
from django.conf import settings
from .forms import ImageUploadForm
from .models import ImageUpload
from PIL import Image
import os
import pickle
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
model1=pickle.load(open('mobile_model.pkl','rb'))
preprocess_input=pickle.load(open('preprocess.pkl','rb'))
# Create your views here.
# def index(request):
#     return render(request,'home.html')

def about(request):
    return render(request,'About.html')

def upload_image(request):
    if request.method=='POST':
        form=ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else :
        form =ImageUploadForm()
    return render(request,'home.html',{'form':form})

def get_last_uploaded_image_path():
    last_uploaded_image = ImageUpload.objects.latest('uploaded_at')
    if last_uploaded_image:
        # Construct the full path
        image_path = os.path.join(settings.MEDIA_ROOT, last_uploaded_image.image.name)
        return image_path
    return None
def Report(request):
    image_path = get_last_uploaded_image_path()
    image = load_img(image_path, target_size=(224, 224))
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    prediction = model1.predict(image)
    prediction = tf.nn.sigmoid(prediction)
    prediction = tf.where(prediction < 0.5, 0, 1)
    i=prediction.numpy()[0][0]
    return render(request,'Report.html',{'pred': i})
