console.log("Sales Agent Admin Loaded");

function checkAdminAuth(){
    const token = localStorage.getItem("admin_token");
    if(!token){
        window.location.href = "admin_login.html";
    }
}

function getAuthHeaders(){
    const token = localStorage.getItem("admin_token");
    return{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`
    };
}

function logoutAdmin(){
    localStorage.removeItem("admin_token");
    window.location.href = "admin_login.html";
}

if(!window.location.pathname.includes("admin_login.html") &&
   !window.location.pathname.includes("customer_login.html")&&
   !window.location.pathname.includes("landing.html")){
    checkAdminAuth();
   }