import string
import cv2
from keras.models import *
from keras.layers import *
import tensorflow as tf

characters = string.digits
print(characters)


width, height, n_len, n_class = 210, 100, 4, len(characters)
Path="E:/Python_Project/Python3.6/SEU_LES_CATCHER/TrainData/"

def decode(y):
    y = np.argmax(np.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])
def encode(str):
    labels =  np.zeros((n_len, n_class), dtype=np.uint8)
    for i,ch in enumerate(str):
        labels[i,:] = 0
        labels[i,characters.find(ch)] = 1
    return labels

def loadData(path,number):
    data =  np.empty((number,height,width),dtype=np.uint8)   #empty与ones差不多原理，但是数值随机，类型随后面设定
    labels =  np.zeros((n_len,number,n_class),dtype=np.uint8)
    listImg = os.listdir(path)
    count=0
    for img in listImg:
       imgData=cv2.imread(path+img, 0) #数据
       cv2.threshold(imgData,255/2,255,cv2.THRESH_BINARY,imgData)
       data[count,:,:] = np.asarray(imgData)   #将每个三维数组赋给data
       labels[:,count,:] =  encode(str(img)[0:n_len])   #取该图像的数值属性作为标签
       count=count+1
       if count>=number:
          break
    return data.reshape((number,height,width,1)), labels


TrainData,TrainLabels=loadData(Path,2005)
input_tensor = Input((height, width, 1))
x = input_tensor
for i in range(4):
    x = Convolution2D(32*2**i, 3, 3, activation='relu')(x)
    x = Convolution2D(32*2**i, 3, 3, activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dropout(0.4)(x)
x = [Dense(n_class, activation='softmax', name='c%d'%(i+1))(x) for i in range(4)]
model = Model(input=input_tensor, output=x)

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

config = tf.ConfigProto(allow_soft_placement=True)
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.per_process_gpu_memory_fraction = 0.80

config.gpu_options.allow_growth=True

run_options = tf.RunOptions(report_tensor_allocations_upon_oom = True)

model.fit(TrainData, {'c%d'%(i+1):TrainLabels[i] for i in range(n_len)}, batch_size=100,epochs=10,shuffle=True,verbose=1,validation_split=0.2)


model.save('CNN.h5')