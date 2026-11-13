// Mobile navigation toggle. The site works without this file:
// with JavaScript off, the full navigation stays visible.
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nav.classList.toggle("is-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  // Close after choosing a link (same-page anchors on mobile).
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setOpen(false);
  });

  // Escape closes the menu and returns focus to the button.
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  // Reset when the window grows past the mobile breakpoint.
  var mq = window.matchMedia("(min-width: 1080px)");
  var onChange = function () { if (mq.matches) setOpen(false); };
  if (mq.addEventListener) mq.addEventListener("change", onChange);
  else if (mq.addListener) mq.addListener(onChange);
})();

// Automation audit form: validates, then sends the answers.
// If the form posts to Formspree, it is sent in the background (fetch) and the visitor stays on the page.
// Otherwise (or if sending fails) it opens the visitor's email app with the answers filled in.
// Without JavaScript the form still submits normally to its action.
(function () {
  "use strict";
  var form = document.getElementById("audit-form");
  if (form) {
    var errorBox = document.getElementById("form-error");
    var status = document.getElementById("form-status");
    var button = form.querySelector('button[type="submit"]');
    var buttonHtml = button ? button.innerHTML : "";
    var to = form.getAttribute("data-email") || "meetwith.waqarahmed@gmail.com";
    var useFormspree = /^https:\/\/formspree\.io\/f\/[A-Za-z0-9]+$/.test(form.getAttribute("action") || "");
    var busy = false;

    var v = function (id) { return document.getElementById(id).value.trim(); };

    function mailtoHref() {
      var lines = [
        "Automation audit request",
        "",
        "Full name: " + v("f-name"),
        "Work email: " + v("f-email"),
        "Phone or WhatsApp: " + (v("f-phone") || "not given"),
        "Trade type: " + v("f-trade"),
        "Help with: " + v("f-help"),
        "",
        "Primary bottleneck:",
        v("f-bottleneck"),
        "",
        "Contact consent (transactional): yes",
        "Marketing tips consent: " + (document.getElementById("f-marketing").checked ? "yes" : "no")
      ];
      return "mailto:" + to + "?subject=" + encodeURIComponent("Automation audit request: " + v("f-help")) +
        "&body=" + encodeURIComponent(lines.join("\n"));
    }

    function showError(msg, withEmailLink) {
      errorBox.textContent = msg;
      if (withEmailLink) {
        errorBox.appendChild(document.createTextNode(" "));
        var a = document.createElement("a");
        a.href = mailtoHref();
        a.textContent = "Send it from your email app instead";
        errorBox.appendChild(a);
        errorBox.appendChild(document.createTextNode(", or email " + to + "."));
        // One-click copy of the address, so a visitor can still reach me if sending fails
        var copy = document.createElement("button");
        copy.type = "button";
        copy.className = "btn btn--quiet btn--small copy-btn";
        copy.textContent = "Copy " + to;
        var said = document.createElement("span");
        said.className = "small copy-status";
        said.setAttribute("role", "status");
        copy.addEventListener("click", function () {
          var ok = function () { said.textContent = " Email address copied."; };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(to).then(ok, function () { said.textContent = " Copy failed. Please type " + to + "."; });
          } else { said.textContent = " Please copy " + to + "."; }
        });
        errorBox.appendChild(document.createElement("br"));
        errorBox.appendChild(copy);
        errorBox.appendChild(said);
      }
      errorBox.hidden = false;
    }

    function setBusy(on) {
      busy = on;
      if (!button) return;
      button.disabled = on;
      button.setAttribute("aria-busy", on ? "true" : "false");
      if (on) button.textContent = "Sending...";
      else button.innerHTML = buttonHtml;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (busy) return;
      var invalid = [];
      Array.prototype.forEach.call(form.querySelectorAll("[required]"), function (el) {
        var ok = el.type === "checkbox" ? el.checked : el.value.trim() !== "" && el.checkValidity();
        el.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) invalid.push(el);
      });
      if (invalid.length) {
        showError("Please complete the highlighted fields and agree to be contacted.");
        invalid[0].focus();
        return;
      }
      errorBox.hidden = true;
      status.textContent = "";

      if (!useFormspree || !window.fetch || !window.FormData) {
        window.location.href = mailtoHref();
        status.textContent = "Your email app should open with your request filled in. If it doesn't, email " + to + " directly.";
        return;
      }

      var data = new FormData(form);
      data.set("Marketing consent", document.getElementById("f-marketing").checked ? "Yes" : "No");
      data.set("_subject", "Automation audit request: " + v("f-help") + " / " + v("f-trade"));
      setBusy(true);
      status.textContent = "Sending your request...";

      fetch(form.action, { method: "POST", body: data, headers: { "Accept": "application/json" } })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            Array.prototype.forEach.call(form.querySelectorAll("[aria-invalid]"), function (el) { el.removeAttribute("aria-invalid"); });
            status.textContent = "Thank you. Your audit request was sent to " + to + ". I will reply by email.";
            status.setAttribute("tabindex", "-1");
            status.focus();
            return;
          }
          return res.json().catch(function () { return {}; }).then(function (body) {
            status.textContent = "";
            if (res.status === 429) {
              showError("Too many requests just now. Please wait a minute and try again.", true);
            } else if (body && body.errors && body.errors.length) {
              showError(body.errors.map(function (x) { return x.message; }).join(". ") + ".", true);
            } else {
              showError("Sorry, your request could not be sent.", true);
            }
          });
        })
        .catch(function () {
          status.textContent = "";
          showError("Sorry, your request could not be sent. Check your connection and try again.", true);
        })
        .then(function () { setBusy(false); });
    });
  }

  // Copy-email buttons
  Array.prototype.forEach.call(document.querySelectorAll(".copy-btn"), function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var out = btn.parentNode.querySelector(".copy-status");
      var done = function () { if (out) out.textContent = "Email address copied."; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { if (out) out.textContent = "Copy failed. Select the address above instead."; });
      } else {
        var r = document.createRange(); var a = document.getElementById("biz-email");
        r.selectNodeContents(a); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        if (out) out.textContent = "Address selected. Press Ctrl+C to copy.";
      }
    });
  });
})();

// Cost calculator: arithmetic on the visitor's own numbers. Hidden without JavaScript.
(function () {
  "use strict";
  var box = document.getElementById("calc");
  if (!box) return;
  var visits = document.getElementById("c-visits"), mins = document.getElementById("c-min"), rate = document.getElementById("c-rate");
  var hoursOut = document.getElementById("c-hours"), costOut = document.getElementById("c-cost");
  function num(el) { var n = parseFloat(el.value); return isFinite(n) && n > 0 ? n : 0; }
  function update() {
    var hours = num(visits) * 52 / 12 * num(mins) / 60;
    hoursOut.textContent = hours >= 10 ? Math.round(hours) : Math.round(hours * 10) / 10;
    var r = num(rate);
    costOut.textContent = r ? "About " + Math.round(hours * r).toLocaleString("en") + " a month at that hourly cost." : "";
  }
  [visits, mins, rate].forEach(function (el) { el.addEventListener("input", update); });
  box.querySelector("form").addEventListener("submit", function (e) { e.preventDefault(); });
  box.hidden = false;
  update();
})();
