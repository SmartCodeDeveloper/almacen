
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function isValidDate(str){
        // STRING FORMAT yyyy-mm-dd
        if(str=="" || str==null){return false;}								
        
        // m[1] is year 'YYYY' * m[2] is month 'MM' * m[3] is day 'DD'
        let re = /(\d{4})-(\d{2})-(\d{2})/

        let valid = re.test(str);

        console.log("valid")
        console.log(valid);

        if(!valid){
          return false;
        }
        
					
        var thisYear = new Date().getFullYear(); //YEAR NOW
        var minYear = 1999; //MIN YEAR
        var m = str.split("-");
        

        // YEAR CHECK
        if( parseInt(m[0]) < thisYear){ return false;}
        // MONTH CHECK			
        if( (m[1].length < 2) || parseInt(m[1]) < 1 || parseInt(m[1]) > 12){return false;}
        // DAY CHECK
        if( (m[2].length < 2) || parseInt(m[2]) < 1 || parseInt(m[2]) > 31){return false;}

        
        return true;			
    }




    function validateEmptyOrNull(value){
        let validate = false;

        if(value.length==0 || value==null || value==undefined)
          validate = true;

        return validate;
    }

    function validateEmail(value){
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(value).toLowerCase());
    }


    function isOneNumber(value){
        let validate = false;

        if($.isNumeric(value)){
            if(value.indexOf(".") == -1){
                validate = true;
            }
        }

        return validate;
    }

    function messageError(mjs){
         Swal.fire({
           title: "Error",
           text: mjs,
           icon: 'error',
           confirmButtonText: 'OK'
         });
    }

    function menssageExit(title, mjs){
        Swal.fire(title, mjs, 'success');
    }


    function getOrDeletePeticion(url, method, csrftoken){
        return fetch(url, {
            method: method,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            }
        });
    }


    function postorPutPeticion(url, method, data, csrftoken){
        return fetch(url,{
            method: method,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });
    }



    function addOptionsSelect(selectid, elements){

        let select = document.getElementById(`${selectid}`);
        select.innerHTML = "";
    
        elements.map((value, index)=>{

          var opt = document.createElement('option');
          opt.appendChild(document.createTextNode(value.name));
          opt.value = value.id;
          select.appendChild(opt);
    
        });

    }


    function getToday(){

        let today = new Date();

        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();

        today = dd + '/' + mm + '/' + yyyy;

        return today;

    }

    function convertDate(day){

        let dayArray = day.split("/");
        day = dayArray[2]+"-"+dayArray[1]+"-"+dayArray[0];

        return day;
    }


    function convertDateSpanish(day){
        
        let dayArray = day.split("-");
        day = dayArray[2]+"/"+dayArray[1]+"/"+dayArray[0];

        return day;
    }

    function validExtension(filename, extensions)
    {

        let fileNameExt     = filename.substr(filename.lastIndexOf('.') + 1);
        //let validExtensions = ['jpg','png','jpeg'];
        let validExtensions = extensions;
        let valid = false;

        if ($.inArray(fileNameExt, validExtensions) != -1) {
            valid = true;
        }

        return valid;
    }




    function cleanFieldsText(idfields){
        idfields.map((value, index)=>{
            document.getElementById(`${value}`).value = "";
        });
    }

    function defaultSelect(idfields, index){
        idfields.map((value, index)=>{
            document.getElementById(`${value}`).selectedIndex = index;
        })
    }

    function defaultCheck(idfields, status){
        idfields.map((value, index)=>{
            document.getElementById(`${value}`).checked = status;
        });
    }

    function getObjectBody(idfields){
        let objectresult = {};


        idfields.map((value, index)=>{
            Object.assign(objectresult, {[`${value}`]: document.getElementById(`${value}`).value})
        });

        return objectresult;
    }



    function listHours(classid, classfrom, classto, classfrom2, classto2, classfrom3){

        let rangosValidos = [];
        $(classid).each((index, elemento)=>{
            let  id  = $(elemento).data("id");
            let from = $(elemento).find(classfrom).first();
            let to   = $(elemento).find(classto).first();

            let from2 = $(elemento).find(classfrom2).first();
            let to2   = $(elemento).find(classto2).first();

            let from3 = $(elemento).find(classfrom3).first();

            let anticipation = from2.val()
            let maxwashes    = to2.val()
            let active = from3.val() == "1" ? true: false;
            let fromvalue = from.val()
            let tovalue   = to.val()
            let discount  = $("#discount").val()

            console.log(parent);
            rangosValidos.push({id, hourstart: fromvalue , hourend: tovalue, anticipation: anticipation, maxwashes: maxwashes, active: active, discount: discount })
        });

        return rangosValidos;

    }


    function validarListHours(classid, classfrom, classto, classextra1, classextra2, fromfunc, tofunc, indexroot ){
        let valid = true;
        let rangosValidos = [];
        $(classid).each((index, elemento)=>{

            console.log(elemento);
            let from = $(elemento).find(classfrom).first();
            let to   = $(elemento).find(classto).first();
            let anticipation = $(elemento).find(classextra1).first();
            let maxwashes    = $(elemento).find(classextra2).first();
            let fromvalue = from.val()
            let tovalue   = to.val()
            let maxwashesvalue = maxwashes.val();
            let anticipationvalue = anticipation.val();
            

            console.log(tovalue);
            console.log(fromvalue);
            console.log(maxwashesvalue)
            console.log(anticipationvalue)

            let valor = !validateEmptyOrNull(fromvalue);

            console.log(valor);

            if(validateEmptyOrNull(fromvalue)){ valid=false; return false; }
            if(validateEmptyOrNull(tovalue)){ valid=false; return false; }
            if(anticipationvalue==null ||  anticipationvalue==undefined){ valid=false; return false; }
            if(maxwashesvalue==null || maxwashesvalue==undefined){ valid=false; return false; }
            if(!isOneNumber(anticipationvalue)){ valid=false; return false; }
            if(!isOneNumber(maxwashesvalue)){ valid=false; return false; }


           // alert("rumbo a validates");

            if(validateHours(fromvalue, tovalue)){ valid=false;  return false;  }

           // alert("paso validadtes")



            if(indexroot!=index){

                if(fromfunc!=null && tofunc!=null ){
                    console.log("no entro en recursividad")
                    if(!validateRange(fromvalue, tovalue, fromfunc, tofunc, index, indexroot)){ valid =false; return false;}
                }else{
                    console.log("entro en recursividad")
    
                    if(!validarListHours(classid, classfrom, classto, classextra1, classextra2, fromvalue, tovalue, index)){valid =false; return false;}
                    
                }

            }
            
          })

          return valid;
    }


    function validateRange(hourfrom, hourto, hour2from, hour2to, indexa, indexb)
    {

        console.log("entro en validar rango")
        hourfrom = hourfrom.split(":");
        hourto   = hourto.split(":");
        hour2from = hour2from.split(":");
        hour2to   = hour2to.split(":");
        let valid  = false;


        let dateStart = new Date();
        dateStart.setHours(hourfrom[0], hourfrom[1]);

        let dateEnd   = new Date(dateStart);
        dateEnd.setHours(hourto[0], hourto[1])


        let dateStart2 = new Date(dateStart);
        dateStart2.setHours(hour2from[0], hour2from[1]);

        let dateEnd2   = new Date(dateStart);
        dateEnd2.setHours(hour2to[0], hour2to[1])


        console.log("==============");
        console.log("==============");
        console.log("==============");

        console.log(dateStart+">="+dateStart2);
        console.log(dateStart+">"+dateEnd2);
        console.log("=======");
        console.log(dateEnd+"<="+dateStart2);
        console.log(dateEnd+"<"+dateEnd2);

        console.log("==============");
        console.log("==============");
        console.log("==============");


        if( (dateStart>dateStart2 && dateStart>=dateEnd2 ) || (dateEnd<=dateStart2 && dateEnd<dateEnd2 ) ){
            valid = true;
        }


        return valid;
    }

    function validateHours(hourfrom, hourto)
    {
        hourfrom = hourfrom.split(":");
        hourto   = hourto.split(":");
        let valid  = true;


        let dateStart = new Date();
        dateStart.setHours(hourfrom[0], hourfrom[1]);

        let dateEnd   = new Date(dateStart);
        dateEnd.setHours(hourto[0], hourto[1])


        if(dateStart<dateEnd){
            valid = false;
        }
        

        return valid;

    }

    function checkoruncheck(day, active)
    {
        if(active){
            $(day).iCheck('check'); 
        }else{
            $(day).iCheck('uncheck'); 
        }
    }

    function activeDay2(day, scheduleday, professionalcompany, active){

        let botonmodal;
        let dia;

    
        switch(day){
            case 1:
              console.log("llego aca");
              checkoruncheck("#monday", active);
              console.log("scheduleday: "+scheduleday)
              botonmodal = $("#monday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("monday");
              console.log(professionalcompany);
              console.log(dia);
              dia.dataset.professionalcompany = professionalcompany;

              break;
            case 2:
              //$("#tuesday").iCheck('check');
              checkoruncheck("#tuesday", active);
              botonmodal = $("#tuesday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("tuesday");
              dia.dataset.professionalcompany = professionalcompany;
              break;
            case 3: 
              //$("#wednesday").iCheck('check');
              checkoruncheck("#wednesday", active);
              botonmodal = $("#wednesday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("wednesday");
              dia.dataset.professionalcompany = professionalcompany;
              break;
            case 4:
             // $("#thursday").iCheck('check');
              checkoruncheck("#thursday", active);
              botonmodal = $("#thursday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("thursday");
              dia.dataset.professionalcompany = professionalcompany;
              break; 
            case 5:
              //$("#friday").iCheck('check');
              checkoruncheck("#friday", active);
              botonmodal = $("#friday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("friday");
              dia.dataset.professionalcompany = professionalcompany;
              break;
            case 6:
              //$("#saturday").iCheck('check');
              checkoruncheck("#saturday", active);
              botonmodal = $("#saturday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("saturday");
              dia.dataset.professionalcompany = professionalcompany;
              break; 
            case 7:
              //$("#sunday").iCheck('check');
              checkoruncheck("#sunday", active);
              botonmodal = $("#sunday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              dia  = document.getElementById("sunday");
              dia.dataset.professionalcompany = professionalcompany;
              break;
            default:
              break;
              
          }
    }



    function activeDay(day, scheduleday, active, discount){

        let botonmodal;

    
        switch(day){
            case 1:
              console.log("llego aca");
              checkoruncheck("#monday", active);
              console.log("scheduleday: "+scheduleday)
              botonmodal = $("#monday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break;
            case 2:
              $("#tuesday").iCheck('check');
              checkoruncheck("#tuesday", active);
              botonmodal = $("#tuesday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break;
            case 3: 
              $("#wednesday").iCheck('check');
              checkoruncheck("#wednesday", active);
              botonmodal = $("#wednesday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break;
            case 4:
              $("#thursday").iCheck('check');
              checkoruncheck("#thursday", active);
              botonmodal = $("#thursday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break; 
            case 5:
              $("#friday").iCheck('check');
              checkoruncheck("#friday", active);
              botonmodal = $("#friday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break;
            case 6:
              $("#saturday").iCheck('check');
              checkoruncheck("#saturday", active);
              botonmodal = $("#saturday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break; 
            case 7:
              $("#sunday").iCheck('check');
              checkoruncheck("#sunday", active);
              botonmodal = $("#sunday").parent().parent().parent().parent().find("button.js-modalrange")[0];
              botonmodal.dataset.scheduleday =  scheduleday;
              botonmodal.dataset.discount  = discount
              break;
            default:
              break;
              
          }
    }


    function showMessageAlert(title, text, buttontext){

        return Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: buttontext
        });
    }







