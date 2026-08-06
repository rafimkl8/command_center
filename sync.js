/* ============================================================
   Cross-device sync for the trackers (iPhone <-> Windows).
   Uses Firebase Firestore + a personal "sync code".
   No server to run. The Firebase web config below is NOT a
   secret (it is safe to be public); your data is guarded by
   your unguessable sync code.

   SETUP STATUS:
   [x] Firebase project created (my-command-center-b4bde)
   [x] Config wired into FIREBASE_CONFIG below
   [ ] Firestore rules published  <-- DO THIS FIRST, see index.html.
                                      Until then every write fails with a
                                      permission error and the bar shows
                                      "Sync error".
   [ ] Devices linked: tap "Connect", leave blank to generate a code, then
       enter that SAME code on the other device.
   ============================================================ */
(function () {
  // ===== FIREBASE CONFIG =====
  // These values are a public project identifier, not a secret. Firebase web
  // config is designed to ship in client code — anyone can read it from any
  // deployed site. The thing that actually protects your data is the Firestore
  // rules (see index.html) plus a long, unguessable sync code.
  var FIREBASE_CONFIG = {
    apiKey: "AIzaSyC2JQHfYU_4vs7wP0TzxzFRjrDHTDiHzLg",
    authDomain: "my-command-center-b4bde.firebaseapp.com",
    projectId: "my-command-center-b4bde",
    storageBucket: "my-command-center-b4bde.firebasestorage.app",
    messagingSenderId: "10791355509",
    appId: "1:10791355509:web:4a0250f4ee1d8de865243c"
  };
  // ===========================

  // Firestore rules require >= 12 characters. Enforced here too so a short
  // code fails with an explanation instead of a silent permission error.
  var MIN_CODE_LEN = 12;

  var KEYS = [], onData = function () {};
  var db = null, ref = null, unsub = null, code = null;
  var origin = Math.random().toString(36).slice(2);
  var firstPull = false, applying = false, pushTimer = null;

  function configured() { return !!(FIREBASE_CONFIG.projectId && FIREBASE_CONFIG.apiKey); }

  function setStatus(txt, cls) {
    var s = document.getElementById('cloudstat'); if (!s) return;
    s.textContent = txt;
    var colors = { ok: '#4ade80', err: '#f87171', off: '#fbbf24', '': '#9fb4c7' };
    s.style.color = colors[cls || ''] || '#9fb4c7';
  }

  function buildBar() {
    if (document.getElementById('cloudbar')) return;
    var b = document.createElement('div');
    b.id = 'cloudbar';
    b.style.cssText = 'position:sticky;top:0;z-index:99999;background:#0f1720;color:#cfe;font-family:Geist,sans-serif;font-size:12px;padding:8px 12px;display:flex;align-items:center;gap:10px;border-radius:0 0 12px 12px;box-shadow:0 2px 8px rgba(0,0,0,.2)';
    b.innerHTML = '<span style="font-size:13px">☁️</span><span id="cloudstat">…</span>'
      + '<button id="cloudbtn" style="margin-left:auto;background:#1d4ed8;color:#fff;border:none;border-radius:7px;padding:5px 12px;font:600 12px Geist,sans-serif;cursor:pointer">Connect</button>';
    document.body.insertBefore(b, document.body.firstChild);
    document.getElementById('cloudbtn').onclick = promptCode;
  }

  function promptCode() {
    if (!configured()) {
      alert('Cross-device sync is not set up yet.\n\nOpen the hub page (index.html) and follow the 5-minute Firebase setup, or ask your assistant to wire in your Firebase config. Until then, your progress still saves on THIS device.');
      return;
    }
    var cur = localStorage.getItem('sync_code') || '';
    var c = prompt('Enter a SYNC CODE — use the SAME code on your iPhone and your laptop.\n\nLeave blank to generate a new one:', cur);
    if (c === null) return;
    c = (c || '').trim();
    if (!c) {
      c = 'wsr-' + Math.random().toString(36).slice(2, 8) + Math.random().toString(36).slice(2, 6);
      alert('Your new sync code is:\n\n' + c + '\n\nWrite it down, then enter this SAME code on your other device to link them.');
    } else if (c.length < MIN_CODE_LEN) {
      alert('That code is too short (' + c.length + ' characters).\n\nUse at least ' + MIN_CODE_LEN + ' characters, or leave the box blank to generate a strong one.\n\nShort codes can be guessed by someone else, which would let them read and overwrite your progress.');
      return;
    }
    firstPull = true;
    connect(c);
  }

  function snapshotLocal() {
    var o = {};
    KEYS.forEach(function (k) { var v = localStorage.getItem(k); if (v !== null) o[k] = v; });
    return o;
  }

  function applyReplace(remote) {
    applying = true;
    KEYS.forEach(function (k) { if (remote[k] !== undefined) localStorage.setItem(k, remote[k]); });
    applying = false;
    onData();
  }

  // First link merges so no progress is lost from either device.
  function mergeFirst(remote) {
    applying = true;
    KEYS.forEach(function (k) {
      if (remote[k] === undefined) return;
      if (k.indexOf('done') >= 0) {
        var loc = {}, rem = {};
        try { loc = JSON.parse(localStorage.getItem(k)) || {}; } catch (e) {}
        try { rem = JSON.parse(remote[k]) || {}; } catch (e) {}
        for (var p in rem) { if (rem[p]) loc[p] = rem[p]; }
        localStorage.setItem(k, JSON.stringify(loc));
      } else {
        localStorage.setItem(k, remote[k]);
      }
    });
    applying = false;
    onData();
    pushNow();
  }

  function pushNow() {
    if (!ref) return;
    ref.set({ keys: snapshotLocal(), updatedAt: Date.now(), origin: origin })
      .then(function () { setStatus('Synced ✓  (' + code + ')', 'ok'); })
      .catch(function () { setStatus('Sync error — check connection', 'err'); });
  }

  function push() {
    if (!ref || applying) return;
    clearTimeout(pushTimer);
    pushTimer = setTimeout(pushNow, 600);
  }

  function connect(c) {
    code = c;
    localStorage.setItem('sync_code', c);
    setStatus('Connecting…', '');
    if (unsub) { unsub(); unsub = null; }
    ref = db.collection('trackers').doc(c);
    unsub = ref.onSnapshot(function (snap) {
      var d = snap.data();
      if (firstPull) {
        firstPull = false;
        if (!d) { pushNow(); return; }     // empty cloud -> upload this device
        mergeFirst(d.keys || {});          // both exist -> merge, then upload
        return;
      }
      if (d && d.origin !== origin) {       // a change from the OTHER device
        applyReplace(d.keys || {});
        setStatus('Synced ✓  (' + code + ')', 'ok');
      }
    }, function () { setStatus('Sync error — check connection', 'err'); });
  }

  function start(opts) {
    KEYS = (opts && opts.keys) || [];
    onData = (opts && opts.onData) || function () {};
    buildBar();
    if (!configured()) { setStatus('Sync OFF — set up Firebase (see hub page)', 'off'); return; }
    if (!window.firebase || !firebase.firestore) { setStatus('Sync library not loaded', 'err'); return; }
    if (!firebase.apps.length) firebase.initializeApp(FIREBASE_CONFIG);
    db = firebase.firestore();
    var saved = localStorage.getItem('sync_code');
    if (saved) { firstPull = true; connect(saved); }
    else { setStatus('Not linked — tap Connect to sync devices', 'off'); }
  }

  window.CloudSync = { start: start, push: push, connect: connect, configured: configured };
})();
