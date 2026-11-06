import os
import shutil

mysql_path = r"C:\xampp\mysql"
data_path = os.path.join(mysql_path, "data")
backup_path = os.path.join(mysql_path, "backup")
data_old_path = os.path.join(mysql_path, "data_antigo")

if os.path.exists(data_old_path):
    shutil.rmtree(data_old_path, ignore_errors=True)

print("1. Renomeando pasta data para data_antigo...")
os.rename(data_path, data_old_path)

print("2. Criando nova pasta data...")
os.makedirs(data_path, exist_ok=True)

print("3. Copiando arquivos da pasta backup...")
for item in os.listdir(backup_path):
    s = os.path.join(backup_path, item)
    d = os.path.join(data_path, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print("4. Copiando ibdata1 de data_antigo...")
ibdata_old = os.path.join(data_old_path, "ibdata1")
if os.path.exists(ibdata_old):
    shutil.copy2(ibdata_old, os.path.join(data_path, "ibdata1"))
    print("ibdata1 copiado.")

# Copiar bancos de dados criados pelo usuário (se houver)
system_folders = {"mysql", "performance_schema", "phpmyadmin", "test"}
for item in os.listdir(data_old_path):
    s = os.path.join(data_old_path, item)
    if os.path.isdir(s) and item not in system_folders:
        d = os.path.join(data_path, item)
        shutil.copytree(s, d)
        print(f"Banco do usuario preservado: {item}")

print("Concluido com sucesso!")
