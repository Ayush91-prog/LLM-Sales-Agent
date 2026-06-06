console.log("Business Page Loaded")
const saveButton = document.querySelector("#saveBusinessBtn");
if (saveButton) {
    saveButton.addEventListener("click",() =>{

        const businessName= document.querySelector("#businessName").value;
        const businessEmail = document.querySelector("#businessEmail").value;
        const businessPhone= document.querySelector("#businessPhone").value;
        const brandVoice = document.querySelector("#brandVoice").value;
        if (!businessName) {
            alert("Please enter Business Name");
            return;
        }
        if (!businessEmail) {
            alert("Please enter Business Email");
            return;
        }
        if (!businessPhone) {
            alert("Please enter Business Phone");
            return;
        }
        if (!brandVoice) {
            alert("Please enter Brand Voice");
            return;
        }
        const businessData={
            businessName,
            businessEmail,
            businessPhone,
            brandVoice
        };
        localStorage.setItem(
            "businessData",
            JSON.stringify(businessData)
        );
        alert("Business Information Saved");
        console.log(businessData);
    }
    );
}

const uploadBtn= document.querySelector("#uploadCatalogBtn");
const fileInput = document.querySelector("#catalogFile");
if(uploadBtn){
    uploadBtn.addEventListener("click",()=>{
        fileInput.click();
    });
}
if(fileInput){
    fileInput.addEventListener("change",(event)=>{
        const file = event.target.files[0];
        if(!file) return;
        const reader = new FileReader();
        reader.onload =(e) => {
            try{
                const products= JSON.parse(e.target.result);
                localStorage.setItem("products",JSON.stringify(products));
                alert("Catalog Uploaded Successfully");
            }
            catch{
                alert("Invalid JSON File")
            }
        };
        reader.readAsText(file);
    });
}