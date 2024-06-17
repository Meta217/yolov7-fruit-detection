document.addEventListener('DOMContentLoaded', function() {
    // 动态设置背景图片
    document.body.style.background = 'url(' + window.location.origin + '/static/background.jpg) no-repeat center center fixed';
    document.body.style.backgroundSize = 'cover';
});

function uploadImage() {
    const input = document.getElementById('uploadInput');
    if (input.files.length > 0) {
        const file = input.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {  // 确保这里的URL指向后端服务器的地址和端口
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const uploadedImage = document.getElementById('uploadedImage');
                const outputImage = document.getElementById('outputImage');

                // 设置上传图片的URL
                uploadedImage.src = `/img/${data.uploaded_image}`;
                
                // 设置识别后图片的URL
                outputImage.src = `/output/${data.output_image}`;
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// 自定义鼠标光标逻辑
var mouse = document.querySelector('.mouse');
window.addEventListener('mousemove', function(event) {    
    mouse.style.left = event.clientX - mouse.offsetWidth / 2 + 'px';
    mouse.style.top = event.clientY - mouse.offsetHeight / 2 + 'px';
});