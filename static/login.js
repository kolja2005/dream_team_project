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

    login = document.querySelector("#login").value
    password = document.querySelector("#password").value

    let xhr = new XMLHttpRequest();
    xhr.getResponseHeader("Content-Type", "application/json;charset=utf-8")
    xhr.open("POST", "/login")

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
    xhr.send(JSON.stringify({"login": login, "password": password}))
}

