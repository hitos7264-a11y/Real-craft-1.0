/* HRGM Voxel World — native-app feel helpers */
(function (global) {
  const isStandalone =
    global.matchMedia("(display-mode: standalone)").matches ||
    global.matchMedia("(display-mode: fullscreen)").matches ||
    global.navigator.standalone === true;

  function haptic(ms) {
    if (global.navigator.vibrate) global.navigator.vibrate(ms || 8);
  }

  let wakeLock = null;
  async function enableWakeLock() {
    if (!("wakeLock" in global.navigator)) return;
    try {
      wakeLock = await global.navigator.wakeLock.request("screen");
      wakeLock.addEventListener("release", () => { wakeLock = null; });
    } catch (_) {}
  }

  async function reacquireWakeLock() {
    if (document.visibilityState === "visible") await enableWakeLock();
  }

  function preventBrowserGestures() {
    document.addEventListener("contextmenu", (e) => e.preventDefault());
    document.addEventListener("gesturestart", (e) => e.preventDefault());
    let lastTouch = 0;
    document.addEventListener("touchend", (e) => {
      const now = Date.now();
      if (now - lastTouch <= 320) e.preventDefault();
      lastTouch = now;
    }, { passive: false });
  }

  function applyStandaloneClass() {
    if (isStandalone) document.documentElement.classList.add("standalone");
    else document.documentElement.classList.add("browser");
  }

  function registerServiceWorker() {
    if ("serviceWorker" in global.navigator) {
      global.navigator.serviceWorker.register("sw.js").catch(() => {});
    }
  }

  global.HRGMNative = {
    isStandalone,
    haptic,
    enableWakeLock,
    reacquireWakeLock,
    preventBrowserGestures,
    applyStandaloneClass,
    registerServiceWorker
  };
})(window);
