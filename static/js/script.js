/* pygab.dev — small interactions on top of Bootstrap (horizontal scrollers) */
(function () {
  // Horizontal scrollers: arrow buttons scroll the track by ~one card
  document.querySelectorAll('[data-scroller]').forEach(function (sc) {
    var track = sc.querySelector('.scroller-track');
    if (!track) return;
    var step = function () {
      var first = track.querySelector('*');
      return first ? first.getBoundingClientRect().width + 22 : 360;
    };
    sc.querySelectorAll('[data-scroll="prev"]').forEach(function (el) {
      el.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    });
    sc.querySelectorAll('[data-scroll="next"]').forEach(function (el) {
      el.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    });
  });
})();
