CKEDITOR.dialog.add( 'getURLDocument', function( editor ) {
    var urlreg=/(([\w]+:)?\/\/)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,63}(:[\d]+)?(\/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?/;

    return {
        title: 'Preview Document',
        minWidth: 400,
        minHeight: 50,
        contents: [
            {
                id: 'tab-basic',
                // label: 'Basic Settings',
                elements: [
                    {
                        type: 'text',
                        id: 'id_file',
                        label: 'URL Document',
                        validate: CKEDITOR.dialog.validate.regex(urlreg, "URL tidak dikenal." )
                    },
                    // {
                    //     type: 'text',
                    //     id: 'title',
                    //     label: 'Explanation',
                    //     validate: CKEDITOR.dialog.validate.notEmpty( "Explanation field cannot be empty." )
                    // }
                ]
            },
            // {
            //     id: 'tab-adv',
            //     label: 'Advanced Settings',
            //     elements: [
            //         {
            //             type: 'text',
            //             id: 'id',
            //             label: 'Id'
            //         }
            //     ]
            // }
        ],
        onOk: function() {
            var dialog = this;

            // var id_file = editor.document.createElement( 'id_file' );
            // id_file.setAttribute( 'title', dialog.getValueOf( 'tab-basic', 'title' ) );
            // id_file.setText( dialog.getValueOf( 'tab-basic', 'abbr' ) );

            editor.insertHtml( 
                '<div class="embed-responsive embed-responsive-1by1">' +
                    '<iframe class="embed-responsive-item" frameborder="0" ' +
                        'src="https://docs.google.com/gview?url=' + 
                        dialog.getValueOf( 'tab-basic', 'id_file' ) + 
                        '&embedded=true">' +
                    '</iframe>' +
                '</div>'

                //'<div class="embed-responsive embed-responsive-1by1">' +
                //    '<iframe class="embed-responsive-item" frameborder="0" ' +
                //        'src="https://drive.google.com/file/d/' + dialog.getValueOf( 'tab-basic', 'id_file' ) + '/preview">' +
                //    '</iframe>' +
                //'</div>'
    
            );
    

            // var id = dialog.getValueOf( 'tab-adv', 'id' );
            // if ( id )
            //     abbr.setAttribute( 'id', id );

            // editor.insertElement( abbr );
        }
    };
});