"use strict";

(function () {
  if (window.__bcClickPopToggleLoaded) {
    return;
  }
  window.__bcClickPopToggleLoaded = true;

  var BUTTON_SELECTOR = ".formio-form .btn:not(:disabled):not([disabled])";
  var POP_CLASS = "bc-click-pop";
  var POP_ANIMATION = "bcBtnClickPopFixed";

  function closestButton(node) {
    if (!node || typeof node.closest !== "function") {
      return null;
    }
    return node.closest(BUTTON_SELECTOR);
  }

  function triggerPop(button) {
    button.classList.remove(POP_CLASS);
    void button.offsetWidth;
    button.classList.add(POP_CLASS);
  }

  document.addEventListener(
    "click",
    function (event) {
      var button = closestButton(event.target);
      if (!button) {
        return;
      }
      triggerPop(button);
    },
    true
  );

  document.addEventListener(
    "animationend",
    function (event) {
      if (event.animationName !== POP_ANIMATION) {
        return;
      }
      var button = closestButton(event.target);
      if (!button) {
        return;
      }
      button.classList.remove(POP_CLASS);
    },
    true
  );
})();
