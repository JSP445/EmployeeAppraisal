const appraiserIdInput = document.querySelector('#employeeAppraiserId')
const distAwayInput = 'translateY(-50px)';

appraiserIdInput.required = true;

onChangeSelect = (select) => {
    if (select.value.toUpperCase() === "EMPLOYEE") {
        appraiserIdInput.style.visibility = "visible";
        appraiserIdInput.style.transform = "translateY(0px)";
        appraiserIdInput.style.opacity = "1.0";
        appraiserIdInput.required = true;
    }
    else {
        appraiserIdInput.required = false;
        appraiserIdInput.style.visibility = "hidden";
        appraiserIdInput.style.opacity = "0";
        appraiserIdInput.style.transform = distAwayInput;
    }
}