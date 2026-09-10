# İlerleme

Kurs, kitap, proje — neyi takip ediyorsan bir **tahta** aç, maddeleri yapıştır, tik at.
Üstte yüzde, altta kare kare ilerleme haritası. Bitince kâğıda mühür basılır.

**Canlı deneme:** https://berkdemir18.github.io/ilerleme/

## Neden var

3-4 haftada soğuyan bir çalışma döngüsünde asıl sorun ilgi değil, **ilerlemeyi görememek.**
Kronometrenin olduğu işi bitiriyorsun, olmadığı işi bırakıyorsun. Bu, kronometre.

- Ders listesini kopyalayıp yapıştır — her satır ayrı madde
- İlerleme madde başına bir kare: sadece yüzde değil, **nerede olduğun** da görünür
- `14 gün` dokunulmayan tahtaya "soğumuş" damgası
- Biten maddeler tarihiyle listenin altına düşer
- Üç tema: açık (matbaa), koyu, siber (terminal)

## Kurulum (Windows)

Gerek yok. `Ilerleme.exe` çift tıkla açılır, Python kurulu olmasına gerek duymaz.
Kaynaktan çalıştırmak istersen:

```bash
python app.py
```

Veri `veri.json` olarak uygulamanın yanında durur — düz metin, yedeklenebilir,
her yazmada bir öncesi `.bak` dosyasına alınır. Pencere kapanınca sunucu kendini kapatır.

## Dosyalar

| Dosya | Ne |
|---|---|
| `app.py` | Yerel sunucu + veri yazımı (yalnız standart kütüphane) |
| `index.html` | Arayüzün tamamı — tek dosya, CDN yok |
| `docs/` | GitHub Pages demosu (sunucu yoksa tarayıcı hafızasına yazar) |
