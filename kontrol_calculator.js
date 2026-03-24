    var mevcutNot = $feature.kontrol_ipa;
    var mesajlar = [];

    var alt = $feature.alt_kullanim;

    var siteKodlari = ["2","4","6"];

    // alan boşluk kontrolleri
    var detayKonutBos = IsEmpty($feature.detay_konut);
    var detayTicaretBos = IsEmpty($feature.Detay_Ticaret);
    var naceBos = IsEmpty($feature.NaceKodu);
    var adBos = IsEmpty($feature.AD);

    // --------------------------------------------------
    // 1 - KENTSEL KONUT
    // --------------------------------------------------

    if (alt == "1") {

        if (detayKonutBos) {
            Push(mesajlar,"Detay konut girilmeli");
        }

        if (Includes(siteKodlari,$feature.detay_konut) && adBos) {
            Push(mesajlar,"Ad girilmeli");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }

        if (!IsEmpty($feature.NaceKodu)) {
            Push(mesajlar,"NaceKodu boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Ticaret)) {
            Push(mesajlar,"Detay_Ticaret boş olmalı");
        }
    }

    // --------------------------------------------------
    // 8 - TICARET KONUT
    // --------------------------------------------------

    if (alt == "8") {

        if (detayKonutBos) {
            Push(mesajlar,"Detay konut girilmeli");
        }

        if (detayTicaretBos) {
            Push(mesajlar,"Detay ticaret girilmeli");
        }

        if (naceBos) {
            Push(mesajlar,"Nace kodu girilmeli");
        }

        if (Includes(siteKodlari,$feature.detay_konut) && adBos) {
            Push(mesajlar,"Ad girilmeli");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }
    }

    // --------------------------------------------------
    // SOSYAL ALTYAPI (38-42)
    // --------------------------------------------------

    var egitimKodlari = ["38","39","40","41","42"];

    if (Includes(egitimKodlari,alt)) {

        if (naceBos) {
            Push(mesajlar,"Nace kodu girilmeli");
        }

        if (IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi girilmeli");
        }

        if (!IsEmpty($feature.detay_konut)) {
            Push(mesajlar,"detay_konut boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Ticaret)) {
            Push(mesajlar,"Detay_Ticaret boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }
    }

    // --------------------------------------------------
    // KAMU KURUMU (26-27)
    // --------------------------------------------------

    var kamuKodlari = ["26","27"];

    if (Includes(kamuKodlari,alt)) {

        if (naceBos) {
            Push(mesajlar,"Nace kodu girilmeli");
        }

        if (!IsEmpty($feature.detay_konut)) {
            Push(mesajlar,"detay_konut boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Ticaret)) {
            Push(mesajlar,"Detay_Ticaret boş olmalı");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }
    }

    // --------------------------------------------------
    // SANAYI TICARET (20)
    // --------------------------------------------------

    if (alt == "20") {

        if (naceBos) {
            Push(mesajlar,"Nace kodu girilmeli");
        }

        if (!IsEmpty($feature.detay_konut)) {
            Push(mesajlar,"detay_konut boş olmalı");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }
    }

    // --------------------------------------------------
    // SANAYI (11)
    // --------------------------------------------------

    if (alt == "11") {

        //if (!(Left($feature.NaceKodu,1) == "C" || Left($feature.NaceKodu,1) == "T")) {
            //Push(mesajlar,"Nace kodu C veya T ile başlamalı");
        //}

        if (!IsEmpty($feature.detay_konut)) {
            Push(mesajlar,"detay_konut boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Ticaret)) {
            Push(mesajlar,"Detay_Ticaret boş olmalı");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }
    }

    // --------------------------------------------------
    // TICARET (3)
    // --------------------------------------------------

    if (alt == "3") {

        if (naceBos) {
            Push(mesajlar,"Nace kodu girilmeli");
        }

        if (detayTicaretBos) {
            Push(mesajlar,"Detay_Ticaret girilmeli");
        }

        if (!IsEmpty($feature.detay_konut)) {
            Push(mesajlar,"detay_konut boş olmalı");
        }

        if (!IsEmpty($feature.Detay_SosyalAltyapi)) {
            Push(mesajlar,"Detay_SosyalAltyapi boş olmalı");
        }

        if (!IsEmpty($feature.Detay_Resmi)) {
            Push(mesajlar,"Detay_Resmi boş olmalı");
        }
    }

    // --------------------------------------------------
    // MESAJ MOTORU
    // --------------------------------------------------

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