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
            name:businessName,
            email:businessEmail,
            phone:businessPhone,
            currency:"INR",
            brand_voice:brandVoice
        };
        
        fetch(`${API_BASE_URL}/business/`,{
            method:"Post",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(businessData)
        })
        .then(response => {
            if(!response.ok){
                throw new Error("Failed to save business")
            }
            return response.json();
        })
        .then(data =>{
            console.log("Business Created:",data);
            alert("Business saved successfully");
        })
        .catch(error =>{
            console.error(error);
            alert("Error saving business");
        });
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
    fileInput.addEventListener("change", async (event)=>{
        const file = event.target.files[0];
        if(!file) return;

        const reader = new FileReader();
        reader.onload = async (e) => {
            try{
                const rawProducts= JSON.parse(e.target.result);
                if (!Array.isArray(rawProducts)) {
                    alert("JSON file must contain an array of products: [{name, price, stock}]");
                    return;
                }

                const cleanedProducts = rawProducts.map(p => ({
                    name:p.name,
                    price: Number(p.price),
                    stock: Number(p.stock !== undefined ? p.stock : (p.inventory_qty || 0 ))
                }));

                const token = localStorage.getItem("admin_token");
                const res = await fetch(`${API_BASE_URL}/products/bulk`, {
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authorization":token ? `Bearer ${token}`: ""
                    },
                    body: JSON.stringify(cleanedProducts)
                });

                if (!res.ok) {
                    const err = await res.json().catch(() => ({}));
                    const errMsg = Array.isArray(err.detail)
                        ? err.detail.map(d => `${d.loc ? d.loc.slice(-1) : 'field'}: ${d.msg}`).join('\n')
                        : (err.detail || `Upload failed with status ${res.status}`);
                    throw new Error(errMsg);
                }
                const saveProducts = await res.json();

                alert(`Successfully uploaded ${saveProducts.length} products into your store catalog!`);
                fileInput.value = "";
            }
            catch(err){
                console.error(err);
                alert(`Error uploading catalog: ${err.message}`);
            }
        };
        reader.readAsText(file);
    });
}