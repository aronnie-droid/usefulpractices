var rules = FeatureSetByName($datastore, "rules_table_2", 
["alt_kullanim_","condition_field","condition_operator","condition_value",
"check_field","check_operator","check_value","severity","category","message"], false);

var alt = Text($feature.alt_kullanim);
var mevcutNot = $feature.kontrol;

var mesajlar = [];

// ----------------------------------
// GENERIC EVALUATE FUNCTION
// ----------------------------------

function evaluate(value, operator, ruleValue) {

    var val = Text(value);

    if (operator == "always") return true;

    if (operator == "is_empty") return IsEmpty(value);

    if (operator == "not_empty") return !IsEmpty(value);

    if (operator == "in") return Includes(Split(ruleValue,"|"), val);

    if (operator == "not_in") return !Includes(Split(ruleValue,"|"), val);

    if (operator == "starts_with") {

        var prefixes = Split(ruleValue,"|");

        for (var p in prefixes) {
            if (Left(val,1) == prefixes[p]) {
                return true;
            }
        }
        return false;
    }

    return false;
}

// ----------------------------------
// FILTER RULES
// ----------------------------------

var filteredRules = Filter(rules, "alt_kullanim_ = '" + alt + "'");

// ----------------------------------
// LOOP
// ----------------------------------

for (var r in filteredRules) {

    var condField = r["condition_field"];
    var condOp = r["condition_operator"];
    var condVal = r["condition_value"];

    var checkField = r["check_field"];
    var checkOp = r["check_operator"];
    var checkVal = r["check_value"];

    var severity = r["severity"];
    var category = r["category"];
    var mesaj = r["message"];

    var condResult = true;

    if (!IsEmpty(condField)) {
        condResult = evaluate($feature[condField], condOp, condVal);
    }

    if (condResult) {

        var checkResult = evaluate($feature[checkField], checkOp, checkVal);

        if (checkResult) {

            var finalMesaj = "[" + Upper(severity) + "][" + Upper(category) + "] " + mesaj;

            Push(mesajlar, finalMesaj);
        }
    }
}

// ----------------------------------
// MESAJ MOTORU
// ----------------------------------

if (Count(mesajlar) == 0) {
    return;
}

var sonuc;

if (IsEmpty(mevcutNot)) {
    sonuc = Concatenate(mesajlar," | ");
}
else {

    sonuc = mevcutNot;

    for (var m in mesajlar) {
        if (Find(m,sonuc) == -1) {
            sonuc = sonuc + " | " + m;
        }
    }
}

if (sonuc != mevcutNot) {
    return sonuc;
}

return;