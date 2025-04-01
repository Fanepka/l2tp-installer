import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox
import configparser

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_vpn_connection():
    try:
        server = "l2tp.nl.plydev.ru"
        psk = "jyhkgfyig7895ertfgyh"
        username = "test"
        password = "test" 

        # Удаляем существующее подключение (если есть)
        subprocess.run(['rasdial', server, '/DISCONNECT'], shell=True, check=False)
        subprocess.run(['rasphone', '-r', server], shell=True, check=False)
        
        # Создаем новое VPN подключение
        subprocess.run(
            f'powershell -command "Add-VpnConnection -Name \\"{server}\\" '
            f'-ServerAddress \\"{server}\\" -TunnelType L2tp '
            f'-EncryptionLevel Required -AuthenticationMethod MSChapv2 '
            f'-L2tpPsk \\"{psk}\\" -Force -RememberCredential"',
            shell=True, check=True
        )
        
        # Сохраняем учетные данные
        save_credentials(server, username, password)
        
        # Изменяем настройки реестра для L2TP
        subprocess.run(
            'REG ADD HKLM\\SYSTEM\\CurrentControlSet\\Services\\PolicyAgent '
            '/v AssumeUDPEncapsulationContextOnSendRule /t REG_DWORD /d 0x2 /f',
            shell=True, check=True
        )
        
        return True
    except Exception as e:
        print(f"Ошибка при создании подключения: {e}")
        return False

def save_credentials(server, username, password):
    """Надежное сохранение учетных данных"""
    try:
        # 1. Сохранение через rasphone
        pbk_path = os.path.join(
            os.environ['APPDATA'],
            'Microsoft',
            'Network',
            'Connections',
            'Pbk',
            'rasphone.pbk'
        )
        
        # Создаем директорию, если ее нет
        os.makedirs(os.path.dirname(pbk_path), exist_ok=True)
        
        # Записываем данные в файл телефонной книги
        config = configparser.ConfigParser()
        
        if os.path.exists(pbk_path):
            config.read(pbk_path)
        
        if server not in config.sections():
            config.add_section(server)
        
        config.set(server, 'MEDIA', 'rastapi')
        config.set(server, 'Port', 'VPN2-0')
        config.set(server, 'Device', 'WAN Miniport (IKEv2)')
        config.set(server, 'DEVICE', 'vpn')
        config.set(server, 'PhoneNumber', server)
        config.set(server, 'Credentials', server)
        config.set(server, 'UserName', username)
        config.set(server, 'Password', password)
        
        with open(pbk_path, 'w') as configfile:
            config.write(configfile)
        
        # 2. Дополнительное сохранение через PowerShell
        subprocess.run(
            f'powershell -command "$vpn = Get-VpnConnection -Name \\"{server}\\"; '
            f'$vpn.RememberCredential = $true; $vpn | Set-VpnConnection"',
            shell=True, check=True
        )
        
        # 3. Сохранение через cmdkey
        subprocess.run(
            f'cmdkey /generic:{server} /user:{username} /pass:{password}',
            shell=True, check=True
        )
        
    except Exception as e:
        print(f"Ошибка при сохранении учетных данных: {e}")

def reboot_computer():
    """Немедленная перезагрузка компьютера"""
    try:
        subprocess.run(['shutdown', '/r', '/t', '0'], shell=True)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось перезагрузить компьютер: {e}")

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    
    root = tk.Tk()
    root.withdraw()
    
    if create_vpn_connection():
        messagebox.showinfo(
            "Успех", 
            "VPN подключение успешно создано и настроено!\n\n"
            "Компьютер будет перезагружен для применения изменений."
        )
        reboot_computer()
    else:
        messagebox.showerror(
            "Ошибка", 
            "Не удалось создать VPN подключение.\n"
            "Проверьте:\n"
            "1. Подключение к интернету\n"
            "2. Антивирусное ПО\n"
            "3. Логи системы"
        )
    
    root.destroy()

if __name__ == "__main__":
    main()