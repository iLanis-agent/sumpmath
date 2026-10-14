(function (root) {
  "use strict";
  var PUMP_LPH = 2000;  // labeled sump pump move, liters per hour
  var BATTERY_L = 4000; // labeled battery-backup move over an outage, liters

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }

  function pitPlan(diameterCm, riseCm) {
    if (!(diameterCm > 0) || !(riseCm > 0)) return { error: "the pit and the rise must be positive" };
    var r = diameterCm / 2;
    var liters = round1(Math.PI * r * r * riseCm / 1000);
    var verdict;
    if (liters <= 15) verdict = "a teacup cycle";
    else if (liters <= 40) verdict = "a bucket cycle";
    else verdict = "a drum cycle";
    return { liters: liters, verdict: verdict };
  }

  function stormPlan(liters, cyclesPerHour) {
    if (!(liters > 0) || !(cyclesPerHour > 0)) return { error: "the liters and the cycles must be positive" };
    var lph = Math.round(liters * cyclesPerHour);
    var share = Math.round(lph / PUMP_LPH * 100);
    var verdict;
    if (share <= 40) verdict = "loafing";
    else if (share <= 80) verdict = "working hard";
    else verdict = "undersized for the storm";
    return { lph: lph, share: share, verdict: verdict };
  }

  function backupPlan(lph, outageHours) {
    if (!(lph > 0) || !(outageHours > 0)) return { error: "the flow and the hours must be positive" };
    var liters = Math.round(lph * outageHours);
    var verdict;
    if (liters <= 1000) verdict = "a short watch";
    else if (liters <= BATTERY_L) verdict = "within battery reach";
    else verdict = "a generator conversation";
    return { liters: liters, verdict: verdict };
  }

  function renderPit(r, diameterCm, riseCm) {
    return "Your " + diameterCm + " cm pit rising " + riseCm + " cm between cycles holds " + r.liters
      + " L a cycle - " + r.verdict + ".";
  }

  function renderStorm(r, liters, cyclesPerHour) {
    return liters + " L a cycle at " + plural(cyclesPerHour, "cycle") + " an hour is " + r.lph
      + " L an hour, " + r.share + "% of a labeled " + PUMP_LPH + " L/h pump - " + r.verdict + ".";
  }

  function renderBackup(r, lph, outageHours) {
    return "Your " + outageHours + " h outage at " + lph + " L an hour is " + r.liters
      + " L to move - " + r.verdict + ".";
  }

  var api = { pitPlan: pitPlan, stormPlan: stormPlan, backupPlan: backupPlan, renderPit: renderPit, renderStorm: renderStorm, renderBackup: renderBackup };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.SumpMath = api;
})(this);
