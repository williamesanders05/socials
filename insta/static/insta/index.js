document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#likebutton').onclick = () => {
        document.querySelector('#numlikes').style.color = 'red'
    };
})