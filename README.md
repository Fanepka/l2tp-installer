
# 🔒 VPN Auto-Installer for Windows

Автоматический установщик L2TP/IPsec VPN подключения для Windows с предустановленными параметрами.  
**Клиент специально разработан для сервера `l2tp.nl.plydev.ru`** 🚀

## 🌟 Особенности

- ⚡ Создает VPN подключение с типом L2TP/IPsec
- 🔧 Автоматически применяет необходимые настройки реестра
- 🔑 Сохраняет учетные данные для автоматического подключения
- 🤖 Не требует ввода данных пользователем (все параметры предустановлены)
- 🔄 Поддерживает автоматическую перезагрузку для применения изменений

## 📋 Требования

- ✔️ Windows 7/8/10/11
- ⚠️ Права администратора
- 💻 PowerShell 5.0+

## 🛠️ Установка

1. 📝 Замените в коде `ваш_логин` и `ваш_пароль` на реальные учетные данные
2. 🔄 Скомпилируйте скрипт в EXE:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico l2tp-installer.py
```

3. 🚀 Запустите полученный EXE-файл из папки `dist` с правами администратора

## ⚙️ Параметры подключения (предустановленные)

- 🌐 Сервер: `l2tp.nl.plydev.ru`
- 🔐 Тип VPN: L2TP/IPsec
- 🗝️ PSK ключ: `jyhkgfyig7895ertfgyh`
- 🔒 Аутентификация: MSChapv2

## ✅ После установки

- 📶 Подключение появится в списке сетевых адаптеров
- 💾 Учетные данные будут сохранены для автоматического подключения
- 🔄 Для применения всех изменений потребуется перезагрузка

## 📜 Лицензия

MIT License. Используйте на свой страх и риск.  

---

**ℹ️ Примечание**: Перед использованием в production среде проверьте скрипт в тестовом окружении.  
**👨‍💻 Разработано специально для сервера l2tp.nl.plydev.ru**  
**🐞 Багрепорты:** issues на GitHub  

[![GitHub stars](https://img.shields.io/github/stars/ваш_username/ваш_репозиторий?style=social)](https://github.com/Fanepka/l2tp-installer)
