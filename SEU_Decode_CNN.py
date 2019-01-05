
import string

from keras.models import *
from keras.layers import *
import cv2

characters = string.digits
width, height, n_len, n_class = 210, 100, 4, len(characters)

def decode(y):
	y = np.argmax(np.array(y), axis=2)[:,0]
	return ''.join([characters[x] for x in y])

model = load_model('cnn.h5')

def SEU_Decode(SEU_Code):

    SEU_Grey = cv2.cvtColor(SEU_Code, cv2.COLOR_BGR2GRAY)
    cv2.threshold(SEU_Grey,255/2,255,cv2.THRESH_BINARY,SEU_Grey)
    SEU_Code_Reshape4D = np.array(SEU_Grey).reshape((1, height, width, 1))
    y_pred = model.predict(SEU_Code_Reshape4D)
    return decode(y_pred)

if __name__ == "__main__":
    print(SEU_Decode(cv2.imread('code.jpg')))