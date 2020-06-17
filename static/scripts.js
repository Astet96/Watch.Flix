function prd(){
    var dec = document.getElementById("period").value;
    var str1 = "Period: ";
    var str2 = String(dec);
    var str3 = "'s";
    str1 += str2 + str3;
    console.log(str1);
    document.getElementById("period_label").innerHTML = str1;
}

function str(){
    var rt = document.getElementById("star").value;
    var str1 = "Rating: ";
    var str2 = String(rt);
    var str3 = " stars";
    str1 += str2 + str3;
    console.log(str1);
    document.getElementById("star_label").innerHTML = str1;
}