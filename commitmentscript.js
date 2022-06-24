function addText(name, phone) {
    if (phone === "") phone = "No Number";
    let divName = document.createElement("div");
    let divPhone = document.createElement("div");
    divName.innerHTML = name;
    divPhone.innerHTML = phone;
    document.querySelector('.pageDescription').append(divName,divPhone);
}

function getCommit() {
    var caseNum = document.querySelector(".pageDescription").innerHTML.slice(0, 9);
    
    try {
        var name = document.querySelector("#cas3_ileinner a").innerHTML;
    } catch (e) {
        return
    }

    try {
        var phone1 = document.querySelector("#cas20_ileinner").innerHTML;
    } catch (e) {
        var phone1 = ""
    }
    try {
        var phone2 = document.querySelector("#cas9_ileinner a").innerHTML;
    } catch (e) {
        var phone2 = ""
    }
    if (phone1 === "" || phone1 === "&nbsp;") {
        phone2 = phone2.replace(/[()-. ]/g, "");
        console.log('2', caseNum, name, phone2);
        addText(name, phone2);
    } else {
        phone1 = phone1.replace(/[()-. ]/g, "");
        console.log('1', caseNum, name, phone1);
        addText(name, phone1);
    }
}
getCommit();