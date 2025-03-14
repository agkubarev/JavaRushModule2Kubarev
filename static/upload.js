function ekUpload(){
    function Init() {

        console.log("Upload Initialised");

        var fileSelect = document.getElementById('file-upload'),
            fileDrag = document.getElementById('file-drag');

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

        if (files.length > 0) {
          const data = new FormData();
          const file = files[0];
          parseFile(file);
          data.append('image', file);
          fetch('/upload', {
            method: 'POST',
            body: data
          })
          .then(() => { console.log("file uploaded");
                        output(
                        '<strong>' + 'Файл загружен' + '</strong>' );
                      })
          .catch(reason => console.error(reason));
       }
    }

    function output(msg) {
        var m = document.getElementById('messages');
        m.innerHTML = msg;
    }

    function parseFile(file) {

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

    if (window.File && window.FileList && window.FileReader) {
        Init();
    }
    else {
        document.getElementById('file-drag').style.display='none' ;
    }
}
ekUpload();