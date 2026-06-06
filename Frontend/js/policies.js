console.log("Policies Page Loaded");
const saveButton= document.querySelector(".primary-btn")
if (saveButton) {
    saveButton.addEventListener("click",() => {
        const inputs=document.querySelectorAll("input");
        const policyData= {};
        inputs.forEach((input,index) => {
            if(input.type ==="checkbox"){
                policyData[`checkbox_${index}`] =input.checked;
            }else{
                policyData[`input_${index}`]= input.value;
            }
        });
        localStorage.setItem(
            "policyData",
            JSON.stringify(policyData)
        );
        alert("Policies Saved Succesfully");
        console.log(policyData);

    } );
}