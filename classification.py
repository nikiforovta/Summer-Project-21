import numpy as np
from keras.models import load_model, Sequential
from keras.preprocessing.image import load_img, img_to_array

# Словарь вида "номер" : "порода" для интерпретации вывода модели
mapping = ['Affenpinscher', 'Afghan Hound', 'African Hunting Dog', 'Airedale', 'American Staffordshire Terrier',
           'Appenzeller', 'Australian Terrier', 'Basenji', 'Basset', 'Beagle', 'Bedlington Terrier',
           'Bernese Mountain Dog', 'Black-And-Tan Coonhound', 'Blenheim Spaniel', 'Bloodhound', 'Bluetick',
           'Border Collie', 'Border Terrier', 'Borzoi', 'Boston Bull', 'Bouvier Des Flandres', 'Boxer',
           'Brabancon Griffon', 'Briard', 'Brittany Spaniel', 'Bull Mastiff', 'Cairn', 'Cardigan',
           'Chesapeake Bay Retriever', 'Chihuahua', 'Chow', 'Clumber', 'Cocker Spaniel', 'Collie',
           'Curly-Coated Retriever', 'Dandie Dinmont', 'Dhole', 'Dingo', 'Doberman', 'English Foxhound',
           'English Setter', 'English Springer', 'Entlebucher', 'Eskimo Dog', 'Flat-Coated Retriever', 'French Bulldog',
           'German Shepherd', 'German Short-Haired Pointer', 'Giant Schnauzer', 'Golden Retriever', 'Gordon Setter',
           'Great Dane', 'Great Pyrenees', 'Greater Swiss Mountain Dog', 'Groenendael', 'Ibizan Hound', 'Irish Setter',
           'Irish Terrier', 'Irish Water Spaniel', 'Irish Wolfhound', 'Italian Greyhound', 'Japanese Spaniel',
           'Keeshond', 'Kelpie', 'Kerry Blue Terrier', 'Komondor', 'Kuvasz', 'Labrador Retriever', 'Lakeland Terrier',
           'Leonberg', 'Lhasa', 'Malamute', 'Malinois', 'Maltese Dog', 'Mexican Hairless', 'Miniature Pinscher',
           'Miniature Poodle', 'Miniature Schnauzer', 'Newfoundland', 'Norfolk Terrier', 'Norwegian Elkhound',
           'Norwich Terrier', 'Old English Sheepdog', 'Otterhound', 'Papillon', 'Pekinese', 'Pembroke', 'Pomeranian',
           'Pug', 'Redbone', 'Rhodesian Ridgeback', 'Rottweiler', 'Saint Bernard', 'Saluki', 'Samoyed', 'Schipperke',
           'Scotch Terrier', 'Scottish Deerhound', 'Sealyham Terrier', 'Shetland Sheepdog', 'Shih-Tzu',
           'Siberian Husky', 'Silky Terrier', 'Soft-Coated Wheaten Terrier', 'Staffordshire Bullterrier',
           'Standard Poodle', 'Standard Schnauzer', 'Sussex Spaniel', 'Tibetan Mastiff', 'Tibetan Terrier',
           'Toy Poodle', 'Toy Terrier', 'Vizsla', 'Walker Hound', 'Weimaraner', 'Welsh Springer Spaniel',
           'West Highland White Terrier', 'Whippet', 'Wire-Haired Fox Terrier', 'Yorkshire Terrier']

# Размер изображения для преобразования на вход модели
IM_SIZE = 150

# Глобальная инициализация модели
model = Sequential()


def init_classification():
    global model
    # Загрузка модели из файла, сохраненного в конце первой части проекта
    model = load_model("pretrained_dbc.h5", compile=False)


def classification(filename):
    # Преобразование входного изображения до необходимого размера
    img = load_img(filename, grayscale=False, color_mode='rgb', target_size=(IM_SIZE, IM_SIZE))
    # Нормализация изображения (переход от цвета в диапазоне [0,255] к диапазону [0,1])
    img_array = img_to_array(img) / 255
    # Словарь вида "порода" : "вероятность", полученный в результате работы модели
    return dict(zip(mapping, model.predict(np.expand_dims(img_array, axis=0))[0]))
