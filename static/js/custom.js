function notify(type,text){
    var n = noty({
        layout: 'topRight',
        theme: 'relax',
        type: type,
        text: text,
        animation: {
            open: {height: 'toggle'},
            close: {height: 'toggle'},
            easing: 'swing', // easing
            speed: 500
        },
        timeout: 5000,
        killer: true,
        maxVisible: 1
    });
}

function checkEmpty(fieldname,fieldvalue){
    if(fieldvalue===''){
        notify('error',fieldname+' cannot be empty');
        return true;
    }
    else return false;
}

function validatePhotoFormat(fileName){
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile==="jpg" || extFile==="jpeg" || extFile==="png"){
        return true;
    }else{
        return false;
    }
}

function validateUploadImage() {
    var inputImage = document.getElementById('inputImage').value.trim();
    if(checkEmpty("Upload Image",inputImage)) return false;
    if(!validatePhotoFormat(inputImage)){
        notify("error","Photo Format must be jpeg, jpg or png");
        return false;
    }else{
        return true;
    }
}
