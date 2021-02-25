// comment 입력 에디터
ClassicEditor
    .create( document.querySelector( '#editor-comment' ), {
        extraPlugins: [MyCustomUploadAdapterPlugin],
        image: {
            toolbar: [
                'imageStyle:alignLeft',
                'imageStyle:full',
                'imageStyle:alignRight',
                'imageTextAlternative',
            ],
            styles: [
                "full",
                "alignLeft",
                "alignRight"
            ]
        },
    })
    .then( newEditor => {
        editorComment = newEditor;
    } )
    .catch( error => {
        console.error( error );
    } );

// comment editor
$(document).ready( function () {
    var commentAll = document.querySelectorAll( '.editor-comment' )
    var replyAll = document.querySelectorAll( '.editor-reply')

    for (let i=0; i < commentAll.length; i++ ) {
        ClassicEditor
            .create(commentAll[i], {
                extraPlugins: [MyCustomUploadAdapterPlugin],
                image: {
                    toolbar: [
                        'imageStyle:alignLeft',
                        'imageStyle:full',
                        'imageStyle:alignRight',
                        'imageTextAlternative',
                    ],
                    styles: [
                        "full",
                        "alignLeft",
                        "alignRight",
                    ]
                },
            })
            .then(newEditor => {
                editorCommentRead = newEditor;
            })
            .catch(error => {
                console.error(error);
            });

    }

    for (let i=0; i < replyAll.length; i++ ) {
        ClassicEditor
            .create(replyAll[i], {
                extraPlugins: [MyCustomUploadAdapterPlugin],
                image: {
                    toolbar: [
                        'imageStyle:alignLeft',
                        'imageStyle:full',
                        'imageStyle:alignRight',
                        'imageTextAlternative',
                    ],
                    styles: [
                        "full",
                        "alignLeft",
                        "alignRight"
                    ]
                },
            })
            .then(newEditor => {
                editorComment = newEditor;
            })
            .catch(error => {
                console.error(error);
            });
    }
});
