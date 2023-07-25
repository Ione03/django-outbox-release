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

// sender = sumber form [form create atau update]
function do_cancel(selector, sender, url) {
    $(selector).click(function() {
        if (confirm('Batalkan proses "'+ sender + '"?')) {
            window.location.href = url;   
        };
    });
};

function do_create_table(url, one_record_only=false, edit_button=true, delete_button=true) {
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
            var foto_idx = -1;   // # cari index 

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
                        // console.log('=',tmp[i]);
                        if (i==3)
                            main_col = tmp[i];

                        if (tmp[i]=='Foto') {
                            foto_idx = i;
                            console.log('foto idx change', i);
                        };

                        console.log('=',foto_idx);
                    };

                    // extra column last
                    // columns.push({"title": "Action", "data": "action"});                               
                        
                    first_loop = !first_loop;                            
                };                        

                // console.log('main = ', main_col);

                tmp_data = d[key];
                tmp_data["icon"] = null;
                tmp_data["action"] = null;     
                
                // clear html tag in tmp_data:
                //console.log('tmp_data',tmp_data[j]);
                
                
                for (j in tmp_data) {                
                    //console.log('tmp_data[j]',tmp_data[j] );
                    if (!((tmp_data[j] == null) || (typeof tmp_data[j] != "string"))) {
                        tmp_data[j] = tmp_data[j].replace(/<\/?("[^"]*"|'[^']*'|[^>])*(>|$)/g, "");                    
                    };
                };
                //console.log('tmp_data',tmp_data);
                                
                data.push(tmp_data);
            };

            //console.log('column = ', columns);
            //console.log('data = ', data);

            res["columns"] = columns;
            res["data"] = data;
            
            //console.log('data',data);
            
            if (one_record_only)
                if (data.length >= 1)
                    $("#do_create").hide();
                    
            // ref : https://stackoverflow.com/questions/36046139/datatables-dynamic-columns-from-ajax-data-source
            // tidak menggunakan datatable ajax seperti biasa,
            // gunakan ajax di luar, kemudian hasilnya untuk populate datatable

            // console.log('foto_idx', foto_idx);

            // {% if one_record_only %}
            //     $("#do_create").hide();
            // {% endif %}

            // console.log('res.data=', res.data);

            if (res.data.length>0) {
                $('#datatable_tabletools').DataTable({
                    // dom: "Bfrtip",
                    "deferRender": true,    // for lazy load data (load per page)
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
                            // manfaatkan kondisi target yg harus integer, jika string maka tidak akan di jalankna
                            "targets": [ (foto_idx > -1) ? parseInt(foto_idx): '-1' ],
                            
                            render: function(data) {
                                // console.log('inside target');
                                // console.log(foto_idx);

                                // if (foto_idx > -1) {
                                if (data != null)                                     
                                    return  '<img src="/media/' + data + 
                                            '" class="img-thumbnail">';
                                
                                return 'tidak ada';                                
                            }                    
                        },  
                        {
                            // tampilkan hiperlink di kolom pertama (agar dapat melakukan editing dengan klik field 1)
                            "targets": [ 3 ],
                            
                            render: function(data, type, row) {                            
                                return  "<a href='javascript:void(0);' onclick='do_edit(\"" + row.uuid + "\");' title='Edit Data'>"+ 
                                        "<strong>" + data + "</strong>" +
                                        "</a>";                                
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
                                var tmp = '';
                                var row_value = row[main_col];
                                
                                // clear apostrope and quoted mark
                                row_value = row_value.replaceAll("'","");
                                row_value = row_value.replaceAll("\"","");                                                                
                                
                                if (edit_button)
                                    tmp =   "<button onclick='do_edit(\"" + row.uuid + "\");' class='btn btn-success btn-xs' title='Edit Data'> "+
                                            "    <i class='fa fa-edit'></i> "+                                                           
                                            "</button> ";

                                if (delete_button)
                                    tmp = tmp +
                                            "<button onclick='do_delete(\"" + row.uuid + "\", \"" + 
                                            row_value + "\"" + ");' class='btn btn-danger btn-xs' title='Hapus Data'> "+
                                            "    <i class='fa fa-eraser'></i> "+                                                           
                                            "</button>";

                                return  "<div class='toolbar text-right'>" + tmp +
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
            else {
                // console.log($("#no-data").val());

                $("#no-data").empty();
                $("#no-data").append(
                    '<p class="alert alert-info no-margin">' +
                        'No data to display ...  '+
                    '</p>');
            };

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
    var ww = 0;
    var hh = 0; 
    
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
        // console.log("DIMENSI:");
        // console.log($("#id_dim_w").val());
        // console.log($("#id_dim_h").val());
        // DImensi ini di buat di form masing2
        
        
        
        ww = $("#id_dim_w").val();
        hh = $("#id_dim_h").val();
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

        var save_as_png = $("#id_save_as_png").val();
        console.log('save_as_png=', save_as_png);

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
            var tmp = '';
            if (save_as_png=="1") {                
                tmp = '1/';            
                console.log('do save as png');
            };

            $.ajax('/dashboard/upload-photo/' + ww + '/' + hh + '/' + tmp, {
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
