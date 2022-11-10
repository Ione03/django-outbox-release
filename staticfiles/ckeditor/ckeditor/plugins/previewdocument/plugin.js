/*
 Copyright (c) 2003-2015, CKSource - Iwan Setiawan. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/

CKEDITOR.plugins.add( 'previewdocument', {
    icons: 'previewdocument',
    // requires: 'widget',

    init: function( editor ) {
        // editor.addCommand( 'insertScriptDocument', {
        //     exec: function( editor ) {
        //         var now = new Date();
        //         editor.insertHtml( 'The current date and time is: <em>' + now.toString() + '</em>' );
        //     }
        // });

        // Create command
        editor.addCommand( 'insertScriptDocument', 
            new CKEDITOR.dialogCommand( 'getURLDocument' ) );

        // Create button
        editor.ui.addButton( 'PreviewDocument', {
            label: 'Preview Document',
            command: 'insertScriptDocument',
            toolbar: 'insert'
        });

        CKEDITOR.dialog.add( 'getURLDocument', this.path + 'dialogs/getURLDocument.js' );
    }
});


// (function () {
//     CKEDITOR.plugins.add("previewdocument", {
//         icons: "previewdocument",
//         // hidpi: !0,
//         requires: "embedbase",
//         onLoad: function () {
//             this.registerOembedTag();
//         },
//         init: function (a) {
//             var b = CKEDITOR.plugins.embedBase.createWidgetBaseDefinition(a),
//                 d = b.init;
//             CKEDITOR.tools.extend(
//                 b,
//                 {
//                     dialog: "embedBase",
//                     button: a.lang.embedbase.button,
//                     allowedContent: "oembed",
//                     requiredContent: "oembed",
//                     styleableElements: "oembed",
//                     providerUrl: new CKEDITOR.template(a.config.embed_provider || "//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}"),
//                     init: function () {
//                         var e = this;
//                         d.call(this);
//                         this.once("ready", function () {
//                             this.data.loadOnReady &&
//                                 this.loadContent(this.data.url, {
//                                     callback: function () {
//                                         e.setData("loadOnReady", !1);
//                                         a.fire("updateSnapshot");
//                                     },
//                                 });
//                         });
//                     },
//                     upcast: function (a, b) {
//                         if ("oembed" == a.name) {
//                             var c = a.children[0];
//                             if (c && c.type == CKEDITOR.NODE_TEXT && c.value)
//                                 return (b.url = c.value), (b.loadOnReady = !0), (c = new CKEDITOR.htmlParser.element("div")), a.replaceWith(c), (c.attributes["class"] = a.attributes["class"]), c;
//                         }
//                     },
//                     downcast: function (a) {
//                         var b = new CKEDITOR.htmlParser.element("oembed");
//                         b.add(new CKEDITOR.htmlParser.text(this.data.url));
//                         a.attributes["class"] && (b.attributes["class"] = a.attributes["class"]);
//                         return b;
//                     },
//                 },
//                 !0
//             );
//             a.widgets.add("PreviewDocument", b);
//         },
//         registerOembedTag: function () {
//             var a = CKEDITOR.dtd,
//                 b;
//             a.oembed = { "#": 1 };
//             for (b in a) a[b].div && (a[b].oembed = 1);
//         },
//     });
// })();
