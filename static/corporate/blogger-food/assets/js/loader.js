
function loader() {
    console.log('call loader');   
    console.log(document.getElementByClass("loader1")); 
    document.getElementByClass("loader1").style.display = "block";
    //$('#loader').addClass('show');		
    
    setTimeout(
        //function() { 
        //    if ($('.loader').length > 0) 
        //        $('.loader').removeClass('show');			
        //}
        showPage
    , 10000);
};
    
function showPage() {
    console.log('Show Page');    
    document.getElementById(".loader1").style.display = "none";
    document.getElementById("body-content").style.display = "block";
};
