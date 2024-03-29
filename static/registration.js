document.addEventListener('click', (event) => {
    if (event.target.closest('input')) {
        error_block.classList.remove('opened')
    }
})

send_btn = document.querySelector(".send_btn")
error_message = document.querySelector(".error_message")
error_block = document.querySelector(".error_block")

send_btn.onclick =  (event) => {
    error_block.classList.remove('opened')

    f_name = document.querySelector("#f_name").value
    l_name = document.querySelector("#l_name").value
    m_name = document.querySelector("#m_name").value
    login = document.querySelector("#login").value
    password = document.querySelector("#password").value
    password2 = document.querySelector("#password2").value


    if (/[!@#$%^&*]|[\d]/.test(f_name)) {
        error_block.classList.add('opened')
        error_message.innerText = "Имя может содержать только буквы"
        return;
    }
    if (/[!@#$%^&*]|[\d]/.test(l_name)) {
        error_block.classList.add('opened')
        error_message.innerText = "Фамилия может содержать только буквы"
        return;
    }
    if (m_name && /[!@#$%^&*]|[\d]/.test(m_name)) {
        error_block.classList.add('opened')
        error_message.innerText = "Отчество может содержать только буквы"
    }
    if (f_name.length > 30 || l_name.length > 30 || m_name.length > 30 || f_name.length == 0 || l_name.length == 0) {
        error_block.classList.add('opened')
        error_message.innerText = "Ошибка ввода"
        return;
    }

    if (password.length < 8 || password.lenght > 20) {
        error_block.classList.add('opened')
        error_message.innerText = "Длина пароля: от 8 до 20 символов"
        return;
    }
    if (!/\d/.test(password)) {
        error_block.classList.add('opened')
        error_message.innerText = "Пароль должен содержать хотя бы одну цифру"
        return;
    }
    if (!/[a-z]/.test(password) && !/[A-Z]/.test(password)){
        error_block.classList.add('opened')
        error_message.innerText = "Пароль должен содержать буквы латинского алфавита"
        return;
    }

    if (!/[!@#$%^&*]/.test(password)) {
        error_block.classList.add('opened')
        error_message.innerText = "Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*)"
        return;
    }

    if (password != password2) {
        error_block.classList.add('opened')
        error_message.innerText = "Пароли не совпадают"
        return
    }


    let xhr = new XMLHttpRequest();
    xhr.getResponseHeader("Content-Type", "application/json;charset=utf-8")
    xhr.open("POST", "/registration")

    xhr.onload = () => {
        if (xhr.status != 200) {
            error_block.classList.add("opened")
            if (xhr.status == 400) {
                error_message.innerText = xhr.responseText
            }
            else {
                error_message.innerText = "Ошибка " + xhr.status;
            }

        } else {
            window.location.href = '/'
        }

    }

    xhr.onerror = () => {
        error_block.classList.add("opened")
        error_message.innerText = "Ошибка подключения"
    }
    xhr.send(JSON.stringify({"f_name": f_name, "l_name": l_name, "m_name": m_name, "login": login, "password": password, "password2": password2 }))
}

