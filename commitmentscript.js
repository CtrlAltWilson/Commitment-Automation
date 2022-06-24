function addText(name, phone) {
    let createDiv = document.createElement("div");
    createDiv.innerHTML = name + " " + phone;
    document.querySelector('.pageDescription').appendChild(createDiv);
}
function getCommit() {
    var caseNum = document.querySelector(".pageDescription").innerHTML.slice(0,9);
    var name = document.querySelector("#cas3_ileinner a").innerHTML;
    var phone1 = document.querySelector("#cas20_ileinner").innerHTML;
    var phone2 = document.querySelector("#cas9_ileinner a").innerHTML;
    if (phone1 === "" || phone1 === "&nbsp;") {
        phone2 = phone2.replace("(","").replace(")","").replace(" ","").replaceAll("-","").slice(0,10);
        console.log('2',caseNum, name, phone2);
        addText(name, phone2);
    } else {
        phone1 = phone1.replace("(","").replace(")","").replace(" ","").replaceAll("-","")
        console.log('1', caseNum, name,phone1);
        addText(name, phone1);
    }
}
getCommit();
