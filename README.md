# xaloAC-Stealer

**Windows Information Stealer — Educational & Security Research Project**

`xaloAC-Stealer`, Windows üzerinde çalışan bir bilgi hırsanı (information stealer) mimarisinin incelenmesi amacıyla hazırlanmış deneysel bir güvenlik araştırması projesidir.

Proje, bir istemci/payload oluşturucu ile bu istemciden gelen verileri alan Flask tabanlı bir sunucu bileşeninden oluşmaktadır.

> **xaloAC**
> Developer: **x410m1s0**

---

## ⚠️ Önemli Proje Durumu

Bu repository'deki kodların tamamı gerçek bir kurban sistemi üzerinde çalıştırılarak doğrulanmış değildir.

Kaynak kodu **statik olarak incelenmiş ve Python kaynaklarının sözdizimi seviyesinde doğrulanmıştır**. Ancak bilgi toplama işlemlerinin gerçek bir Windows sistemi üzerinde uçtan uca başarıyla gerçekleştiği iddia edilmemektedir.

Bu nedenle:

* Proje production-ready değildir.
* Tüm özelliklerin gerçek sistemlerde çalıştığı garanti edilmez.
* Her Windows sürümüyle uyumlu olduğu garanti edilmez.
* Payload'ın gerçek bir sistem üzerinde başarıyla çalıştığı iddia edilmez.
* Tüm veri toplama modüllerinin uçtan uca test edildiği iddia edilmez.
* CS2, Steam, Discord veya diğer üçüncü taraf servislerle sürekli uyumluluk garanti edilmez.
* Projedeki herhangi bir bileşenin yalnızca kaynak kodda bulunması, gerçek ortamda başarıyla çalıştığı anlamına gelmez.

Repository'nin amacı **çalışan bir kötü amaçlı yazılımı dağıtmak değil; bilgi hırsanı mimarisini kaynak kod üzerinden incelemek ve güvenlik araştırmalarına yardımcı olmaktır.**

---

## 🎯 Projenin Amacı

Proje aşağıdaki güvenlik konularını incelemek amacıyla hazırlanmıştır:

* Information stealer mimarisi
* Windows sistem bilgilerinin toplanması
* Tarayıcı verilerinin nasıl hedeflenebildiğinin incelenmesi
* Kimlik bilgisi hırsızlığı tekniklerinin analizi
* Cookie/token toplama yöntemlerinin incelenmesi
* Wi-Fi bilgilerinin hedeflenmesi
* Dosya toplama mekanizmalarının analizi
* İstemci → sunucu veri akışı
* Flask tabanlı veri alıcı mimarisi
* SQLite ile toplanan verilerin saklanması
* Malware davranışlarının tespit edilmesi
* Savunma ve güvenlik araştırması

---

## 🧩 Mimari

Projenin temel yapısı iki ana bileşenden oluşmaktadır:

```text
┌──────────────────────────────┐
│         builder.py           │
│                              │
│ Payload oluşturma mantığı    │
└──────────────┬───────────────┘
               │
               ▼
       Oluşturulan payload
               │
               ▼
┌──────────────────────────────┐
│        Hedef Windows         │
│                              │
│ Sistem / tarayıcı / Wi-Fi   │
│ oyun ve dosya verileri       │
└──────────────┬───────────────┘
               │
               │ HTTP
               ▼
┌──────────────────────────────┐
│          server.py           │
│                              │
│ Flask veri alıcı             │
│ SQLite veritabanı            │
│ Web paneli                   │
└──────────────────────────────┘
```

Bu diyagram projenin kaynak kodundaki tasarlanan veri akışını ifade eder; gerçek sistem üzerinde uçtan uca çalışırlık garantisi değildir.

---

## 📁 Proje Yapısı

```text
xaloAC-Stealer/
│
├── builder.py
├── server.py
├── requirements.txt
│
├── victims/
│   └── xaloac.db
│
├── README.md
└── LICENSE
```

---

## 🔨 builder.py

`builder.py`, proje içerisindeki payload oluşturma mekanizmasını içerir.

Kaynak kodda oluşturulan payload içerisinde çeşitli bilgi toplama işlevleri bulunmaktadır.

Kaynak kod tarafından hedeflenen veri kategorileri arasında:

### Sistem Bilgileri

* Bilgisayar adı
* Windows kullanıcı adı
* Public IP
* HWID / sistem kimliği
* CPU bilgisi
* RAM bilgisi
* GPU bilgisi
* Ekran çözünürlüğü
* Windows sürümü
* Dil
* Saat dilimi
* Administrator durumu

### Ağ / Wi-Fi

Kaynak kodda Wi-Fi SSID ve kayıtlı Wi-Fi kimlik bilgilerinin hedeflenmesine yönelik işlevler bulunmaktadır.

### Tarayıcı Verileri

Kaynak kodda çeşitli Chromium tabanlı tarayıcılardan:

* kayıtlı parolalar
* cookie verileri

elde etmeye yönelik işlevler bulunmaktadır.

Kodda Chrome, Edge, Brave ve Opera gibi tarayıcılarla ilişkili yollar/işlemler bulunmaktadır.

### Oyun / Uygulama Verileri

Kaynak kodda bazı oyun ve uygulamalarla ilişkili verilerin hedeflenmesine yönelik bölümler bulunmaktadır.

Bunlar arasında kaynak kodda:

* Steam
* Epic Games
* Minecraft
* Riot Games
* FiveM / Rockstar
* Ubisoft
* Discord

ile ilişkili veri toplama mantıkları yer almaktadır.

> Bu liste, kaynak kodda bulunan hedefleme mantığını açıklamaktadır. Her bileşenin gerçek sistem üzerinde başarıyla veri topladığı doğrulanmış değildir.

### Dosya Toplama

Kaynak kodda kullanıcı profili altında bulunan belirli klasörlerden dosya toplamaya yönelik mekanizmalar bulunmaktadır.

Hedeflenen klasörler arasında:

```text
Desktop
Documents
Pictures
Downloads
```

gibi kullanıcı dizinleri yer almaktadır.

---

## 🌐 server.py

`server.py`, Flask kullanılarak oluşturulmuş sunucu tarafını içerir.

Kaynak kodda gelen verilerin SQLite veritabanına kaydedilmesi için tablolar oluşturulmaktadır.

Kaynak kodda bulunan veri kategorileri:

```text
victims
passwords
cookies
wifi
games
files_log
clipboard
```

şeklindedir.

Sunucu tarafında ayrıca dosya yükleme ve kayıtlı dosyaların sunulmasına yönelik endpointler bulunmaktadır.

Web paneli üzerinden toplanan verilerin görüntülenmesine yönelik bir arayüz de bulunmaktadır.

---

## 🗄️ SQLite

Proje `victims/xaloac.db` isimli SQLite veritabanı kullanmaktadır.

Veritabanı yapısı kaynak kod içerisinde çeşitli veri kategorilerini ayrı tablolar halinde saklayacak şekilde tasarlanmıştır.

Repository içerisindeki mevcut `xaloac.db` dosyası bir örnek/veritabanı dosyasıdır.

---

## 📦 Gereksinimler

Proje içerisinde `requirements.txt` bulunmaktadır.

Python bağımlılıklarının kurulumu için:

```text
pip install -r requirements.txt
```

kullanılabilir.

Ancak bağımlılıkların kurulumunun projenin tüm özelliklerinin çalışacağı anlamına gelmediği unutulmamalıdır.

---

## 🧪 Test Durumu

Bu repository için test durumu özellikle açık bırakılmıştır.

### Doğrulanan

Python kaynaklarının sözdizimi seviyesinde kontrolü yapılmıştır.

### Doğrulanmayan

Aşağıdaki işlemlerin gerçek bir hedef Windows sistemi üzerinde uçtan uca başarıyla çalıştığı doğrulanmamıştır:

* Payload'ın gerçek hedef sistemde çalışması
* Tarayıcı kimlik bilgilerinin başarıyla alınması
* Cookie'lerin başarıyla alınması
* Wi-Fi bilgilerinin başarıyla alınması
* Oyun/uygulama verilerinin başarıyla alınması
* Dosyaların başarıyla aktarılması
* Tüm verilerin server tarafından eksiksiz alınması

Bu nedenle repository'deki özellikler **kaynak kodunda mevcut olan işlevler** olarak değerlendirilmelidir; tamamı gerçek ortamda doğrulanmış özellikler olarak değerlendirilmemelidir.

---

## 🔬 Eğitim ve Araştırma Kullanımı

Bu repository özellikle aşağıdaki araştırmalar için kullanılabilir:

### Malware Analysis

Bir bilgi hırsanının hangi bileşenlerden oluşabileceğini incelemek.

### Detection Engineering

Bilgi hırsanlarında görülebilecek:

* şüpheli PowerShell davranışları
* tarayıcı veri erişimleri
* credential erişimleri
* HTTP veri aktarımı
* dosya toplama
* SQLite veri depolaması

gibi davranışları araştırmak.

### Windows Security

Windows kullanıcı verilerinin ve uygulama verilerinin kötü amaçlı yazılımlar tarafından neden hedeflenebildiğini anlamak.

### Defensive Security

Endpoint Detection & Response (EDR), antivirüs ve diğer güvenlik sistemlerinin tespit edebileceği davranışları araştırmak.

---

## ⚠️ Güvenli Araştırma

Bu proje yalnızca:

* izole laboratuvar ortamlarında,
* araştırmacının kontrolündeki sistemlerde,
* açıkça izin verilmiş test ortamlarında

incelenmelidir.

Gerçek kullanıcıların:

* parolalarını,
* cookie'lerini,
* tokenlarını,
* Wi-Fi kimlik bilgilerini,
* dosyalarını

izinsiz şekilde toplamak veya aktarmak için kullanılmamalıdır.

---

## 🚫 Yetkisiz Kullanım

Bu repository:

* gerçek kullanıcıların bilgilerinin izinsiz toplanması,
* kimlik bilgilerinin çalınması,
* hesaplara yetkisiz erişim,
* kişisel dosyaların izinsiz alınması,
* gizli verilerin üçüncü kişilere aktarılması

amacıyla kullanılmak üzere sunulmamaktadır.

Projenin güvenlik araştırması dışında kullanımından kullanıcı kendisi sorumludur.

---

## 🔒 Üçüncü Taraf Servisler

Projede bazı üçüncü taraf uygulamalar ve servislerle ilişkili veri toplama mantıkları bulunmaktadır.

Bu proje:

* Valve Corporation,
* Steam,
* Discord,
* Epic Games,
* Riot Games,
* Ubisoft,
* Microsoft,
* Google,
* Brave,
* Opera

ve diğer ilgili şirket veya servislerle bağlantılı, desteklenen veya onaylanan resmi bir proje değildir.

İlgili marka ve fikri mülkiyet hakları sahiplerine aittir.

---

## 📄 Lisans

Bu proje standart MIT, Apache veya GPL lisansı altında değildir.

Kullanım ve dağıtım koşulları için repository içerisindeki [`LICENSE`](LICENSE) dosyasına bakınız.

Bu lisans özellikle projenin **eğitim, analiz ve güvenlik araştırması** amacıyla kullanılmasını esas alır.

---

## 👤 Geliştirici

**xaloAC**

Developer:

**x410m1s0**

---

## 📌 Sonuç

`xaloAC-Stealer`, kaynak kodunda bilgi hırsanı davranışlarını modelleyen deneysel bir güvenlik araştırması projesidir.

Projenin amacı:

> **Bir bilgi hırsanının nasıl yapılandırılabileceğini anlamak, bu davranışları analiz etmek ve savunma amaçlı güvenlik araştırmalarına kaynak sağlamaktır.**

Kodların tamamının gerçek sistem üzerinde test edildiği veya çalıştığının doğrulandığı iddia edilmemektedir.

**Kaynak kodu inceleyin, davranışları analiz edin ve yalnızca yetkili/izole araştırma ortamlarında kullanın.**

---

**xaloAC**
**x410m1s0**
**2026**
