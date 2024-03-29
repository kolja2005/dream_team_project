document.addEventListener("click", (event) => {
    if (!event.target.closest('#dropdown_usermenu') && !event.target.closest('.btn_user')) {
        dropdown_usermenu.classList.remove('opened')
    }
})