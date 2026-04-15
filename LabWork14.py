import tkinter as tk
from tkinter import messagebox
from cefpython3 import cefpython as cef
import sys
import json
import os
import urllib.parse

# работа с базой данных (json)

def load_users():
    # грузим юзеров, если файла нет — отдаем пустой список
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_users(users):
    # сохраняем всю пачку юзеров обратно в файл
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_remembered():
    # подтягиваем сохраненные пароли
    if os.path.exists("remembered.json"):
        with open("remembered.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_remembered(remembered):
    # сохраняем данные для автозаполнения
    with open("remembered.json", "w", encoding="utf-8") as f:
        json.dump(remembered, f, indent=4, ensure_ascii=False)

# мост между python и javascript

def on_register(login, password, about, gender, continent, js_callback=None, *args):
    # регистрируем юзера, js_callback ловит ту самую функцию из браузера
    users = load_users()
    
    for u in users:
        if u["login"] == login:
            if js_callback:
                js_callback.Call({"ok": False, "msg": "логин уже занят"})
            return

    users.append({
        "login": login,
        "password": password,
        "about": about,
        "gender": gender,
        "continent": continent
    })
    save_users(users)
    
    if js_callback:
        js_callback.Call({"ok": True, "msg": "регистрация успешна! теперь войдите"})

def on_login(login, password, remember, js_callback=None, *args):
    # проверяем данные и сохраняем пароль, если стояла галочка
    users = load_users()
    for u in users:
        if u["login"] == login and u["password"] == password:
            remembered = load_remembered()
            if remember:
                remembered[login] = password
            else:
                if login in remembered:
                    del remembered[login]
            save_remembered(remembered)
            
            if js_callback:
                js_callback.Call({"ok": True, "msg": f"добро пожаловать, {login}!"})
            return
            
    if js_callback:
        js_callback.Call({"ok": False, "msg": "неверный логин или пароль"})

def get_remembered_password(login, js_callback=None, *args):
    # отдаем пароль для автозаполнения
    remembered = load_remembered()
    if js_callback:
        js_callback.Call(remembered.get(login, ""))

def update_variable_values(text_val, check_val, radio_val, js_callback=None, *args):
    # обновляем тестовые переменные на третьей вкладке
    data = {
        "text": text_val,
        "checkbox": "да" if check_val else "нет",
        "radio": radio_val
    }
    if js_callback:
        js_callback.Call(data)

# основной интерфейс и логика приложения

def main():
    sys.excepthook = cef.ExceptHook
    cef.Initialize()

    root = tk.Tk()
    root.title("лабораторная работа — монохром")
    root.geometry("800x600")
    root.configure(bg="#e5e5e5")

    # фрейм под браузер
    browser_frame = tk.Frame(root)
    browser_frame.pack(fill=tk.BOTH, expand=True)

    window_info = cef.WindowInfo()
    window_info.SetAsChild(browser_frame.winfo_id(), [0, 0, 800, 600])
    browser = cef.CreateBrowserSync(window_info, url="about:blank")

    # связываем функции
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetFunction("py_register", on_register)
    bindings.SetFunction("py_login", on_login)
    bindings.SetFunction("py_get_remembered", get_remembered_password)
    bindings.SetFunction("py_update_vars", update_variable_values)
    browser.SetJavascriptBindings(bindings)

    # html и css интерфейс
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: system-ui, -apple-system, sans-serif;
                background: #e5e5e5;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 1rem;
            }
            .card {
                background: #ffffff;
                border-radius: 1rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 24rem;
                overflow: hidden;
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                padding: 1rem;
                background: #f5f5f5;
                border-bottom: 1px solid #d4d4d4;
                flex-wrap: wrap;
            }
            .pill {
                padding: 0.5rem 1rem;
                border-radius: 99px;
                border: 1px solid #d4d4d4;
                font-size: 0.85rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
                background: #ffffff;
                color: #333333;
            }
            .pill:hover {
                background: #e5e5e5;
            }
            .pill.active {
                background: #333333;
                color: #ffffff;
                border-color: #333333;
            }
            .page {
                padding: 1.5rem;
                animation: fadeIn 0.2s ease-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .hidden {
                display: none;
            }
            h2 {
                font-size: 1.25rem;
                font-weight: 600;
                text-align: center;
                color: #1a1a1a;
                margin-bottom: 1.25rem;
            }
            .field {
                margin-bottom: 1rem;
            }
            label {
                display: block;
                font-size: 0.8rem;
                font-weight: 600;
                color: #666666;
                margin-bottom: 0.3rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            input[type="text"], input[type="password"], textarea, select {
                width: 100%;
                padding: 0.6rem;
                border: 1px solid #cccccc;
                border-radius: 0.5rem;
                font-size: 0.9rem;
                background: #fafafa;
                color: #1a1a1a;
                transition: border-color 0.2s;
            }
            input:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #666666;
                background: #ffffff;
            }
            textarea {
                resize: vertical;
            }
            .checkbox-group, .radio-group {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
            }
            .radio-group {
                flex-wrap: wrap;
                gap: 1rem;
            }
            .radio-group label, .checkbox-group label {
                font-weight: normal;
                text-transform: none;
                letter-spacing: normal;
                margin: 0;
                color: #333333;
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }
            button.btn-main {
                width: 100%;
                padding: 0.7rem;
                border: none;
                border-radius: 0.5rem;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                background: #1a1a1a;
                color: #ffffff;
                margin-top: 0.5rem;
            }
            button.btn-main:hover {
                background: #404040;
            }
            button.btn-main:active {
                transform: scale(0.98);
            }
            .msg {
                text-align: center;
                font-size: 0.85rem;
                margin-top: 1rem;
                min-height: 1.2rem;
                font-weight: 500;
            }
            .var-display {
                background: #f5f5f5;
                border: 1px solid #e5e5e5;
                border-radius: 0.5rem;
                padding: 1rem;
                text-align: center;
                margin-top: 1rem;
            }
            .var-display span:first-child {
                font-size: 0.8rem;
                color: #666666;
                text-transform: uppercase;
            }
            .var-value {
                margin-top: 0.5rem;
                font-size: 0.9rem;
                color: #1a1a1a;
                font-weight: 600;
            }
            .hint {
                text-align: center;
                font-size: 0.75rem;
                color: #999999;
                margin-top: 1rem;
            }
        </style>
        <script>
            function showPage(pageId, btnElement) {
                document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
                document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
                
                document.getElementById(pageId).classList.remove('hidden');
                if(btnElement) btnElement.classList.add('active');
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
                    document.getElementById('login_msg').innerText = 'заполните оба поля';
                    return;
                }
                window.py_login(login, password, remember, function(response) {
                    document.getElementById('login_msg').innerText = response.msg;
                    if(response.ok) {
                        document.getElementById('login_username').value = '';
                        document.getElementById('login_password').value = '';
                    }
                });
            }

            function doRegister() {
                const login = document.getElementById('reg_login').value.trim();
                const password = document.getElementById('reg_password').value;
                const about = document.getElementById('reg_about').value;
                const continent = document.getElementById('reg_continent').value;
                
                let gender = '';
                const genders = document.getElementsByName('gender');
                for(let g of genders) {
                    if(g.checked) gender = g.value;
                }
                
                if(!login || !password) {
                    document.getElementById('reg_msg').innerText = 'логин и пароль обязательны';
                    return;
                }
                if(!gender) {
                    document.getElementById('reg_msg').innerText = 'выберите пол';
                    return;
                }
                
                window.py_register(login, password, about, gender, continent, function(response) {
                    document.getElementById('reg_msg').innerText = response.msg;
                    if(response.ok) {
                        document.getElementById('reg_login').value = '';
                        document.getElementById('reg_password').value = '';
                        document.getElementById('reg_about').value = '';
                        document.getElementById('reg_continent').selectedIndex = 0;
                        document.querySelector('input[name="gender"]:checked').checked = false;
                        
                        setTimeout(() => {
                            document.getElementById('reg_msg').innerText = '';
                            showPage('loginPage', document.querySelector('.pill'));
                        }, 1500);
                    }
                });
            }

            function attachVarEvents() {
                const ids = ['var_text', 'var_check', 'var_radio_male', 'var_radio_female', 'var_radio_other'];
                ids.forEach(id => {
                    const el = document.getElementById(id);
                    if(el) el.addEventListener(el.type === 'text' ? 'input' : 'change', updateVarLabel);
                });
            }
            
            function updateVarLabel() {
                const textVal = document.getElementById('var_text').value;
                const checkVal = document.getElementById('var_check').checked;
                let radioVal = 'не выбран';
                if(document.getElementById('var_radio_male').checked) radioVal = 'мужской';
                if(document.getElementById('var_radio_female').checked) radioVal = 'женский';
                if(document.getElementById('var_radio_other').checked) radioVal = 'другой';
                
                window.py_update_vars(textVal, checkVal, radioVal, function(result) {
                    document.getElementById('var_label').innerText = 
                        `Текст: ${result.text} | Флажок: ${result.checkbox} | Радио: ${result.radio}`;
                });
            }
        </script>
    </head>
    <body>
        <div class="card">
            <div class="nav">
                <button class="pill active" onclick="showPage('loginPage', this)">вход</button>
                <button class="pill" onclick="showPage('registerPage', this)">регистрация</button>
                <button class="pill" onclick="showPage('varsPage', this)">переменные</button>
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
                    <label>запомнить меня</label>
                </div>
                <button class="btn-main" onclick="doLogin()">войти</button>
                <div id="login_msg" class="msg"></div>
            </div>

            <div id="registerPage" class="page hidden">
                <h2>новый аккаунт</h2>
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
                    <textarea id="reg_about" rows="2"></textarea>
                </div>
                <div class="field">
                    <label>пол</label>
                    <div class="radio-group">
                        <label><input type="radio" name="gender" value="мужской"> муж.</label>
                        <label><input type="radio" name="gender" value="женский"> жен.</label>
                        <label><input type="radio" name="gender" value="другой"> др.</label>
                    </div>
                </div>
                <div class="field">
                    <label>регион</label>
                    <select id="reg_continent">
                        <option value="евразия">евразия</option>
                        <option value="америка">америка</option>
                        <option value="африка">африка</option>
                        <option value="австралия">австралия</option>
                    </select>
                </div>
                <button class="btn-main" onclick="doRegister()">создать</button>
                <div id="reg_msg" class="msg"></div>
            </div>

            <div id="varsPage" class="page hidden">
                <h2>тест переменных</h2>
                <div class="field">
                    <label>поле ввода</label>
                    <input type="text" id="var_text" value="привет">
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="var_check">
                    <label>согласие на обработку</label>
                </div>
                <div class="field">
                    <label>переключатель</label>
                    <div class="radio-group">
                        <label><input type="radio" name="var_radio" id="var_radio_male" value="мужской"> вариант 1</label>
                        <label><input type="radio" name="var_radio" id="var_radio_female" value="женский"> вариант 2</label>
                        <label><input type="radio" name="var_radio" id="var_radio_other" value="другой"> вариант 3</label>
                    </div>
                </div>
                <div class="var-display">
                    <span>текущее состояние:</span>
                    <div id="var_label" class="var-value">—</div>
                </div>
                <div class="hint">данные синхронизируются с python в реальном времени</div>
            </div>
        </div>
    </body>
    </html>
    """

    html_encoded = "data:text/html," + urllib.parse.quote(html_content)
    browser.LoadUrl(html_encoded)

    def on_configure(event):
        if browser:
            browser.NotifyMoveOrResizeStarted()
    browser_frame.bind("<Configure>", on_configure)

    # меню управления окном
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # тема оформления
    theme_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Theme", menu=theme_menu, accelerator="Ctrl+T")
    
    def set_color(color):
        root.configure(bg=color)
        browser_frame.configure(bg=color)
        
    theme_menu.add_command(label="Light Gray", command=lambda: set_color("#e5e5e5"), accelerator="Ctrl+L")
    theme_menu.add_command(label="Dark Gray", command=lambda: set_color("#808080"), accelerator="Ctrl+D")
    theme_menu.add_command(label="Black", command=lambda: set_color("#1a1a1a"), accelerator="Ctrl+B")

    # размер окна
    size_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Size", menu=size_menu, accelerator="Ctrl+S")
    
    def set_size(width, height):
        root.geometry(f"{width}x{height}")
        browser.NotifyMoveOrResizeStarted()
        
    size_menu.add_command(label="500x600", command=lambda: set_size(500, 600), accelerator="Ctrl+5")
    size_menu.add_command(label="800x600", command=lambda: set_size(800, 600), accelerator="Ctrl+8")

    def on_key(event):
        if event.state & 0x4:  # проверяем зажат ли ctrl
            key = event.keysym.lower()
            if key == 'l': set_color("#e5e5e5")
            elif key == 'd': set_color("#808080")
            elif key == 'b': set_color("#1a1a1a")
            elif key == '5': set_size(500, 600)
            elif key == '8': set_size(800, 600)
    root.bind("<Control-Key>", on_key)

    # запуск цикла cef параллельно с tkinter
    def message_loop_work():
        cef.MessageLoopWork()
        root.after(10, message_loop_work)
    message_loop_work()

    def on_closing():
        browser.CloseBrowser(True)
        cef.Shutdown()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
