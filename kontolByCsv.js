    // RULE TABLE
    var rules = FeatureSetByName($datastore, "rules_table", 
        ["alt_kullanim","rule_type","field","operator","value","message"], false);

    var alt = $feature.alt_kullanim;
    var mevcutNot = $feature.kontrol;
    var mesajlar = [];

    // site tipi için sabit liste
    var siteKodlari = ["2","4","6"];

    // ilgili kuralları filtrele
    var filteredRules = Filter(rules, "alt_kullanim = @alt");

    // loop
    for (var r in filteredRules) {

        var fieldName = r["field"];
        var operator = r["operator"];
        var mesaj = r["message"];

        var fieldValue = $feature[fieldName];

        // ----------------------------------
        // REQUIRED (boş olamaz)
        // ----------------------------------
        if (operator == "is_empty") {

            if (IsEmpty(fieldValue)) {
                Push(mesajlar, mesaj);
            }
        }

        // ----------------------------------
        // MUST BE EMPTY
        // ----------------------------------
        if (operator == "not_empty") {

            if (!IsEmpty(fieldValue)) {
                Push(mesajlar, mesaj);
            }
        }

        // ----------------------------------
        // CONDITIONAL (site konut → AD zorunlu)
        // ----------------------------------
        if (operator == "site_konut") {

            if (Includes(siteKodlari, $feature.detay_konut) && IsEmpty(fieldValue)) {
                Push(mesajlar, mesaj);
            }
        }

        // ----------------------------------
        // EXCEPTION'lı REQUIRED
        // ----------------------------------
        if (operator == "is_empty_except_nace") {

            var exceptions = Split(r["value"], "|");   // CSV'den gelen liste
            var nace = Text($feature.NaceKodu);

            if (IsEmpty(fieldValue) && !Includes(exceptions, nace)) {
                Push(mesajlar, mesaj);
            }
        }
    }

    // ----------------------------------
    // MESAJ MOTORU (senin sistemle uyumlu)
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