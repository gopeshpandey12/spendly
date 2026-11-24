// "See how it works" video modal — vanilla JS, no dependencies.
(function () {
    var modal = document.getElementById("video-modal");
    var openBtn = document.querySelector("[data-video-open]");
    if (!modal || !openBtn) return;

    var dialog = modal.querySelector(".lp-modal-dialog");
    var closeBtn = modal.querySelector("[data-video-close]");
    var iframe = modal.querySelector("iframe");

    function openModal() {
        // Load the video only when opened, so it starts fresh each time.
        iframe.src = iframe.dataset.src;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        closeBtn.focus();
    }

    function closeModal() {
        if (modal.hidden) return;
        modal.hidden = true;
        // Removing the src unloads the player, which stops playback completely.
        iframe.removeAttribute("src");
        document.body.style.overflow = "";
        openBtn.focus();
    }

    openBtn.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);

    // Clicking the dark overlay (anywhere outside the dialog) closes it.
    modal.addEventListener("click", function (event) {
        if (!dialog.contains(event.target)) closeModal();
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") closeModal();
    });
})();
