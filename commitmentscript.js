function inputDetails(arr, minutes){
	arr.push(minutes);
	var sampleTextarea = document.createElement("textarea");
	document.body.appendChild(sampleTextarea);
	sampleTextarea.value = arr; //save main text in it
	sampleTextarea.select(); //select textarea contenrs
	document.execCommand("copy");
	document.body.removeChild(sampleTextarea);
	console.log("Copied!");
	arr.pop(minutes);
}

function addText(arr) {
	let divName = document.createElement("div");
	let divPhone = document.createElement("div");
	divName.innerHTML = arr[1];
	divPhone.innerHTML = arr[2];
	document.querySelector('.pageDescription').append(divName,divPhone);
	console.log("arr2 = " + arr[2]);
	if (arr[3]){
		arr.pop(3);
		var commitBtn = document.createElement("button");
		commitBtn.innerHTML = "+2m";
		commitBtn.addEventListener('click', function(){
			inputDetails(arr, 2);
		});
		var commitBtn2 = document.createElement("button");
		commitBtn2.innerHTML = "+15m";
		commitBtn2.addEventListener('click', function(){
			inputDetails(arr, 15);
		});
		var commitBtn3 = document.createElement("button");
		commitBtn3.innerHTML = "+30m";
		commitBtn3.addEventListener('click', function(){
			inputDetails(arr, 30);
		});
		var commitBtn4 = document.createElement("button");
		commitBtn4.innerHTML = "+60m";
		commitBtn4.addEventListener('click', function(){
			inputDetails(arr, 60);
		});
		document.querySelector('.pageDescription').append("Create Commit:" ,commitBtn,commitBtn2,commitBtn3,commitBtn4);
	}
}

function getCommit() {
	var caseNum = document.querySelector(".pageDescription").innerHTML.slice(0, 9);
	var generateBtn = 1;
	var phone = "";

	try {
		var name = document.querySelector("#cas3_ileinner a").innerHTML;
	} catch (e) {
		return
	}

	try {
		var phone1 = document.querySelector("#cas20_ileinner").innerHTML;
	} catch (e) {
		var phone1 = "";
	}
	try {
		var phone2 = document.querySelector("#cas9_ileinner a").innerHTML;
	} catch (e) {
		var phone2 = "";
	}

	if (phone1 === "" || phone1 === "&nbsp;") {
		phone = phone2.replace(/[()-. ]/g, "");
		console.log('2', caseNum, name, phone2);
	} else {
		phone = phone1.replace(/[()-. ]/g, "");
		console.log('1', caseNum, name, phone1);
	}

	phone = phone.slice(0,10)

	if (phone === ""){
		phone = "No Number";
		generateBtn = 0;
	} else if (phone.charAt(0) === '+'){
		phone = "Recheck: International Number";
		generateBtn = 0;
	} else if (phone.length < 10) {
		phone = "Recheck: Number too Short";
		generateBtn = 0;
	}

	return [caseNum,name,phone,generateBtn];
}

function main(){
	commitInfo = getCommit();
	addText(commitInfo);
}

main();