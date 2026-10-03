// Lógica de instalação PWA: computador + celular (Android/iOS).
(function () {
  var installBtn = document.getElementById("install-btn");
  var helpBtn = document.getElementById("install-help-btn");
  var banner = document.getElementById("install-banner");
  var bannerInstall = document.getElementById("banner-install");
  var bannerHelp = document.getElementById("banner-help");
  var bannerClose = document.getElementById("banner-close");
  var dialog = document.getElementById("install-dialog");
  var detected = document.getElementById("install-detected");
  var deferredPrompt = null;

  function isIos() {
    return /iphone|ipad|ipod/i.test(navigator.userAgent) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  }
  function isSamsung() { return /samsungbrowser/i.test(navigator.userAgent); }
  function isAndroid() { return /android/i.test(navigator.userAgent); }
  function isMobile() { return isAndroid() || isIos() || /mobi/i.test(navigator.userAgent); }

  function detectPlatform() {
    if (isIos()) return "iphone";
    if (isSamsung()) return "samsung";
    if (isAndroid()) return "android-chrome";
    return "desktop";
  }

  function isStandalone() {
    return window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches ||
      window.navigator.standalone === true;
  }

  function show(el) { if (el) el.style.display = "inline-block"; }
  function hide(el) { if (el) el.style.display = "none"; }

  function highlightStep() {
    var p = detectPlatform();
    var steps = document.querySelectorAll(".install-step");
    steps.forEach(function (s) {
      s.classList.toggle("active", s.getAttribute("data-platform") === p);
    });
    var names = {
      "android-chrome": "Detectado: Android Chrome",
      "samsung": "Detectado: Samsung Internet",
      "iphone": "Detectado: iPhone Safari",
      "desktop": "Detectado: computador"
    };
    if (detected) detected.textContent = names[p] || "";
  }

  function statusMsg(msg) {
    document.querySelectorAll(".js-install-status").forEach(function (el) {
      el.textContent = msg;
    });
  }

  function refreshUI() {
    highlightStep();
    if (isStandalone()) {
      hide(installBtn); hide(banner); hide(helpBtn);
      return;
    }
    if (deferredPrompt) {
      show(installBtn);
      show(helpBtn);
      if (banner && !localStorage.getItem("sebo-install-dismissed")) banner.style.display = "flex";
      statusMsg("");
    } else {
      hide(installBtn);
      show(helpBtn);
      if (banner && (isMobile()) && !localStorage.getItem("sebo-install-dismissed")) banner.style.display = "flex";
      // Sem prompt automático: avisa que é manual (iOS/Samsung/Firefox).
      if (detectPlatform() === "iphone") statusMsg("");
      else if (detectPlatform() !== "desktop") statusMsg("Se o botão automático não aparecer, use o menu do navegador (⋮ ou ☰).");
    }
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    refreshUI();
  });

  function doInstall() {
    if (!deferredPrompt) {
      var p = detectPlatform();
      if (p === "iphone") statusMsg("No iPhone é manual: Compartilhar ⎙ → Adicionar à Tela de Início.");
      else if (p === "samsung") statusMsg("No Samsung: ☰ → Adicionar página a → Tela inicial.");
      else statusMsg("Menu ⋮ → Adicionar à tela inicial → Instalar.");
      openHelp();
      return;
    }
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function (choice) {
      statusMsg(choice.outcome === "accepted" ? "Instalando…" : "Instalação dispensada. Tente pelo menu ⋮.");
      deferredPrompt = null;
      refreshUI();
    }).catch(function () {
      deferredPrompt = null;
      refreshUI();
    });
  }

  function doShare() {
    var data = { title: "Sebo", text: "Sebo — encomende livros:", url: location.href };
    if (navigator.share) navigator.share(data).catch(function () {});
    else doCopy();
  }

  function doCopy() {
    var url = location.href;
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () {
      statusMsg("Link copiado!");
    });
    else {
      var t = document.createElement("textarea");
      t.value = url; document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); statusMsg("Link copiado!"); } catch (e) {}
      t.remove();
    }
  }

  function openHelp() {
    highlightStep();
    if (dialog && dialog.showModal) dialog.showModal();
  }

  document.querySelectorAll(".js-install-now").forEach(function (b) {
    b.addEventListener("click", doInstall);
  });
  document.querySelectorAll(".js-share").forEach(function (b) {
    // Esconde Compartilhar se a API não existir (desktop antigo).
    if (!navigator.share) b.style.display = "none";
    b.addEventListener("click", doShare);
  });
  document.querySelectorAll(".js-copy-link").forEach(function (b) {
    b.addEventListener("click", doCopy);
  });

  if (installBtn) installBtn.addEventListener("click", doInstall);
  if (bannerInstall) bannerInstall.addEventListener("click", doInstall);
  if (helpBtn) helpBtn.addEventListener("click", openHelp);
  if (bannerHelp) bannerHelp.addEventListener("click", openHelp);
  if (bannerClose) bannerClose.addEventListener("click", function () {
    hide(banner);
    try { localStorage.setItem("sebo-install-dismissed", "1"); } catch (e) {}
  });

  window.addEventListener("appinstalled", function () {
    deferredPrompt = null;
    hide(banner);
    statusMsg("Instalado com sucesso!");
    refreshUI();
  });

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js").catch(function () {});
  }

  refreshUI();
})();
