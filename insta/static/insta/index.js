document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#likebutton').onmouseover = () => {
        document.querySelector('i').style.color = 'red'
        return false;
    };
})