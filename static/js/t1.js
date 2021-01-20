function web1(){
    document.getElementById("set").innerHTML="sfef";
}
function web2(){
    document.getElementById("set1").style.fontSize="120px";
}
function web3(){
    var ms;
    if(confirm(" Are YOU  sure")){
        ms = "OK";
    
    }else{
        ms = "cancle";
    }
    document.getElementById("set2").innerHTML= ms;

}
