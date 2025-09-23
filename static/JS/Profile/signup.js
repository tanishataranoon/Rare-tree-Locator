
document.addEventListener("DOMContentLoaded", function () {
    let userTypeField = document.getElementById("id_user_type");
    let professionField = document.getElementById("professionField");

    function toggleProfession() {
        if (userTypeField.value === "contributor") {
            professionField.style.display = "block";
        } else {
            professionField.style.display = "none";
        }
    }

    userTypeField.addEventListener("change", toggleProfession);
    toggleProfession();
});
  