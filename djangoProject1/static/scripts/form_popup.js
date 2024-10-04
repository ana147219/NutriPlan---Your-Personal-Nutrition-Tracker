$(document).ready(function() {

    function disableScroll() {
        document.body.style.overflow = "hidden";
    }

    function enableScroll() {
        document.body.style.overflow = "auto";
    }

    /*=============== SHOW MODAL ===============*/

    document.querySelectorAll(".window_trigger").forEach(function(element) {
        element.addEventListener("click", function() {
            disableScroll();

            document.getElementById('publish-modal-container').classList.add('show-modal');
            event.preventDefault();

        });
    });




    /*=============== CLOSE MODAL ===============*/
    const closeBtn = document.querySelectorAll('.close-modal');

    function closeModal(){
        enableScroll();
        const modalContainer = document.getElementById('publish-modal-container');
        modalContainer.classList.remove('show-modal');
    }
    closeBtn.forEach(c => c.addEventListener('click', closeModal));
});