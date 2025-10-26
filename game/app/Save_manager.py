import sys, os, json, shutil, uuid, hashlib
from cryptography.fernet import Fernet
import base64

# ------------------------
# 🔹 ПУТИ
# ------------------------
def resource_path(relative_path):
    """Возвращает путь к ресурсу (работает и в exe, и при разработке)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_save_dir():
    """Путь к папке сохранений в AppData"""
    appdata = os.getenv("APPDATA")
    save_dir = os.path.join(appdata, "Dead_world")  # ← можно изменить имя
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def get_save_path():
    """Путь к зашифрованному файлу сейва"""
    return os.path.join(get_save_dir(), "save.dat")


# ------------------------
# 🔹 ГЕНЕРАЦИЯ УНИКАЛЬНОГО КЛЮЧА ДЛЯ ПК
# ------------------------
def generate_system_key():
    """
    Генерирует уникальный ключ для конкретного ПК
    на основе имени пользователя и UUID системы.
    """
    username = os.getenv("USERNAME", "UnknownUser")
    system_id = uuid.getnode()  # уникальный MAC/ID машины
    raw_key = f"{username}-{system_id}-Dead_world".encode("utf-8")

    # Хэш превращаем в 32-байтный ключ для Fernet
    key = hashlib.sha256(raw_key).digest()
    return Fernet(base64.urlsafe_b64encode(key[:32]))


# ------------------------
# 🔹 СОЗДАНИЕ SAVE, ЕСЛИ НЕТ
# ------------------------
def ensure_save_exists():
    """Если сейва нет — создаём его из шаблона (зашифрованный)"""
    save_path = get_save_path()
    cipher = generate_system_key()

    if not os.path.exists(save_path):
        try:
            # Загружаем шаблон save.json из ресурсов
            with open(resource_path("save.json"), "r", encoding="utf-8") as f:
                data = f.read()
            encrypted_data = cipher.encrypt(data.encode("utf-8"))
            with open(save_path, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            print("Не удалось создать зашифрованный save:", e)
    return save_path, cipher


# ------------------------
# 🔹 ЗАГРУЗКА SAVE
# ------------------------
def load_save():
    save_path, cipher = ensure_save_exists()
    with open(save_path, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
    return json.loads(decrypted_data)


# ------------------------
# 🔹 СОХРАНЕНИЕ SAVE
# ------------------------
def save_game(data):
    save_path, cipher = ensure_save_exists()
    json_data = json.dumps(data, indent=4)
    encrypted_data = cipher.encrypt(json_data.encode("utf-8"))
    with open(save_path, "wb") as f:
        f.write(encrypted_data)
