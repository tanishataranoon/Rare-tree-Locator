document.addEventListener("DOMContentLoaded", () => {
    const userType = document.getElementById("userType");
    const professionField = document.getElementById("professionField");
    const createAccountBtn = document.getElementById("createAccountBtn");
    const agreementModal = document.getElementById("agreementModal");
    const agreeBtn = document.getElementById("agreeBtn");
    const cancelBtn = document.getElementById("cancelBtn");
    const signupForm = document.getElementById("signupForm");
  
    // Show/hide profession field based on user type
    userType.addEventListener("change", () => {
      if (userType.value === "contributor") {
        professionField.style.display = "block";
      } else {
        professionField.style.display = "none";
      }
    });
  
    // Show agreement modal when clicking Create Account
    createAccountBtn.addEventListener("click", () => {
      agreementModal.style.display = "flex";
    });
  
    // Agree -> submit form
    agreeBtn.addEventListener("click", () => {
      agreementModal.style.display = "none";
      signupForm.submit();
    });
  
    // Cancel -> close modal
    cancelBtn.addEventListener("click", () => {
      agreementModal.style.display = "none";
    });
  });
  