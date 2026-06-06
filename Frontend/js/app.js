console.log("Sales Agent Admin Loaded");

function showAlert(message){
    alert(message);
}
function saveToLocal(key,data){
    localStorage.setItem(key,JSON.stringify(data));
}
function getFromLocal(key){
    const data= localStorage.getItem(key);
    if(!data){
        return null;
    }
    return JSON.parse(data);
}