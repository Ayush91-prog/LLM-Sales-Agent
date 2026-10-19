console.log("Sales Agent Admin Loaded");

function checkAdminAuth(){
    const token = localStorage.getItem("admin_token");
    if(!token || token === "null" || token === "undefined"){
        localStorage.removeItem("admin_token");
        window.location.href = "admin_login.html";
    }
}

function getAuthHeaders(){
    const token = localStorage.getItem("admin_token");
    if (!token || token === "null" || token === "undefined") {
        window.location.href = "admin_login.html";
        return {
            "Content-Type":"application/json"
        };
    }
    return{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`
    };
}

async function autoPopulateBusinessId() {
    const businessIdInputs = document.querySelectorAll("#businessId");
    if (businessIdInputs.length === 0) return;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/admin/me`, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            const admin = await response.json();
            if (admin.business_id) {
                businessIdInputs.forEach(input => {
                    input.value = admin.business_id;
                    input.disabled = true; 
                });
            }
        }
    } catch (err) {
        console.error("Could not auto-populate Business ID", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    autoPopulateBusinessId();
});

function logoutAdmin(){
    localStorage.removeItem("admin_token");
    window.location.href = "admin_login.html";
}

if(!window.location.pathname.includes("admin_login.html") &&
   !window.location.pathname.includes("customer_login.html")&&
   !window.location.pathname.includes("landing.html")){
    checkAdminAuth();
   }