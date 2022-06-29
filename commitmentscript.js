function inputDetails(arr, minutes){
	var text =" \
	function addTimeToString(timeString, addHours, addMinutes) {\n \
	  if (addMinutes === undefined) {\n \
	    addMinutes = 0; \n \
	  } \n \
	  var match = /(\\d+):(\\d+)\\s+(\\w+)/.exec(timeString); \n \
	      hours = Number(match[1]) % 12; \n \
	      minutes = Number(match[2]); \n \
	      modifier = match[3].toLowerCase(); \n \
	  if (modifier[0] == 'p') { \n \
	    hours += 12;\n \
	  }\n \
	  var newMinutes = (hours + addHours) * 60 + minutes + addMinutes,\n \
	      newHours = Math.floor(newMinutes / 60) % 24;\n \
	  newMinutes %= 60;\n \
	  var newModifier = (newHours < 12 ? 'AM' : 'PM'),\n \
	      hours12 = (newHours < 12 ? newHours : newHours % 12);\n \
	  if (hours12 == 0) {\n \
	    hours12 = 12;\n \
	  }\n \
	  var minuteString = (newMinutes >= 10 ? '' : '0') + newMinutes;\n \
	  return hours12 + ':' + minuteString + ' ' + newModifier;\n \
	}\n \
	document.querySelector(\"#HomePromiseKeeperIconDiv\").click();\n \
	document.querySelector(\"#newBtnId\").click();\n \
	document.getElementById('firstNameId').value = \"" + arr[0] + "\";\n \
	document.getElementById('lastNameId').value = \"" + arr[1] + "\";\n \
	document.getElementById('phoneId').value = \"" + arr[2] + "\";\n \
	\
	radiobtn = document.querySelectorAll(\"input[type=radio][name=promiseBtnId]\");\n \
	radiobtn[1].checked = true;\n \
	\
	setTimeout(function(){\
		document.querySelector(\".txtSpn.textEllipsis.dispComboText\").click();\n \
		document.querySelector(\"[id='Support OB']\").click();\n \
	},1000);\
	\
	document.querySelector('[class=dateTimeIconDiv]').click();\n \
	setTimeout(function(){\
		document.querySelector('[id=timePickerInputTxt]').value = addTimeToString(document.querySelector('[id=timePickerInputTxt]').value,0," + minutes + ");\n \
		document.querySelector('[id=saveBtn]').click();\n \
	},1000);\
	";
	arr.push(minutes);
	//document.querySelector(\"#hour1\").click();\n \
	var sampleTextarea = document.createElement("textarea");
	document.body.appendChild(sampleTextarea);
	sampleTextarea.value = arr; //save main text in it
	sampleTextarea.select(); //select textarea contenrs
	document.execCommand("copy");
	document.body.removeChild(sampleTextarea);
	console.log("Copied!");
	/*
	setOutbound = document.querySelectorAll(".txtSpn.textEllipsis.dispComboText");
	setOutbound[0].title = "Support OB";
	setOutbound[0].textContent = "Support OB";
	*/
	arr.pop(minutes);
}

function addText(arr) {
	if (arr[2] === "") arr[2] = "No Number";
	let divName = document.createElement("div");
	let divPhone = document.createElement("div");
	divName.innerHTML = arr[1];
	divPhone.innerHTML = arr[2];
	document.querySelector('.pageDescription').append(divName,divPhone);
	console.log("arr2 = " + arr[2]);
	if (arr[2] !== "No Number"){
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

	var phone = "";
	if (phone1 === "" || phone1 === "&nbsp;") {
		phone = phone2.replace(/[()-. ]/g, "");
		console.log('2', caseNum, name, phone2);
	} else {
		phone = phone1.replace(/[()-. ]/g, "");
		console.log('1', caseNum, name, phone1);
	}
	phone = phone.slice(0,10)
	if (phone.charAt(0) === '+'){
		phone = "Recheck: International Number"
	}
	if (phone.length < 10) {
		phone = "Recheck: Number too Short"
	}
	return [caseNum,name,phone];
}

function main(){
	commitInfo = getCommit();
	addText(commitInfo);
}

main();