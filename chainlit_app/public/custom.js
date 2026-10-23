// chainlit_app/public/custom.js
(function () {
  // Save URL query parameters immediately upon page load into sessionStorage
  const urlParams = new URLSearchParams(window.location.search);
  const cid = urlParams.get("customer_id");
  const cname = urlParams.get("name");
  const caddr = urlParams.get("address");

  if (cid) sessionStorage.setItem("customer_id", cid);
  if (cname) sessionStorage.setItem("customer_name", cname);
  if (caddr) sessionStorage.setItem("customer_address", caddr);

  // Listen for Chainlit backend requests via CopilotFunction
  window.addEventListener("chainlit-call-fn", (e) => {
    const { name, args, callback } = e.detail;
    if (name === "get_customer_params") {
      const params = new URLSearchParams(window.location.search);
      const customerId = params.get("customer_id") || sessionStorage.getItem("customer_id");
      const customerName = params.get("name") || sessionStorage.getItem("customer_name");
      const customerAddress = params.get("address") || sessionStorage.getItem("customer_address");

      callback({
        customer_id: customerId,
        name: customerName,
        address: customerAddress
      });
    }
  });
})();
