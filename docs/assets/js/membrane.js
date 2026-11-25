// Interactive membrane on the home page: a row of MesoMem particles with their
// orientation vectors. The membrane undulates gently and bends away from the cursor.
(function () {
  var canvas = document.getElementById('membrane');
  if (!canvas || !canvas.getContext) return;

  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var R = 64;          // radius of the (invisible) cursor brush, px
  var SPACING = 18;    // particle spacing, px
  var W = 0, H = 0, N = 0, t = 0;
  var h = new Float32Array(0);
  var mx = null, my = null;

  function resize() {
    var r = canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    W = r.width; H = r.height;
    canvas.width = Math.max(1, Math.round(W * dpr));
    canvas.height = Math.max(1, Math.round(H * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var n = Math.max(24, Math.round(W / SPACING));
    if (n !== N) { N = n; h = new Float32Array(N); }
  }

  function idx(i) { return (i + N) % N; }

  canvas.addEventListener('pointermove', function (e) {
    var r = canvas.getBoundingClientRect();
    mx = e.clientX - r.left;
    my = e.clientY - r.top;
  });
  canvas.addEventListener('pointerleave', function () { mx = null; my = null; });
  window.addEventListener('resize', resize);

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

    ctx.clearRect(0, 0, W, H);
    for (var j = 0; j < N; j++) {
      var px = (j + 0.5) * dx;
      var py = H / 2 + h[j];
      var slope = (h[idx(j + 1)] - h[idx(j - 1)]) / (2 * dx);
      var norm = Math.sqrt(1 + slope * slope);
      var nx = -slope / norm, ny = 1 / norm;
      var L = 9;

      ctx.beginPath();
      ctx.moveTo(px - nx * L, py - ny * L);
      ctx.lineTo(px + nx * L, py + ny * L);
      ctx.strokeStyle = 'rgba(15, 110, 110, 0.55)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px, py, 4.5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.strokeStyle = '#0f6e6e';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
    requestAnimationFrame(step);
  }

  resize();
  requestAnimationFrame(step);
})();
