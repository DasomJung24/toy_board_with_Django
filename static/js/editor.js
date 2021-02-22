// create / update editor
ClassicEditor
    .create( document.querySelector( '#editor' ), {
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
        editor = newEditor;
        editor.ui.view.editable.element.style.height = '400px';
    } )
    .catch( error => {
        console.error( error );
    } );
