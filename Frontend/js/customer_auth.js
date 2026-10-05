document.addEventListener("DOMContentLoaded",()=>{
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    loginTab.addEventListener('click',()=>{
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.style.display='block';
        registerForm.style.display='none';
    });

    registerTab.addEventListener('click',()=>{
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.style.display='block';
        loginForm.style.display='none';
    });

    loginForm.addEventListener('submit',async(e)=>{
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try{
            const res = await fetch(`${API_BASE_URL}/auth/customer/login`,{
                method:"POST",
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({email,password})
            });
            const data = await res.json();
            if(res.ok){
                localStorage.setItem('customer_token',data.access_token);
                alert("Logged in Successfully! Redirecting to AI Chat...");
                window.location.href = 'https://llm-sales-agent.onrender.com'
            }else{
                alert(data.detail || "Login Failed");
            }
        }catch(err){
            alert('Could not connect to backend server');
        }
    });

    registerForm.addEventListener('submit', async(e)=>{
        e.preventDefault();
        const name = document.getElementById('regName').value;
        const email = document.getElementById('regEmail').value;
        const phone = document.getElementById('regPhone').value;
        const password = document.getElementById('regPassword').value;

        try{
            const res = await fetch(`${API_BASE_URL}/auth/customer/register`,{
                method:"POST",
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({name,email,phone,password})
            });
            const data = await res.json();
            if(res.ok){
                localStorage.setItem('customer_token',data.access_token);
                alert("Account created! Redirecting to AI Chat...");
                window.location.href='https://llm-sales-agent.onrender.com';
            }else{
                alert(data.detail || 'Registration failed');
            }
        }catch(err){
            alert('Could not connect to backend server');
        }
    });
})