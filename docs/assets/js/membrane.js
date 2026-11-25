// Interactive membrane on the home page: a row of MesoMem particles with their
// orientation vectors. The membrane undulates gently and bends away from the cursor.
(function () {
  var canvas = document.getElementById('membrane');
  if (!canvas || !canvas.getContext) return;

  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var R = 48;          // radius of the (invisible) cursor brush, px
  var SPACING = 18;    // particle spacing, px
  var W = 0, H = 0, N = 0, t = 0;
  var h = new Float32Array(0);
  var th = new Float32Array(0);   // orientation of each particle, radians from vertical
  var mx = null, my = null;

  function resize() {
    var r = canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    W = r.width; H = r.height;
    canvas.width = Math.max(1, Math.round(W * dpr));
    canvas.height = Math.max(1, Math.round(H * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var n = Math.max(24, Math.round(W / SPACING));
    if (n !== N) { N = n; h = new Float32Array(N); th = new Float32Array(N); }
  }

  function idx(i) { return (i + N) % N; }

  canvas.addEventListener('pointermove', function (e) {
    var r = canvas.getBoundingClientRect();
    mx = e.clientX - r.left;
    my = e.clientY - r.top;
  });
  canvas.addEventListener('pointerleave', function () { mx = null; my = null; });
  window.addEventListener('resize', resize);

  // "line": white beads with a short orientation line pointing up.
  // "bilayer": blue beads with a yellow band and a black arrow, as in the paper schematic.
  var bilayer = canvas.getAttribute('data-variant') === 'bilayer';

  function drawLine(x, y, ux, uy) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + ux * 20, y + uy * 20);
    ctx.strokeStyle = 'rgba(15, 110, 110, 0.55)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(x, y, 5.5, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.strokeStyle = '#0f6e6e';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  function drawBilayer(x, y, angle) {
    var r = 8.5;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.clip();
    ctx.fillStyle = '#8fa3c8';
    ctx.fillRect(-r, -r, 2 * r, 2 * r);
    ctx.fillStyle = '#f3df8a';
    ctx.fillRect(-r, -0.34 * r, 2 * r, 0.68 * r);
    ctx.restore();
  }

  function drawArrow(x, y, ux, uy) {
    var L = 18;
    var tx = x + ux * L, ty = y + uy * L;
    var qx = -uy, qy = ux;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(tx - ux * 3, ty - uy * 3);
    ctx.strokeStyle = '#1d2327';
    ctx.lineWidth = 1.3;
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(tx, ty);
    ctx.lineTo(tx - ux * 4.5 + qx * 2.4, ty - uy * 4.5 + qy * 2.4);
    ctx.lineTo(tx - ux * 4.5 - qx * 2.4, ty - uy * 4.5 - qy * 2.4);
    ctx.closePath();
    ctx.fillStyle = '#1d2327';
    ctx.fill();
  }

  function step() {
    t += reduce ? 0 : 0.012;
    var dx = W / N;
    var next = new Float32Array(N);

    for (var i = 0; i < N; i++) {
      var x = (i + 0.5) * dx;
      var lap = h[idx(i - 1)] - 2 * h[i] + h[idx(i + 1)];
      var bil = h[idx(i - 2)] - 4 * h[idx(i - 1)] + 6 * h[i] - 4 * h[idx(i + 1)] + h[idx(i + 2)];
      var target = reduce ? 0 :
        8 * Math.sin(2 * Math.PI * 2 * x / W + t) +
        5 * Math.sin(2 * Math.PI * 3 * x / W - 1.3 * t + 1.1) +
        3 * Math.sin(2 * Math.PI * 5 * x / W + 0.7 * t + 2.0);
      var f = 0.18 * lap - 0.05 * bil + 0.03 * (target - h[i]);

      if (mx !== null) {
        var y = H / 2 + h[i];
        var ddx = x - mx;
        if (Math.abs(ddx) < R) {
          var half = Math.sqrt(R * R - ddx * ddx);
          var dy = y - my;
          if (Math.abs(dy) < half) {
            var want = dy >= 0 ? my + half : my - half;
            f += 0.35 * (want - y);
          }
        }
      }
      next[i] = h[i] + f;
    }
    for (var k = 0; k < N; k++) h[k] = Math.max(-H / 2 + 12, Math.min(H / 2 - 12, next[k]));

    // Orientations: each arrow relaxes toward the local membrane normal (tilt) and
    // toward its neighbours (splay); the cursor turns nearby arrows away.
    var nextTh = new Float32Array(N);
    for (var o = 0; o < N; o++) {
      var ox = (o + 0.5) * dx;
      var oy = H / 2 + h[o];
      var phi = Math.atan((h[idx(o + 1)] - h[idx(o - 1)]) / (2 * dx));
      var d = th[o] - 0.06 * (th[o] - phi) + 0.12 * (th[idx(o - 1)] + th[idx(o + 1)] - 2 * th[o]);
      if (mx !== null) {
        var cdx = ox - mx, cdy = oy - my;
        var dist = Math.sqrt(cdx * cdx + cdy * cdy);
        if (dist < R && dist > 0.001) {
          var diff = Math.atan2(cdx, -cdy) - d;
          diff = Math.atan2(Math.sin(diff), Math.cos(diff));
          d += 0.08 * (1 - dist / R) * diff;
        }
      }
      nextTh[o] = phi + Math.max(-0.95, Math.min(0.95, d - phi));
    }
    th = nextTh;

    ctx.clearRect(0, 0, W, H);
    for (var j = 0; j < N; j++) {
      var px = (j + 0.5) * dx;
      var py = H / 2 + h[j];
      if (bilayer) drawBilayer(px, py, th[j]);
      else drawLine(px, py, Math.sin(th[j]), -Math.cos(th[j]));
    }
    if (bilayer) {
      for (var a = 0; a < N; a++) {
        drawArrow((a + 0.5) * dx, H / 2 + h[a], Math.sin(th[a]), -Math.cos(th[a]));
      }
    }
    requestAnimationFrame(step);
  }

  resize();
  requestAnimationFrame(step);
})();
