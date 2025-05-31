from PIL import Image
import imagehash
import os

# Ruta donde están las imágenes
folder_path = r"C:\Users\juant\OneDrive\Escritorio\Juan Diego\Universidad\Electiva 3\DataSet Aves\Pruebas"
hashes = {}  # Diccionario para almacenar el hash y la imagen más grande
similarity_threshold = 5  # Umbral de diferencia entre hashes (ajustable)

# Recorremos todas las imágenes en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith((".jpg", ".png", ".jpeg")):  # Filtrar solo imágenes
        img_path = os.path.join(folder_path, filename)  # Ruta completa de la imagen
        img = Image.open(img_path)  # Abrir la imagen con PIL
        hash_value = imagehash.phash(img)  # Calcular el hash perceptual
        img_size = img.size[0] * img.size[1]  # Calcular el tamaño (ancho × alto)

        # Buscar si hay imágenes similares ya almacenadas
        duplicate_found = False
        for stored_hash, stored_info in hashes.items():
            if hash_value - stored_hash <= similarity_threshold:  # Comparar con umbral
                stored_img_path, stored_size = stored_info

                if img_size > stored_size:  # Si la nueva imagen es más grande
                    os.remove(stored_img_path)  # Eliminar la imagen más pequeña
                    print(f"Eliminada: {os.path.basename(stored_img_path)} (manteniendo {filename})")
                    hashes[stored_hash] = (img_path, img_size)  # Guardar la imagen más grande
                else:
                    os.remove(img_path)  # Eliminar la nueva imagen porque es más pequeña
                    print(f"Eliminada: {filename} (manteniendo {os.path.basename(stored_img_path)})")
                
                duplicate_found = True
                break  # Detener la búsqueda una vez que se encuentra un duplicado

        if not duplicate_found:  # Si no se encontró un duplicado, almacenar la imagen
            hashes[hash_value] = (img_path, img_size)
