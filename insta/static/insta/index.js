// first we make sure to run this javascript after the html has loaded
document.addEventListener('DOMContentLoaded', function() {
    //make the heart button red when hovered and clicked
    document.querySelector('#likebutton').onmouseover = () => {
        document.querySelector('i').style.color = 'red'
        return false;
    };
})