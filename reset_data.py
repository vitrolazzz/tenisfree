import os
import shutil

mysql_path = r"C:\xampp\mysql"
data_path = os.path.join(mysql_path, "data")
backup_path = os.path.join(mysql_path, "backup")

# Remove tudo de data
for item in os.listdir(data_path):
    p = os.path.join(data_path, item)
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        try:
            os.remove(p)
        except Exception:
            pass

# Copia tudo de backup (novo, limpo)
for item in os.listdir(backup_path):
    s = os.path.join(backup_path, item)
    d = os.path.join(data_path, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print("Pasta data totalmente restaurada do backup (100% limpa)!")
