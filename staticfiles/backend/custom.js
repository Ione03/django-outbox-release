// Custom js for backend (crud process)
// 7 Nop 2022 (Grid software, inc.)

var breakpointDefinition = {
    tablet : 1024,
    phone : 480
};

var responsiveHelper_datatable_tabletools = undefined;

function do_edit(uuid) {            
    window.location.href = "update/"+uuid;
};

function do_delete(uuid, name) {
    if (confirm('Anda yakin menghapus data "'+ name + '"?')) {
        window.location.href = "delete/"+uuid;
    };
};

function do_create(url) {
    $("#do_create").click(function() {
        // url = "{% url 'tags_create' %}"
        window.location.href = url;   
    });
};

function do_cancel(url) {
    $("#do_cancel").click(function() {
        window.location.href = url;   
    });
};

function do_create_table(url) {
    $.ajax({
        "url": url,
        "dataSrc": "",

        success: function(d) {
            var columns = [];                    
            var data = [];
            var res = {};
            var first_loop = true;
            var tmp_data = {};
            var main_col = '';

            for(key in d) {

                if (first_loop) {
                    tmp = Object.keys(d[key]);
                    // console.log(key, tmp);

                    // extra column first
                    // columns.push({"title": "", "data": "icon"});                            

                    for (i in tmp) {
                        if  (tmp[i]=='icon')
                            columns.push({"title": "", "data": tmp[i]});     
                        else
                            columns.push({"title": tmp[i], "data": tmp[i]});     

                        // console.log('i=', i);
                        if (i==3)
                            main_col = tmp[i];
                    };

                    // extra column last
                    // columns.push({"title": "Action", "data": "action"});                               
                        
                    first_loop = !first_loop;                            
                };                        

                // console.log('main = ', main_col);

                tmp_data = d[key];
                tmp_data["icon"] = null;
                tmp_data["action"] = null;                            
                data.push(tmp_data);
            };

            // console.log('column = ', columns)
            // console.log('data = ', data)

            res["columns"] = columns;
            res["data"] = data;
            
            // ref : https://stackoverflow.com/questions/36046139/datatables-dynamic-columns-from-ajax-data-source
            // tidak menggunakan datatable ajax seperti biasa,
            // gunakan ajax di luar, kemudian hasilnya untuk populate datatable

            $('#datatable_tabletools').DataTable({
                // dom: "Bfrtip",
                "data": res.data,
                "columns": res.columns,
                "order": [[ 2, "desc" ]],   
                "columnDefs": [
                    {
                        "targets": [ 1, 2 ],
                        "visible": false,
                        "searchable": false,
                    },  
                    { 
                        "targets": 0, 
                        "width": "5px",
                        "sortable": false,
                        "searchable": false,
                    },
                    { 
                        "targets": [ res.columns.length-2 ], 
                        "width": "100px",
                        "sortable": false,
                        "searchable": false,
                    },
                    {
                        "targets": [ res.columns.length-3 ],
                        
                        render: function(data) {
                            if (data != null) {
                                //console.log( data);
                                return '<img src="/media/' + data + '" class="img-thumbnail">'
                            }
                            else return 'tidak ada'
                        }
                    
                    },  
                    { 
                        "targets": [ res.columns.length-1 ], 
                        "width": "60px",
                        "sortable": false,
                        "searchable": false,                                                            
                        render: function(data, type, row) {                                    
                            // console.log("Object=", Object.keys(res.columns)[0]);
                            // row["Name (id)"]

                            return  "<div class='toolbar text-right'><button onclick='do_edit(\"" + row.uuid + "\");' class='btn btn-success btn-xs' title='Edit Data'> "+
                                    "    <i class='fa fa-edit'></i> "+                                                           
                                    "</button> "+
                                    "<button onclick='do_delete(\"" + row.uuid + "\", \"" + row[main_col] + "\"" + ");' class='btn btn-danger btn-xs' title='Hapus Data'> "+
                                    "    <i class='fa fa-eraser'></i> "+                                                           
                                    "</button>"+
                                    "</div>";
                        }
                    },
                ],
                "sDom": "<'dt-toolbar text-right'<'col-xs-12 col-sm-6 'f><'toolbar'>r>"+                
                        "t"+
                        "<'dt-toolbar-footer'<'col-sm-6 col-xs-12 hidden-xs'i><'col-sm-6 col-xs-12'p>>",      
                "autoWidth" : true,
                
            });
        }
    }); 
};

// PHOTO modification
// ------------------
$(document).ready(function() {

    $("#id_file_path").on("change", function () {
        console.log('enter on file change');

        if (this.files && this.files[0]) {
            console.log('inside trigger photo');
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#form-id").val("photo");
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    var cropBox = {
        left : 0,
        top : 0,
        width : 400, //900, 
        height : 400 //700
    };       
    
    $("#modalCrop").on("show.bs.modal", function () {
        // ww dan hh default sudah ada di masing2 template pemanggil
        // Baca data di interface untuk membedakan ukuran gambar
        // galery layanan ukuran lebih besar

        $(".js-crop-and-upload").removeAttr("disabled").text('Crop and Upload');

        // var banner_position = $("#id_banner-position").val();
        // if (banner_position != null) {
        //     if (banner_position == 'top' || banner_position == 'bottom') {
        //         ww = 728; hh = 90;
        //     }
        //     else {  // middle1 and middle2
        //         ww = 300; hh = 600;
        //     }
        // };        
        // console.log('This is inside crop');
        // console.log('Inside #modalCrop');
        // console.log(ww);
        // console.log(hh);
        
        // acpec ration tidak perlu hh/ww untuk kondisi hh>ww
        var aspect_ratio = ww/hh;
        console.log('aspect ratio', aspect_ratio);
        
        $image.cropper({
            viewMode: 0,    // mode 2 atau 0 untuk resize melewati ukuran gambar
            aspectRatio: aspect_ratio,
            zoomable: true,
            dragMode: 'move',
            center: true,
            cropBoxResizable: true,               

            // rotatable: true,
            // autoCropArea: 0.7,
            // highlight: false,
            // background: false,
            // viewMode: 1,
            // aspectRatio: 1/1,
            // minCropBoxWidth: ww,
            // minCropBoxHeight: hh,
            // width: ww,
            // height: hh,     
            
            ready: function () {                        
                $image.cropper('setCropBoxData', cropBox);                
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);                
            }
        });

    }).on("hidden.bs.modal", function () {
        console.log('on hidden event');
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    $(".js-zoom-in").on("click", function () {
        console.log('inside zoom in');
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").on("click", function () {
    $image.cropper("zoom", -0.1);
    });

    $(".js-move-to-0-0").on("click", function () {
        console.log('inside move 0,0');
        $image.cropper("moveTo", 0.0);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").on("click", function () {
        // $(".js-crop-and-upload").text('Waiting...');
        $(".js-crop-and-upload").attr("disabled", true).text('Processing ...');

        var cropData = $image.cropper("getData");
        var formID = $("#form-id").val();
        var canvas = $image.cropper("getCroppedCanvas");

        // console.log(canvas);        
        // console.log('Inside #js-crop-and-upload');
        // console.log(ww);
        // console.log(hh);

        canvas.toBlob(function (blob) {
            var formData = new FormData();

            formData.append('photo', blob);          
            // console.log(blob);            
            let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            // console.log(csrftoken);

            console.log('value before upload = ');
            console.log($("#id_file_path").val());
            console.log(formID);

            // var arr_idx = formID.split('-');
            // var idx = 0;
            // if (arr_idx.length >= 2)
            //     idx = arr_idx[1]

            // formData.append('old_photo', file_path[idx]);

            $.ajax('/dashboard/upload-photo/' + ww + '/' + hh + '/', {
                method: "POST",
                data: formData,
                processData: false,
                contentType: false,
                async: false,       // set false for waiting result, set time out too, to make limit time waiting
                cache: false,
                timeout: 30000,

                headers:{'X-CSRFToken':csrftoken},

                success: function (response) {
                    console.log('response = ');
                    console.log(response);
                    // file_path[idx] = response;
                    // $("#id_file_path").val(response);                    
                    // $('#id_str_file_path').val(response);
                    // alert($('#id_str_file_path').val());

                    $("#id_str_file_path").val(response);

                    //alert('done');

                    // console.log('outside canvas blob')
                    // console.log('result');
                    // console.log(cropData["x"]);
                    // console.log(cropData["y"]);
                    // console.log(cropData["height"]);
                    // console.log(cropData["width"]);
                    
                    // $("#id_"+ formID +"-x").val(cropData["x"]);
                    // $("#id_"+ formID +"-y").val(cropData["y"]);
                    // $("#id_"+ formID +"-height").val(cropData["height"]);
                    // $("#id_"+ formID +"-width").val(cropData["width"]);

                    //$("#formUpload").submit();
                    $("#modalCrop").modal('hide');
                },

                error: function () {
                    console.log('Upload error');
                }
            });

            //alert('after call ajax');
        });                

        // console.log('outside canvas blob')
        // console.log('result');
        // console.log(cropData["x"]);
        // console.log(cropData["y"]);
        // console.log(cropData["height"]);
        // console.log(cropData["width"]);
        
        // $("#id_"+ formID +"-x").val(cropData["x"]);
        // $("#id_"+ formID +"-y").val(cropData["y"]);
        // $("#id_"+ formID +"-height").val(cropData["height"]);
        // $("#id_"+ formID +"-width").val(cropData["width"]);

        // //$("#formUpload").submit();
        // $("#modalCrop").modal('hide');
    });
});   