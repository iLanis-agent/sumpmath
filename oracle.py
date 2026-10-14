import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)
def round0(x): return jsnum(math.floor(x + 0.5))

PUMP_LPH = 2000
BATTERY_L = 4000

def pit_plan(diameterCm, riseCm):
    if not (diameterCm > 0) or not (riseCm > 0):
        return {"error": "the pit and the rise must be positive"}
    r = diameterCm / 2
    liters = round1(math.pi * r * r * riseCm / 1000)
    if liters <= 15: verdict = "a teacup cycle"
    elif liters <= 40: verdict = "a bucket cycle"
    else: verdict = "a drum cycle"
    return {"liters": liters, "verdict": verdict}

def storm_plan(liters, cyclesPerHour):
    if not (liters > 0) or not (cyclesPerHour > 0):
        return {"error": "the liters and the cycles must be positive"}
    lph = round0(liters * cyclesPerHour)
    share = round0(lph / PUMP_LPH * 100)
    if share <= 40: verdict = "loafing"
    elif share <= 80: verdict = "working hard"
    else: verdict = "undersized for the storm"
    return {"lph": lph, "share": share, "verdict": verdict}

def backup_plan(lph, outageHours):
    if not (lph > 0) or not (outageHours > 0):
        return {"error": "the flow and the hours must be positive"}
    liters = round0(lph * outageHours)
    if liters <= 1000: verdict = "a short watch"
    elif liters <= BATTERY_L: verdict = "within battery reach"
    else: verdict = "a generator conversation"
    return {"liters": liters, "verdict": verdict}

def render_pit(r, diameterCm, riseCm):
    return ("Your " + fmt(diameterCm) + " cm pit rising " + fmt(riseCm) + " cm between cycles holds " + fmt(r["liters"])
            + " L a cycle - " + r["verdict"] + ".")

def render_storm(r, liters, cyclesPerHour):
    return (fmt(liters) + " L a cycle at " + plural(cyclesPerHour, "cycle") + " an hour is " + fmt(r["lph"])
            + " L an hour, " + fmt(r["share"]) + "% of a labeled " + fmt(PUMP_LPH) + " L/h pump - " + r["verdict"] + ".")

def render_backup(r, lph, outageHours):
    return ("Your " + fmt(outageHours) + " h outage at " + fmt(lph) + " L an hour is " + fmt(r["liters"])
            + " L to move - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[45,25],[30,20],[60,30],[40,15],[50,25],[36,20],[25,25],[55,30],[0,25],[45,0]]:
    add("pitPlan", pit_plan, render_pit, a)
for a in [[39.8,6],[14.1,10],[84.8,30],[20,20],[49.1,25],[39.8,60],[12.3,12],[71.3,25],[0,6],[39.8,0]]:
    add("stormPlan", storm_plan, render_storm, a)
for a in [[239,3],[141,8],[400,2],[239,12],[1600,3],[800,6],[100,5],[1200,4],[0,3],[239,0]]:
    add("backupPlan", backup_plan, render_backup, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
