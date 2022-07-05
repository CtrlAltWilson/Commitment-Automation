function addTimeToString(timeString, addHours, addMinutes) {
    console.log("starting createCommit");
    console.log(timeString);
    if (addMinutes === undefined) {
        addMinutes = 0;
    }
    var match = /(\d+):(\d+)\s+(\w+)/.exec(timeString);

    var hours = Number(match[1]) % 12;
    var minutes = Number(match[2]);
    var modifier = match[3].toLowerCase();
    console.log("1",hours,minutes,modifier);
    if (modifier[0] == 'p') hours = hours + 12;
    
    var newMinutes = ((hours + addHours) * 60) + (minutes + addMinutes);
    var newHours = Math.floor(newMinutes / 60) % 24;
    var newMinutes = newMinutes % 60;
    var newModifier = (newHours < 12 ? 'AM' : 'PM');
    console.log("2",newHours,newMinutes,newModifier);
    
    var hours12 = (newHours < 12 ? newHours : newHours % 12);
    if (hours12 == 0) hours12 = 12;
    
    var minuteString = (newMinutes >= 10 ? '' : '0') + newMinutes;
    return hours12 + ':' + minuteString + ' ' + newModifier;
}

function createCommit() {
    console.log("starting createCommit");
    navigator.clipboard.readText().then(
        clipText => {
            clipped = clipText.split(",");
            console.log("Clipped = " + clipped);
            console.log("arr is " + typeof(clipped));
            if (clipped.length != 4) {
                console.log(clipped.length);
                console.log("Nothing clipped!");
                return
            }
            document.querySelector("#HomePromiseKeeperIconDiv").click();
            document.querySelector("#newBtnId").click();
            document.getElementById('firstNameId').value = clipped[0];
            document.getElementById('lastNameId').value = clipped[1];
            document.getElementById('phoneId').value = clipped[2];

            radiobtn = document.querySelectorAll("input[type=radio][name=promiseBtnId]");
            radiobtn[1].checked = true;

            setTimeout(function() {
                document.querySelector(".txtSpn.textEllipsis.dispComboText").click();
                document.querySelector("[id='Support OB']").click();
            }, 1000);

            document.querySelector('[class=dateTimeIconDiv]').click();
            setTimeout(function() {
                var newTime = addTimeToString(document.querySelector('[id=timePickerInputTxt]').value, 0, Number(clipped[3]));
                console.log(document.querySelector('[id=timePickerInputTxt]').value, newTime, clipped[3]);
                document.querySelector('[id=timePickerInputTxt]').value = newTime;
                document.querySelector('[id=saveBtn]').click();
            }, 1000);
            setTimeout(function(){
            	document.querySelector('[id=saveBtnID]').click();
            }, 2000);
            setTimeout(function(){
                assignedTo = document.querySelectorAll('input[type=radio][name=promiseKeeperRbtn]');
                assignedTo[1].checked = true;
            },2000);
            console.log("end createCommit");
        });
}

function importClip() {
    console.log("starting importClip");
    var commitDiv = document.createElement('div');
    commitDiv.classList.add('btnBrRound5', 'hpIconDiv', 'btnDivEnable');

    var commitBtn = document.createElement("button");
    commitBtn.innerHTML = "IMPORT";
    commitBtn.style.width = "40px";
    commitBtn.style.height = "40px";
    commitBtn.style.fontSize = "0.7em";
    commitBtn.addEventListener('click', function() {
        createCommit();
    });
    commitDiv.appendChild(commitBtn);
    setTimeout(function() {
        document.querySelector('.homePage').append(commitDiv);
    }, 1000);
    console.log("end importClip");
}

importClip();