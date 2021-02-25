jQuery.fn.serializeObject = function() {
    var obj = null;
    try {
        if (this[0].tagName && this[0].tagName.toUpperCase() == "FORM") {
            var arr = this.serializeArray();
            if (arr) {
                obj = {};
                jQuery.each(arr, function() {
                    obj[this.name] = this.value;
                });
            }
        }
    } catch (e) {
        alert(e.message);
    } finally {
    }

    return obj;
};

class UploadAdapter {
		// 새 플러그인 인스턴스를 만든다. 플러그인 초기화의 첫 번째 단계
		constructor(loader) {
			this.loader = loader;
		}

		upload() {
			return this.loader.file.then( file => new Promise(((resolve, reject) => {
				this._initRequest();
				this._initListeners( resolve, reject, file );
				this._sendRequest( file );
			})))
		}

		_initRequest() {
			const xhr = this.xhr = new XMLHttpRequest();

			xhr.open('POST', '/board/posts/file-upload', true);
			xhr.responseType = 'json';
		}

		_initListeners(resolve, reject, file) {
			const xhr = this.xhr;
			const loader = this.loader;
			const genericErrorText = '파일을 업로드 할 수 없습니다.'

			xhr.addEventListener('error', () => {reject(genericErrorText)})
			xhr.addEventListener('abort', () => reject())
			xhr.addEventListener('load', () => {
				const response = xhr.response
				if(!response || response.error) {
					return reject( response && response.error ? response.error.message : genericErrorText );
				}

				resolve({
					default: response.url
				})
			})
			// 업로드 모니터링
			if ( xhr.upload ) {
            xhr.upload.addEventListener( 'load', evt => {
                if ( evt.lengthComputable ) {
                    loader.uploadTotal = evt.total;
                    loader.uploaded = evt.loaded;
                }
            } );
        }
		}
		_sendRequest(file) {
			const data = new FormData()
			data.append('file',file)
			data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value)
			this.xhr.send(data)
		}
	}
	function MyCustomUploadAdapterPlugin(editor) {
		editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
			return new UploadAdapter(loader)
		}
	}