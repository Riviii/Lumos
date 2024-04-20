var highlighted = false;

        function highlightContent() {
            var content = document.getElementsByTagName("a", "h1", "h2", "h3", "h4")[0];
            content.classList.toggle("highlight");
            highlighted = !highlighted;
        }

        document.addEventListener("mouseover", function (event) {
            if (highlighted && event.target.tagName !== "BUTTON") {
                event.target.classList.add("highlight");
            }
        });

        document.addEventListener("mouseout", function (event) {
            if (highlighted && event.target.tagName !== "BUTTON") {
                event.target.classList.remove("highlight");
            }
        });

document.addEventListener('DOMContentLoaded', function () {
    const selectWarning = document.getElementById('select-warning');
    const copyWarning = document.getElementById('copy-warning');

    function showSelectWarning() {
        selectWarning.style.display = 'block';
        setTimeout(function () {
            selectWarning.style.display = 'none';
        }, 2000);
    }

    function showCopyWarning() {
        copyWarning.style.display = 'block';
        setTimeout(function () {
            copyWarning.style.display = 'none';
        }, 2000); 
    }

    document.addEventListener('mousedown', function (event) {
        if (event.button === 2) { 
            document.addEventListener('contextmenu', showSelectWarningOnce);
        }
    });

    function showSelectWarningOnce(event) {
        showSelectWarning();
        event.preventDefault();
        document.removeEventListener('contextmenu', showSelectWarningOnce);
    }

    document.addEventListener('copy', function (event) {
        event.preventDefault(); 
        showCopyWarning();
    });
});