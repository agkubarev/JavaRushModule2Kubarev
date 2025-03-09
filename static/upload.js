function ekUpload(){
    function Init() {

        console.log("Upload Initialised");

        var fileSelect = document.getElementById('file-upload'),
            fileDrag = document.getElementById('file-drag');
//            submitButton = document.getElementById('submit-button');

        fileSelect.addEventListener('change', fileSelectHandler, false);

        var xhr = new XMLHttpRequest();
        if (xhr.upload) {
            fileDrag.addEventListener('dragover', fileDragHover, false);
            fileDrag.addEventListener('dragleave', fileDragHover, false);
            fileDrag.addEventListener('drop', fileSelectHandler, false);
        }
    }

    function fileDragHover(e) {
        var fileDrag = document.getElementById('file-drag');

        e.stopPropagation();
        e.preventDefault();

        fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
    }

    function fileSelectHandler(e) {
        var files = e.target.files || e.dataTransfer.files;

        fileDragHover(e);

//        for (var i = 0, f; f = files[i]; i++) {
//            console.log(f.name);
//            console.log(f);
//            parseFile(f);
//            var form = document.getElementById('file-upload-form');
//            form.method = 'POST';
////            enctype="multipart/form-data" id="file-upload-form" class="uploader" action="/upload"
//            form.action = '/upload';
//            form.enctype = 'multipart/form-data';
//            form.append('image', f);
//            console.log('form submit');
//            form.submit();
////            uploadFile(f);
//        }
        if (files.length > 0) {
          const data = new FormData();
          for (const file of files) {
            parseFile(file);
            data.append('image', file);
          }

          fetch('/upload', {
            method: 'POST',
            body: data
          })
          .then(() => console.log("file uploaded"))
          .catch(reason => console.error(reason));
       }
    }

    function output(msg) {
        var m = document.getElementById('messages');
        m.innerHTML = msg;
    }

    function parseFile(file) {

        console.log(file.name);
        output(
        '<strong>' + encodeURI(file.name) + '</strong>'
        );

        var imageName = file.name;

        var isGood = (/\.(?=gif|jpg|png|jpeg)/gi).test(imageName);
        if (isGood) {
            document.getElementById('start').classList.add("hidden");
            document.getElementById('response').classList.remove("hidden");
            document.getElementById('notimage').classList.add("hidden");
            // Thumbnail Preview
            document.getElementById('file-image').classList.remove("hidden");
            document.getElementById('file-image').src = URL.createObjectURL(file);
       }
       else {
            document.getElementById('file-image').classList.add("hidden");
            document.getElementById('notimage').classList.remove("hidden");
            document.getElementById('start').classList.remove("hidden");
            document.getElementById('response').classList.add("hidden");
            document.getElementById("file-upload-form").reset();
       }
    }

//    function setProgressMaxValue(e) {
//        var pBar = document.getElementById('file-progress');
//
//        if (e.lengthComputable) {
//            pBar.max = e.total;
//        }
//    }

//    function updateFileProgress(e) {
//        var pBar = document.getElementById('file-progress');
//
//        if (e.lengthComputable) {
//            pBar.value = e.loaded;
//        }
//    }

//    function uploadFile(file) {
//
//        var xhr = new XMLHttpRequest(),
//            fileInput = document.getElementById('class-roster-file'),
//        pBar = document.getElementById('file-progress'),
//        fileSizeLimit = 1024;
//        console.log(fileInput);
//        if (xhr.upload) {
//            if (file.size <= fileSizeLimit * 1024 * 1024) {
//                pBar.style.display='inline' ;
//                xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
//                xhr.upload.addEventListener('progress', updateFileProgress, false);
//                xhr.onreadystatechange=function(e) {
//                    if (xhr.readyState==4) { }
//                };
//                console.log('POST')
//                xhr.open('POST', document.getElementById('file-upload-form').action, true);
//                xhr.setRequestHeader('X-File-Name', file.name);
//                xhr.setRequestHeader('X-File-Size', file.size);
//                xhr.setRequestHeader('Content-Type', 'multipart/form-data' );
//                console.log(`send file ${file}`)
//                xhr.send(file);
//                console.log('after send file')
//            }
//            else {
//                output('Please upload a smaller file (< ' + fileSizeLimit + ' MB).');
//            }
//        }
//    }
    if (window.File && window.FileList && window.FileReader) {
        Init();
    }
    else {
        document.getElementById('file-drag').style.display='none' ;
    }
}
ekUpload();