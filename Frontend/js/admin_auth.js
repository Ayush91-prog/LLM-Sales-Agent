document.addEventListener("DOMContentLoaded", () => {
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const codeAlert = document.getElementById('codeAlert');

    loginTab.addEventListener('click', () => {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    });

    registerTab.addEventListener('click', () => {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.style.display = 'block';
        loginForm.style.display = 'none';
    });

    // Handles Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const identifier = document.getElementById('loginIdentifier').value;
        const password = document.getElementById('loginPassword').value;

        try {
            console.log("Connecting to:",API_BASE_URL);
            const res = await fetch(`${API_BASE_URL}/auth/admin/login`, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ identifier, password })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem('admin_token', data.access_token);
                window.location.href = 'index.html';
            } else {
                alert(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail));
            }
        }
        catch (err) {
            console.error("Login Error:",err);
            alert(`Connection Error: ${err.message}`);
        }
    });

    // Handle Admin Register
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('regName').value;
        const business_name = document.getElementById('regBusiness').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        try {
            console.log("Connecting to:",`${API_BASE_URL}/auth/admin/register`);
            const res = await fetch(`${API_BASE_URL}/auth/admin/register`, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, business_name, email, password })
            });

            const data = await res.json();
            if (res.ok) {
                document.getElementById('displayAdminCode').innerText = data.admin_code;
                codeAlert.style.display = 'block';
                localStorage.setItem('admin_token', data.access_token);
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 4000);
            } else {
                alert(typeof data.detail === 'string' ? data.detail:JSON.stringify(data.detail));
            }
        } catch (err) {
            console.log("Registration Error:", err)
            alert(`Connection Error: ${err.message}`);
        }
    });
})