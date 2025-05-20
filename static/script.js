document.addEventListener("DOMContentLoaded", () => {
    const userList = document.getElementById("userList");
    const totalStepsElement = document.getElementById("totalSteps");
    
    // Функция загрузки данных
    function loadData() {
        // Загружаем пользователей
        fetch("/api/users")
            .then(response => response.json())
            .then(users => {
                userList.innerHTML = "";
                users.forEach(user => {
                    const li = document.createElement("li");
                    li.innerHTML = `${user.name} шагов (${user.email}) 
                        <button onclick="deleteUser(${user.id})">❌</button>`;
                    userList.appendChild(li);
                });
            });
        
        // Загружаем общую сумму
        fetch("/api/users/sum")
            .then(response => response.json())
            .then(data => {
                totalStepsElement.textContent = data.total_steps;
            });
    }

    // Обработчик формы (если она есть на странице)
    const userForm = document.getElementById("userForm");
    if (userForm) {
        userForm.addEventListener("submit", event => {
            event.preventDefault();
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;

            fetch("/api/users", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: parseInt(name), email })
            }).then(() => loadData());
        });
    }

    // Удаление пользователя
    window.deleteUser = (id) => {
        fetch(`/api/users/${id}`, { method: "DELETE" })
            .then(() => loadData());
    };

    // Первоначальная загрузка
    loadData();
});