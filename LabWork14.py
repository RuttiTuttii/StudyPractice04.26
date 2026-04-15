import tkinter as tk
from tkinter import messagebox
from cefpython3 import cefpython as cef
import sys
import json
import os
import urllib.parse

# ----- работа с json -----

def load_users():
    """загружает список пользователей из users.json, если файла нет — возвращает пустой список"""
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_users(users):
    """сохраняет список пользователей в users.json"""
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_remembered():
    """загружает запомненные пароли (логин: пароль)"""
    if os.path.exists("remembered.json"):
        with open("remembered.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_remembered(remembered):
    """сохраняет запомненные пароли"""
    with open("remembered.json", "w", encoding="utf-8") as f:
        json.dump(remembered, f, indent=4, ensure_ascii=False)

# ----- python‑функции, вызываемые из javascript -----

def on_register(login, password, about, gender, continent):
    """регистрация нового пользователя, возвращает статус и сообщение"""
    users = load_users()
    # проверяем, не занят ли логин
    for u in users:
        if u["login"] == login:
            return {"ok": False, "msg": "логин уже занят"}
    # добавляем нового пользователя
    users.append({
        "login": login,
        "password": password,
        "about": about,
        "gender": gender,
        "continent": continent
    })
    save_users(users)
    return {"ok": True, "msg": "регистрация успешна! теперь войдите"}

def on_login(login, password, remember):
    """проверка логина и пароля, при remember=true сохраняет пароль"""
    users = load_users()
    for u in users:
        if u["login"] == login and u["password"] == password:
            if remember:
                remembered = load_remembered()
                remembered[login] = password
                save_remembered(remembered)
            else:
                # если галка снята, удаляем сохранённый пароль для этого логина
                remembered = load_remembered()
                if login in remembered:
                    del remembered[login]
                    save_remembered(remembered)
            return {"ok": True, "msg": f"добро пожаловать, {login}!"}
    return {"ok": False, "msg": "неверный логин или пароль"}

def get_remembered_password(login):
    """возвращает сохранённый пароль для логина (если есть)"""
    remembered = load_remembered()
    return remembered.get(login, "")

def update_variable_values(text_val, check_val, radio_val, *args):
    """для страницы переменных, *args игнорирует лишние параметры от cef"""
    return {
        "text": text_val,
        "checkbox": "да" if check_val else "нет",
        "radio": radio_val
    }

# ----- основное приложение -----

def main():
    sys.excepthook = cef.ExceptHook
    cef.Initialize()

    root = tk.Tk()
    root.title("лабораторная работа №14 — всё в одном")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")   # начальный цвет рамки (фона)

    # фрейм для браузера
    browser_frame = tk.Frame(root)
    browser_frame.pack(fill=tk.BOTH, expand=True)

    # создаём браузер внутри фрейма
    window_info = cef.WindowInfo()
    window_info.SetAsChild(browser_frame.winfo_id(), [0, 0, 800, 600])
    browser = cef.CreateBrowserSync(window_info, url="about:blank")

    # привязываем python‑функции к javascript
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetFunction("py_register", on_register)
    bindings.SetFunction("py_login", on_login)
    bindings.SetFunction("py_get_remembered", get_remembered_password)
    bindings.SetFunction("py_update_vars", update_variable_values)
    browser.SetJavascriptBindings(bindings)

    # ----- html‑код с тремя страницами и tailwind css -----
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #e9eef5 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 1rem;
            }
            .card {
                background: white;
                border-radius: 1.5rem;
                box-shadow: 0 20px 35px -10px rgba(0,0,0,0.15);
                width: 100%;
                max-width: 28rem;
                overflow: hidden;
                transition: transform 0.2s;
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                padding: 1rem;
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
            .pill {
                padding: 0.5rem 1.25rem;
                border-radius: 9999px;
                border: none;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                background: #e2e8f0;
                color: #1e293b;
            }
            .pill:hover {
                transform: translateY(-2px);
                filter: brightness(0.95);
            }
            .pill-blue {
                background: #3b82f6;
                color: white;
            }
            .pill-green {
                background: #10b981;
                color: white;
            }
            .pill-purple {
                background: #8b5cf6;
                color: white;
            }
            .page {
                padding: 1.5rem;
                animation: fadeIn 0.25s ease-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(8px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .hidden {
                display: none;
            }
            h2 {
                font-size: 1.5rem;
                font-weight: 600;
                text-align: center;
                color: #334155;
                margin-bottom: 1.25rem;
            }
            .field {
                margin-bottom: 1rem;
            }
            label {
                display: block;
                font-size: 0.85rem;
                font-weight: 500;
                color: #475569;
                margin-bottom: 0.25rem;
            }
            input, textarea, select {
                width: 100%;
                padding: 0.6rem 1rem;
                border: 1px solid #cbd5e1;
                border-radius: 9999px;
                font-size: 0.9rem;
                transition: all 0.2s;
                background: white;
            }
            textarea {
                border-radius: 1rem;
                resize: vertical;
            }
            input:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
                transform: scale(1.01);
            }
            .checkbox-group {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-top: 0.25rem;
            }
            .checkbox-group input {
                width: auto;
                margin-right: 0.25rem;
            }
            .radio-group {
                display: flex;
                gap: 1rem;
                margin-top: 0.25rem;
            }
            .radio-group label {
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                font-weight: normal;
                margin: 0;
            }
            .radio-group input {
                width: auto;
                margin: 0;
            }
            button {
                width: 100%;
                padding: 0.7rem;
                border: none;
                border-radius: 9999px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin-top: 0.5rem;
            }
            button:active {
                transform: scale(0.97);
            }
            .btn-login {
                background: #3b82f6;
                color: white;
            }
            .btn-login:hover {
                background: #2563eb;
                transform: translateY(-1px);
            }
            .btn-reg {
                background: #10b981;
                color: white;
            }
            .btn-reg:hover {
                background: #059669;
                transform: translateY(-1px);
            }
            .msg {
                text-align: center;
                font-size: 0.85rem;
                margin-top: 0.75rem;
                min-height: 2rem;
            }
            .text-green {
                color: #059669;
            }
            .text-red {
                color: #dc2626;
            }
            .var-display {
                background: #f1f5f9;
                border-radius: 1rem;
                padding: 1rem;
                text-align: center;
                margin-top: 1rem;
            }
            .var-display span:first-child {
                font-weight: 600;
                color: #334155;
            }
            .var-value {
                margin-top: 0.5rem;
                font-size: 0.85rem;
                color: #475569;
                word-break: break-word;
            }
            .hint {
                text-align: center;
                font-size: 0.7rem;
                color: #94a3b8;
                margin-top: 0.75rem;
            }
        </style>
        <script>
            function showPage(pageId) {
                document.getElementById('loginPage').classList.add('hidden');
                document.getElementById('registerPage').classList.add('hidden');
                document.getElementById('varsPage').classList.add('hidden');
                document.getElementById(pageId).classList.remove('hidden');
            }

            window.onload = function() {
                const loginInput = document.getElementById('login_username');
                const passInput = document.getElementById('login_password');
                const rememberCheck = document.getElementById('login_remember');
                
                if(loginInput) {
                    loginInput.addEventListener('change', function() {
                        const login = loginInput.value;
                        if(login) {
                            window.py_get_remembered(login, function(remPass) {
                                if(remPass) {
                                    passInput.value = remPass;
                                    rememberCheck.checked = true;
                                } else {
                                    passInput.value = '';
                                    rememberCheck.checked = false;
                                }
                            });
                        }
                    });
                }
                attachVarEvents();
                updateVarLabel();
            };

            function doLogin() {
                const login = document.getElementById('login_username').value.trim();
                const password = document.getElementById('login_password').value;
                const remember = document.getElementById('login_remember').checked;
                if(!login || !password) {
                    document.getElementById('login_msg').innerHTML = '<span class="text-red">заполните оба поля</span>';
                    return;
                }
                window.py_login(login, password, remember, function(response) {
                    if(response.ok) {
                        document.getElementById('login_msg').innerHTML = '<span class="text-green">' + response.msg + '</span>';
                        document.getElementById('login_username').value = '';
                        document.getElementById('login_password').value = '';
                    } else {
                        document.getElementById('login_msg').innerHTML = '<span class="text-red">' + response.msg + '</span>';
                    }
                });
            }

            function doRegister() {
                const login = document.getElementById('reg_login').value.trim();
                const password = document.getElementById('reg_password').value;
                const about = document.getElementById('reg_about').value;
                let gender = '';
                const genders = document.getElementsByName('gender');
                for(let g of genders) {
                    if(g.checked) gender = g.value;
                }
                const continent = document.getElementById('reg_continent').value;
                if(!login || !password) {
                    document.getElementById('reg_msg').innerHTML = '<span class="text-red">логин и пароль обязательны</span>';
                    return;
                }
                if(!gender) {
                    document.getElementById('reg_msg').innerHTML = '<span class="text-red">выберите пол</span>';
                    return;
                }
                window.py_register(login, password, about, gender, continent, function(response) {
                    if(response.ok) {
                        document.getElementById('reg_msg').innerHTML = '<span class="text-green">' + response.msg + '</span>';
                        document.getElementById('reg_login').value = '';
                        document.getElementById('reg_password').value = '';
                        document.getElementById('reg_about').value = '';
                        let checkedOne = document.querySelector('input[name="gender"]:checked');
                        if(checkedOne) checkedOne.checked = false;
                        document.getElementById('reg_continent').selectedIndex = 0;
                        setTimeout(() => showPage('loginPage'), 1500);
                    } else {
                        document.getElementById('reg_msg').innerHTML = '<span class="text-red">' + response.msg + '</span>';
                    }
                });
            }

            function attachVarEvents() {
                const textInput = document.getElementById('var_text');
                const checkBox = document.getElementById('var_check');
                const radioMale = document.getElementById('var_radio_male');
                const radioFemale = document.getElementById('var_radio_female');
                const radioOther = document.getElementById('var_radio_other');
                
                const update = () => updateVarLabel();
                if(textInput) textInput.addEventListener('input', update);
                if(checkBox) checkBox.addEventListener('change', update);
                if(radioMale) radioMale.addEventListener('change', update);
                if(radioFemale) radioFemale.addEventListener('change', update);
                if(radioOther) radioOther.addEventListener('change', update);
            }
            
            function updateVarLabel() {
                const textVal = document.getElementById('var_text').value;
                const checkVal = document.getElementById('var_check').checked;
                let radioVal = 'не выбран';
                if(document.getElementById('var_radio_male').checked) radioVal = 'мужской';
                if(document.getElementById('var_radio_female').checked) radioVal = 'женский';
                if(document.getElementById('var_radio_other').checked) radioVal = 'другой';
                
                window.py_update_vars(textVal, checkVal, radioVal, function(result) {
                    const label = `текст: ${result.text}, флажок: ${result.checkbox}, переключатель: ${result.radio}`;
                    document.getElementById('var_label').innerText = label;
                });
            }
        </script>
    </head>
    <body>
        <div class="card">
            <div class="nav">
                <button class="pill pill-blue" onclick="showPage('loginPage')">🔐 вход</button>
                <button class="pill pill-green" onclick="showPage('registerPage')">📝 регистрация</button>
                <button class="pill pill-purple" onclick="showPage('varsPage')">🎛️ переменные</button>
            </div>

            <div id="loginPage" class="page">
                <h2>авторизация</h2>
                <div class="field">
                    <label>логин</label>
                    <input type="text" id="login_username">
                </div>
                <div class="field">
                    <label>пароль</label>
                    <input type="password" id="login_password">
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="login_remember">
                    <label>запомнить пароль</label>
                </div>
                <button class="btn-login" onclick="doLogin()">войти</button>
                <div id="login_msg" class="msg"></div>
            </div>

            <div id="registerPage" class="page hidden">
                <h2>регистрация</h2>
                <div class="field">
                    <label>логин</label>
                    <input type="text" id="reg_login">
                </div>
                <div class="field">
                    <label>пароль</label>
                    <input type="password" id="reg_password">
                </div>
                <div class="field">
                    <label>о себе</label>
                    <textarea id="reg_about" rows="3"></textarea>
                </div>
                <div class="field">
                    <label>пол</label>
                    <div class="radio-group">
                        <label><input type="radio" name="gender" value="мужской"> мужской</label>
                        <label><input type="radio" name="gender" value="женский"> женский</label>
                        <label><input type="radio" name="gender" value="другой"> другой</label>
                    </div>
                </div>
                <div class="field">
                    <label>материк</label>
                    <select id="reg_continent">
                        <option value="евразия">евразия</option>
                        <option value="африка">африка</option>
                        <option value="северная америка">северная америка</option>
                        <option value="южная америка">южная америка</option>
                        <option value="австралия">австралия</option>
                        <option value="антарктида">антарктида</option>
                    </select>
                </div>
                <button class="btn-reg" onclick="doRegister()">зарегистрироваться</button>
                <div id="reg_msg" class="msg"></div>
            </div>

            <div id="varsPage" class="page hidden">
                <h2>связанные переменные</h2>
                <div class="field">
                    <label>поле ввода</label>
                    <input type="text" id="var_text" value="привет">
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="var_check">
                    <label>флажок (согласен)</label>
                </div>
                <div class="field">
                    <label>переключатель</label>
                    <div class="radio-group">
                        <label><input type="radio" name="var_radio" id="var_radio_male" value="мужской"> мужской</label>
                        <label><input type="radio" name="var_radio" id="var_radio_female" value="женский"> женский</label>
                        <label><input type="radio" name="var_radio" id="var_radio_other" value="другой"> другой</label>
                    </div>
                </div>
                <div class="var-display">
                    <span>значения через запятую:</span>
                    <div id="var_label" class="var-value">—</div>
                </div>
                <div class="hint">изменяй поля — метка обновляется автоматически</div>
            </div>
        </div>
    </body>
    </html>
    """

    # загружаем html в браузер
    html_encoded = "data:text/html," + urllib.parse.quote(html_content)
    browser.LoadUrl(html_encoded)

    # обработка изменения размера фрейма
    def on_configure(event):
        if browser:
            browser.NotifyMoveOrResizeStarted()
    browser_frame.bind("<Configure>", on_configure)

    # ----- меню (задание 5.4) -----
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # пункт color
    color_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Color", menu=color_menu, accelerator="Ctrl+C")
    def set_color(color):
        root.configure(bg=color)
        # также меняем фон фрейма для эстетики
        browser_frame.configure(bg=color)
    color_menu.add_command(label="Red", command=lambda: set_color("#ffcccc"), accelerator="Ctrl+R")
    color_menu.add_command(label="Green", command=lambda: set_color("#ccffcc"), accelerator="Ctrl+G")
    color_menu.add_command(label="Blue", command=lambda: set_color("#ccccff"), accelerator="Ctrl+B")

    # пункт size
    size_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Size", menu=size_menu, accelerator="Ctrl+S")
    def set_size(width, height):
        root.geometry(f"{width}x{height}")
        # уведомляем браузер о смене размера
        browser.NotifyMoveOrResizeStarted()
    size_menu.add_command(label="500x500", command=lambda: set_size(500, 500), accelerator="Ctrl+5")
    size_menu.add_command(label="700x400", command=lambda: set_size(700, 400), accelerator="Ctrl+7")

    # горячие клавиши для меню
    def on_key(event):
        if event.state & 0x4:  # ctrl
            if event.keysym.lower() == 'r':
                set_color("#ffcccc")
            elif event.keysym.lower() == 'g':
                set_color("#ccffcc")
            elif event.keysym.lower() == 'b':
                set_color("#ccccff")
            elif event.keysym == '5':
                set_size(500, 500)
            elif event.keysym == '7':
                set_size(700, 400)
    root.bind("<Control-Key>", on_key)

    # цикл cef
    def message_loop_work():
        cef.MessageLoopWork()
        root.after(10, message_loop_work)
    message_loop_work()

    # закрытие окна
    def on_closing():
        browser.CloseBrowser(True)
        cef.Shutdown()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()
