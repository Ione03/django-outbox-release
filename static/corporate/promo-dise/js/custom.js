function openWA(number) {
    //var number = document.getElementById("waNumber").value;
    //if (isMobile()=="true")
    console.log('number',number);
    window.open("https://api.whatsapp.com/send?phone="+ number +"&text=Hai, Saya ada pertanyaan tentang cara membuat website di https://authbox.web.id/","_blank");
    //else
    //   alert("This link will open Whatsapp on android");
 }