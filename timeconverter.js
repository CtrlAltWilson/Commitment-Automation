function addTimeToString(timeString, addHours, addMinutes) {
 if (addMinutes === undefined) addMinutes = 0;
 var match = /(d+):(d+)s+(w+)/.exec(timeString),
   hours = Number(match[1], 10) % 12,
   minutes = Number(match[2], 10),
   modifier = match[3].toLowerCase();
 if (modifier[0] == 'p') hours += 12;
 var newMinutes = (hours + addHours) * 60 + minutes + addMinutes,
   newHours = Math.floor(newMinutes / 60) % 24;
 newMinutes %= 60;
 var newModifier = (newHours < 12 ? 'AM' : 'PM'),
   hours12 = (newHours < 12 ? newHours : newHours % 12);
 if (hours12 === 0) hours12 = 12;
 var minuteString = (newMinutes >= 10 ? '' : '0') + newMinutes;
 return hours12 + ':' + minuteString + ' ' + newModifier;
}

addTimeToString("5:05 PM",0,1);