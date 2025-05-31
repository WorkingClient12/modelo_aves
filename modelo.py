# El modelo que utiliza es EfficientNetB0

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import os

# Parámetros
IMG_SIZE = (224, 224)  # EfficientNetB0 espera 224x224
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 3  # Cambia esto según tu dataset (por ejemplo: aves = 3 clases)

# Ruta a tus datos
train_dir = 'E:/Samuel/GitHub/modelo_aves/dataset/train'
val_dir = 'E:/Samuel/GitHub/modelo_aves/dataset/valid'

# Preprocesamiento de imágenes
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Cargar EfficientNetB0 sin la parte superior (top), congelado
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Congelamos capas base

# Construir el modelo
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compilar modelo
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar modelo
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# Guardar modelo
model.save('clasificador_aves_efficientnetb0.h5')
