/* NoteKeeper — small progressive-enhancement helpers (vanilla JS). */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss flash messages after a few seconds.
    var alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
      window.setTimeout(function () {
        // Use Bootstrap's Alert API when available for a smooth fade-out.
        if (window.bootstrap && window.bootstrap.Alert) {
          var instance = window.bootstrap.Alert.getOrCreateInstance(alert);
          instance.close();
        } else {
          alert.style.display = "none";
        }
      }, 4000);
    });

    // Live character counter for the note title field, if present.
    var titleInput = document.getElementById("title");
    if (titleInput && titleInput.maxLength > 0) {
      var counter = document.createElement("small");
      counter.className = "text-muted d-block mt-1";

      var update = function () {
        counter.textContent =
          titleInput.value.length + " / " + titleInput.maxLength;
      };

      update();
      titleInput.addEventListener("input", update);
      titleInput.insertAdjacentElement("afterend", counter);
    }
  });
})();
