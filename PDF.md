### Chapter II

#### Temel Noktalar

Bu bölüm, projenin karmaşıklığını ve bazı önemli noktaları açıklıyor. İşte anlamı:

1. Proje Kapsamı ve Karar Verme: Proje, belirli kısıtlamalar içinde karar vermeyi gerektirir. Bazı modülleri nasıl uygulayacağınız konusunda esneklik sağlanmış, ancak bu kararlarınızı iyi bir şekilde gerekçelendirmelisiniz.

2. Nginx ve Kütüphaneler: Eğer nginx gibi bir araç kullanmanız gerektiğini düşünüyorsanız, gerçekten gerekli olup olmadığını sorgulamalısınız. Ayrıca, kullanmayı düşündüğünüz kütüphanelerin görevlerinizi yerine getirip getirmediğini anlamalısınız.

3. Modüller ve Özellikler: İlginç bulmadığınız alt katmanları yeniden yapılandırmak yerine, önerilen özelliklerin işlevsel olmasına odaklanmalısınız.

4. Teknoloji ve Çerçeve: Projeye başlamadan önce gereksinimleri iyice anlamanız önemlidir. Belirtilen teknolojilere uyum sağlamalısınız; aksi halde, varsayılan diller ya da çerçevelerle çalışmak projeyi geçerli kılmayabilir.

5. Modül Bağımlılıkları: Bazı modüller diğer modüllere güçlü bir şekilde bağımlıdır. Bu bağımlılıkları göz önünde bulundurarak karar vermelisiniz.

6. Tasarım ve Uygulama: Kodlamaya başlamadan önce, uygulamanızın tasarımını dikkatlice düşünmelisiniz. Seçimlerinizi değerlendirmek ve tasarımınızı düşünmek önemlidir.

---

### Chapter III

```
İşinizin yerini alacak kütüphanelerin, çerçevelerin veya araçların kullanılması kesinlikle yasaktır. Konunun her bir kısmı yetkili üçüncü kişiyi açıkça sunacaktır.
kullanabileceğiniz parti yazılımı. Bununla birlikte, belirli eylemleri basitleştirmek için mümkün olan her şeyin kullanılmasına izin verilir ve hatta tavsiye edilir. Kullanılan herhangi bir araç veya kaynağın gerekçelendirilmesi gerektiğini unutmamak önemlidir. Lütfen basitleştirmenin işinizi tamamlamak anlamına gelmediğini unutmayın.
```

#### Zorunlu kısım

Bu bölüm, projenizin gereksinimlerini ve dikkat etmeniz gereken bazı güvenlik önlemlerini detaylandırıyor. İşte özetler:

##### Genel Bilgiler

- Kütüphaneler ve Araçlar: Kütüphaneler veya çerçeveler kullanımı genellikle yasaktır. Ancak, kullanılan araçların her zaman gerekçelendirilmesi gerekmektedir.

#### III.1 Genel Bakış

- Amaç: Kullanıcıların Pong oyunu oynayabileceği bir web sitesi oluşturmanız bekleniyor.
- Arayüz ve Oyun: Kullanıcı arayüzü iyi olmalı ve gerçek zamanlı çok oyunculu oyun desteklenmelidir.

#### III.2 Teknik Gereksinimler

- Backend: Eğer bir backend eklemeyi seçerseniz, Ruby ile yazılmalıdır (ancak Framework modülü bu gereksinimi değiştirebilir).
- Veritabanı: Eğer backend bir veritabanı kullanıyorsa, Database modülünün kısıtlamalarına uyulmalıdır.
- Frontend: Vanilla JavaScript ile geliştirilmeli, ancak FrontEnd modülü ile değiştirilebilir.
- Tek Sayfalı Uygulama: Web sitesi tek sayfa uygulaması olmalı ve tarayıcının geri ve ileri düğmeleri çalışmalıdır.
- Tarayıcı Uyumluluğu: En son stabil Google Chrome sürümü ile uyumlu olmalı.
- Hata ve Uyarılar: Kullanıcı hiçbir işlenmemiş hata veya uyarı ile karşılaşmamalıdır.
- Docker Kullanımı: Her şey tek bir komutla başlatılmalıdır. Örneğin: docker-compose up --build.

#### Docker Güvenlik:

- Docker, rootless modda çalıştırılmalıdır.
- Docker runtime dosyaları /goinfre veya /sgoinfre dizinlerinde bulunmalıdır.
- "Bind-mount volumes" kullanımı yasaktır.

```
Konteyner çözümünüz Docker ise:
    - Clusterlardaki bilgisayarlarınız Linux altında çalıştığında güvenlik açısından Docker'ı rootless modda kullanacaksınız. Bu 2 yan tarafla birlikte gelir:
        1- Docker çalışma zamanı dosyalarınız /goinfre veya konumunda bulunmalıdır /sgoinfre.
        2- Kapta kök olmayan UID'ler kullanılıyorsa, ana bilgisayar ile kapsayıcı arasında "bağlama bağlama birimleri" olarak adlandırılan birimleri kullanamazsınız.
    - Projeye, durumunuza ve bağlama bağlı olarak birkaç geri dönüş mevcuttur: VM'deki Docker, değişikliklerinizden sonra konteynerinizi yeniden oluşturun, benzersiz UID olarak root ile kendi docker görüntünüzü oluşturun.
```

#### III.3 Oyun

- Pong Oyunu: Kullanıcıların web sitesinde diğer oyuncularla Pong oynaması gerekmektedir.
- Turnuva: Oyuncular turnuva düzenleyebilmelidir. Turnuva, oyuncuları ve oyun sırasını net bir şekilde göstermelidir.
- Kayıt Sistemi: Her oyuncunun bir takma ad girmesi gerekmektedir.
- Eşleşme Sistemi: Turnuva sistemi eşleşmeleri düzenlemeli ve bir sonraki maçı duyurmalıdır.
- Kural Uyumu: Tüm oyuncular aynı kurallara uymalıdır ve AI oyuncuları da normal oyuncularla aynı hıza sahip olmalıdır.
- Görsel Tasarım: Oyun, Pong'un (1972) özünü yakalamalıdır.

```
İşinizin yerini alacak kütüphanelerin, çerçevelerin veya araçların kullanılması kesinlikle yasaktır. Konunun her bölümü, kullanabileceğiniz yetkili üçüncü taraf yazılımları açıkça sunacaktır. Bununla birlikte, belirli eylemleri basitleştirmek için mümkün olan her şeyin kullanılmasına izin verilir ve hatta tavsiye edilir. Kullanılan herhangi bir araç veya kaynağın gerekçelendirilmesi gerektiğini unutmamak önemlidir. Lütfen basitleştirmenin işinizi tamamlamak anlamına gelmediğini unutmayın.
```

#### III.4 Güvenlik

- Şifre Hashleme: Veritabanında saklanan şifreler hashlenmelidir.
- Güvenlik: SQL enjeksiyonları/XSS'ye karşı korunma sağlanmalıdır.
- HTTPS: HTTPS bağlantısı zorunludur. wss kullanılmalıdır.
- Form Doğrulama: Formlar ve kullanıcı girişleri doğrulanmalıdır.
- Çevresel Değişkenler: Şifreleme anahtarları ve API anahtarları .env dosyasında saklanmalı ve git tarafından görmezden gelinmelidir.

```
Lütfen güçlü bir şifre karma algoritması kullandığınızdan emin olun.
```

```
Açık güvenlik nedenleriyle, tüm kimlik bilgileri, API anahtarları, env değişkenleri vb. yerel olarak bir .env dosyasına kaydedilmeli ve git tarafından göz ardı edilmelidir. Herkese açık olarak saklanan kimlik bilgileri sizi doğrudan projenin başarısızlığına yönlendirecektir.
```

---

### Chapter IV

#### Modüller

- Projenizin %25'ini tamamladınız ve temel web siteniz işlevsel durumda.
- Projeyi %100'e tamamlamak için en az 7 ana modül gereklidir.
- Her modül projede değişiklikler gerektirebilir, bu yüzden tüm konuyu dikkatlice okuyun.
- Kütüphaneler veya çerçeveler kullanımı genellikle yasaktır, ancak kullanılan araçların gerekçelendirilmesi gerekmektedir.

```
İşinizin yerini alacak kütüphanelerin, çerçevelerin veya araçların kullanılması kesinlikle yasaktır. Konunun her bölümü, kullanabileceğiniz yetkili üçüncü taraf yazılımları açıkça sunacaktır. Bununla birlikte, belirli eylemleri basitleştirmek için mümkün olan her şeyin kullanılmasına izin verilir ve hatta tavsiye edilir. Kullanılan herhangi bir araç veya kaynağın gerekçelendirilmesi gerektiğini unutmamak önemlidir. Lütfen basitleştirmenin işinizi tamamlamak anlamına gelmediğini unutmayın.
```

```
Küçük Modüller: İki küçük modül, bir büyük modül ile eşdeğerdir.
```

#### IV.1 Genel Bakış

- #### Web:

  - **Büyük Modül:** Backend için bir çerçeve kullanın.
  - **Küçük Modül:** Front-end çerçevesi veya aracı kullanın.
  - **Küçük Modül:** Backend için bir veritabanı kullanın.
  - **Büyük Modül:** Turnuva skorlarını Blockchain'de saklayın.

- #### Kullanıcı Yönetimi:

  - **Büyük Modül:** Standart kullanıcı yönetimi, kimlik doğrulama, turnuvalar arası kullanıcı yönetimi.
  - **Büyük Modül:** Uzaktan kimlik doğrulama.

- #### Oyun ve Kullanıcı Deneyimi:

  - **Büyük Modül:** Uzaktan oyuncular.
  - **Büyük Modül:** Aynı oyunda birden fazla oyuncu.
  - **Büyük Modül:** Kullanıcı geçmişi ve eşleşme ile başka bir oyun ekleme.
  - **Küçük Modül:** Oyun özelleştirme seçenekleri.
  - **Büyük Modül:** Canlı sohbet.

- #### AI-Algo:

  - **Büyük Modül:** AI Rakip ekleme.
  - **Küçük Modül:** Kullanıcı ve oyun istatistikleri panelleri.

- #### Siber Güvenlik:

  - **Büyük Modül:** WAF/ModSecurity ile Sert Konfigürasyon ve HashiCorp Vault ile Sırlar Yönetimi.
  - **Küçük Modül:** GDPR uyumluluğu, kullanıcı anonimleştirme, yerel veri yönetimi ve hesap silme seçenekleri.
  - **Büyük Modül:** İki Faktörlü Kimlik Doğrulama (2FA) ve JWT.

- #### DevOps:

  - **Büyük Modül:** Log Yönetimi için Altyapı Kurulumu.
  - **Küçük Modül:** İzleme sistemi.
  - **Büyük Modül:** Backend'i Mikroservisler olarak tasarlama.

- #### Grafikler:

  - **Büyük Modül:** İleri düzey 3D tekniklerinin kullanımı.

- #### Erişilebilirlik:

  - **Küçük Modül:** Tüm cihazlarda destek.
  - **Küçük Modül:** Tarayıcı uyumluluğunu genişletme.
  - **Küçük Modül:** Birden fazla dil desteği.
  - **Küçük Modül:** Görme engelli kullanıcılar için erişilebilirlik ekleme.
  - **Küçük Modül:** Sunucu Tarafı Render (SSR) entegrasyonu.

- #### Sunucu Tarafı Pong:

  - **Büyük Modül:** Temel Pong'u Sunucu Tarafı Pong ile değiştirme ve API entegrasyonu.
  - **Büyük Modül:** Web Kullanıcıları ile CLI üzerinden Pong oynama ve API entegrasyonu.

#### IV.2 Web

Bu modüller, Pong oyununuzda gelişmiş web özelliklerini entegre etmenizi sağlar.

- **Büyük Modül:** Bir Framework kullanarak backend oluşturun.
  Bu ana modülde, backend geliştirme için belirli bir web framework'ü kullanmanız gerekmektedir ve bu framework, Django'dur.
  Bu modülün kısıtlamaları olmadan, varsayılan dil/framework kullanarak bir backend oluşturabilirsiniz. Ancak, bu modül sadece ilişkili kısıtlamaları kullanırsanız geçerli olacaktır.
- **Küçük Modül:** Bir ön yüz framework'ü veya aracı kullanın.
  Ön yüz geliştirme için Bootstrap aracını kullanacaksınız.
  Bu modülün kısıtlamaları olmadan, varsayılan dil/framework kullanarak bir ön yüz oluşturabilirsiniz. Ancak, bu modül sadece ilişkili kısıtlamaları kullanırsanız geçerli olacaktır.
- **Küçük Modül:** Backend için bir veritabanı kullanın ve daha fazlası.
  Projenizdeki tüm veritabanı örnekleri için belirlenen veritabanı PostgreSQL'dir. Bu seçim, veri tutarlılığını ve projenin tüm bileşenleri arasında uyumluluğu garanti eder ve backend Framework modülü gibi diğer modüller için bir ön koşul olabilir.
- **Küçük Modül:** Bir turnuvanın skorlarını Blockchain'de saklayın.
  Bu ana modül, Pong web sitesinde turnuva skorlarını güvenli bir şekilde bir blockchain üzerine kaydetmek için bir özellik uygulamaya odaklanır. Geliştirme ve test amaçları için, bir test blockchain ortamı kullanılacaktır.
  Bu uygulama için seçilen blockchain, Ethereum'dur ve Solidity, akıllı sözleşme geliştirme için kullanılacak programlama dili olacaktır.
- Blockchain Entegrasyonu: Bu modülün birincil hedefi, blockchain teknolojisini, özellikle Ethereum'u, Pong web sitesine sorunsuz bir şekilde entegre etmektir. Bu entegrasyon, turnuva skorlarının güvenli ve değiştirilemez bir şekilde saklanmasını sağlar, oyunculara oyun başarılarının şeffaf ve manipüle edilemez bir kaydını sunar.
  - Solidity Akıllı Sözleşmeleri: Blockchain ile etkileşimde bulunmak için Solidity akıllı sözleşmeleri geliştireceğiz. Bu sözleşmeler, turnuva skorlarını kaydetmek, yönetmek ve geri almakla sorumlu olacak.
  - Test Blockchain: Daha önce belirtildiği gibi, geliştirme ve test amaçları için bir test blockchain kullanılacaktır. Bu, canlı bir blockchain ile ilişkili riskler olmadan blockchain ile ilgili tüm işlevlerin tamamen doğrulanmasını sağlar.
  - İşbirliği: Bu modülün diğer modüllerle, özellikle Backend Framework modülüyle, bağımlılıkları olabilir. Blockchain işlevselliğini entegre etmek, blockchain ile etkileşimleri sağlamak için backend'de ayarlamalar yapılmasını gerektirebilir.

Bu modülü uygulayarak, Pong web sitesini blockchain tabanlı bir skor saklama sistemiyle geliştiriyoruz. Kullanıcılar, oyun skorlarının bütünlüğünü sağlayan ek güvenlik ve şeffaflıktan faydalanacaklardır. Bu modül, blockchain geliştirme ile ilişkili riskleri en aza indirmek için bir test blockchain ortamının kullanılmasına vurgu yapar.

#### IV.3 Kullanıcı Yönetimi

Bu modül, Pong platformunda kullanıcı yönetimi, kullanıcı etkileşimleri ve erişim kontrolüyle ilgili kritik konuları ele alır. İki ana bileşenden oluşur ve her biri kullanıcı yönetimi ve kimlik doğrulama süreçlerinin temel unsurlarına odaklanır: kullanıcıların birden fazla turnuvaya katılımı ve uzaktan kimlik doğrulama sisteminin uygulanması.

- **Büyük Modül:** Standart kullanıcı yönetimi, kimlik doğrulama, turnuvalar arasında kullanıcılar.
  - Kullanıcılar, web sitesine güvenli bir şekilde abone olabilirler.
  - Kayıtlı kullanıcılar güvenli bir şekilde giriş yapabilirler.
  - Kullanıcılar, turnuvalarda oynamak için benzersiz bir gösterim adı seçebilirler.
  - Kullanıcılar, bilgilerini güncelleyebilirler.
  - Kullanıcılar bir avatar yükleyebilir; eğer yüklenmezse varsayılan bir avatar atanır.
  - Kullanıcılar, diğerlerini arkadaş olarak ekleyebilir ve çevrim içi durumlarını görüntüleyebilirler.
  - Kullanıcı profilleri, galibiyetler ve mağlubiyetler gibi istatistikleri gösterir.
  - Her kullanıcının, giriş yapmış kullanıcılar tarafından erişilebilen, 1v1 oyunları, tarihleri ve ilgili detayları içeren bir Maç Geçmişi vardır.

```
Aynı kullanıcı adı/e-posta yönetimi sizin takdirinize bağlıdır. Kararınıza yönelik bir gerekçe sunmanız gerekmektedir.
```

- **Büyük Modül:** uzaktan kimlik doğrulama uygulaması.
  Bu ana modülde, aşağıdaki kimlik doğrulama sistemini uygulamak hedeflenir:
  OAuth 2.0 ile 42 üzerinden kimlik doğrulama. Öne çıkan özellikler ve hedefler şunları içerir:
  - Kullanıcıların güvenli bir şekilde giriş yapabilmelerini sağlamak için kimlik doğrulama sistemini entegre edin.
  - Güvenli bir giriş sağlamak için yetkiliden gerekli kimlik bilgilerini ve izinleri alın.
  - En iyi uygulamalar ve güvenlik standartlarına uygun kullanıcı dostu giriş ve yetkilendirme akışlarını uygulayın.
  - Web uygulaması ile kimlik doğrulama sağlayıcısı arasında kimlik doğrulama token'larının ve kullanıcı bilgilerinin güvenli bir şekilde değişimini sağlayın.

```
Aynı kullanıcı adı/e-posta yönetimi sizin takdirinize bağlıdır. Kararınıza yönelik bir gerekçe sunmanız gerekmektedir.
```

Bu ana modül, kullanıcılara web uygulamasına güvenli ve kullanışlı bir şekilde erişim sağlamak için uzaktan kullanıcı kimlik doğrulaması gerçekleştirmeyi amaçlar.

#### IV.4 Oynanış ve Kullanıcı Deneyimi

Bu modüller, projenin genel oynanışını geliştirmek için tasarlanmıştır.

- **Büyük Modül:** Uzak Oyuncular
  - İki uzak oyuncuya sahip olmak mümkündür. Her oyuncu, ayrı bir bilgisayarda bulunur, aynı web sitesine erişir ve aynı Pong oyununu oynar.

```
Ağ sorunlarını düşünün, beklenmedik bağlantı kopmaları veya gecikmeler gibi. En iyi kullanıcı deneyimini sunmanız gerekiyor.
```

- **Büyük Modül:** Çoklu Oyuncular

  - İkiden fazla oyuncuya sahip olmak mümkündür. Her oyuncunun canlı bir kontrolü olması gerekir (bu yüzden önceki "Uzak Oyuncular" modülü şiddetle tavsiye edilir). Oyunun 3, 4, 5, 6... oyuncu ile nasıl oynanacağını tanımlamak size kalmış. Normal 2 oyunculu oyunun yanı sıra, bu çok oyunculu modül için 2'den büyük tek bir oyuncu sayısı seçebilirsiniz. Örneğin: 4 oyuncu kare şeklinde bir tahtada oynayabilir, her oyuncu karenin bir kenarına sahip olur.

- **Büyük Modül:** Kullanıcı Geçmişi ve Eşleştirme ile Başka Bir Oyun Ekleme. Bu ana modülde, Pong'dan farklı yeni bir oyun tanıtmak ve kullanıcı geçmişi takibi ve eşleştirme gibi özellikleri entegre etmek amaçlanır. Ana özellikler ve hedefler şunlardır:

  - Platformun tekliflerini çeşitlendirmek ve kullanıcıları eğlendirmek için yeni, ilgi çekici bir oyun geliştirin.
  - Bireysel kullanıcıların oyun oynama istatistiklerini kaydetmek ve görüntülemek için kullanıcı geçmişi takibi uygulayın.
  - Kullanıcıların rakip bulmasını ve adil ve dengeli maçlara katılmasını sağlamak için bir eşleştirme sistemi oluşturun.
  - Kullanıcı oyun geçmişi ve eşleştirme verilerinin güvenli bir şekilde saklandığından ve güncel tutulduğundan emin olun.
  - Yeni oyunun performansını ve tepkiselliğini optimize ederek keyifli bir kullanıcı deneyimi sağlayın. Oyun hatalarını düzeltmek, yeni özellikler eklemek ve oynanışı geliştirmek için düzenli olarak güncelleyin ve bakım yapın.

Bu ana modül, platformunuza yeni bir oyun ekleyerek kullanıcı etkileşimini artırmayı, oyun geçmişi ile oynanışı takip etmeyi ve keyifli bir oyun deneyimi için eşleştirmeyi sağlamayı amaçlar.

- **Küçük Modül:** Oyun Özelleştirme Seçenekleri. Bu alt modülde, platformdaki tüm mevcut oyunlar için özelleştirme seçenekleri sunmak hedeflenir. Ana özellikler ve hedefler şunlardır:

  - Oynanışı geliştiren güçlendirmeler, saldırılar veya farklı haritalar gibi özelleştirme özellikleri sunun.
  - Daha basit bir deneyim tercih eden kullanıcılar için temel özelliklere sahip bir varsayılan oyun sürümünü seçme imkanı sunun.
  - Özelleştirme seçeneklerinin platformda sunulan tüm oyunlar için geçerli ve uygulanabilir olmasını sağlayın.
  - Oyun parametrelerini ayarlamak için kullanıcı dostu ayar menüleri veya arayüzler uygulayın.
  - Tüm oyunlar arasında tutarlı bir özelleştirme özellikleri sağlayarak birleşik bir kullanıcı deneyimi sunun.

Bu modül, kullanıcıların tüm mevcut oyunlarda çeşitli özelleştirme seçenekleri sunarak oyun deneyimlerini kendilerine göre uyarlamalarına imkan tanımayı, aynı zamanda daha basit bir oyun deneyimi sunmayı amaçlar.

- **Büyük Modül:** Canlı Sohbet. Bu modülde, kullanıcılarınız için bir sohbet oluşturmanız gerekiyor:
  - Kullanıcı, diğer kullanıcılara doğrudan mesajlar gönderebilmelidir.
  - Kullanıcı, diğer kullanıcıları engelleyebilmelidir. Bu şekilde, engellediği hesaptan gelen mesajları artık görmeyecektir.
  - Kullanıcı, sohbet arayüzü üzerinden diğer kullanıcıları Pong oyunu oynamaya davet edebilmelidir.
  - Turnuva sistemi, sonraki oyun için beklenen kullanıcılara uyarı verebilmelidir.
  - Kullanıcı, sohbet arayüzü üzerinden diğer oyuncuların profillerine erişebilmelidir.

#### IV.5 AI-Algo

Bu modüller, projeye veri odaklı unsurlar eklemeyi amaçlar. Ana modül, oynanışı geliştirmek için bir yapay zeka (AI) rakibini tanıtırken, alt modül, kullanıcı ve oyun istatistik panellerine odaklanarak kullanıcıların oyun deneyimlerine minimalist ama bilgilendirici bir bakış sunar.

- **Büyük Modül:** Bir AI Rakip Tanıtın.

  - Bu ana modülde, oyuna bir AI oyuncu entegre etmek amaçlanır. Bu görevde A\* algoritmasının kullanılması yasaktır. Ana özellikler ve hedefler şunlardır:

    - Kullanıcılara zorlu ve ilgi çekici bir oyun deneyimi sunacak bir AI rakip geliştirin.
    - AI, insan davranışını taklit etmelidir, yani AI uygulamanızda klavye girişini simüle etmelisiniz. Buradaki kısıtlama, AI'nin oyunun görünümünü yalnızca saniyede bir yenileyebilmesi, bu nedenle sıçramaları ve diğer eylemleri öngörmesi gerektiğidir.
    - AI, Oyun özelleştirme seçenekleri modülünü uyguladıysanız güçlendirmeleri kullanmalıdır. (Burası mavi bir kutu içinde)
    - AI oyuncunun zekice ve stratejik hamleler yapmasını sağlayacak AI mantığı ve karar verme süreçlerini uygulayın.
    - A\* algoritmasına başvurmadan etkili bir AI oyuncu oluşturmak için alternatif algoritmalar ve teknikler keşfedin.
    - AI'nin farklı oyun senaryolarına ve kullanıcı etkileşimlerine uyum sağladığından emin olun.

```
AI'nizin nasıl çalıştığını değerlendirmeniz sırasında ayrıntılı bir şekilde açıklamanız gerekecek. Hiçbir şey yapmayan bir AI oluşturmak kesinlikle yasaktır; AI ara sıra kazanma yeteneğine sahip olmalıdır.
```

Bu ana modül, A\* algoritmasına başvurmadan heyecan ve rekabet katan bir AI rakip tanıtarak oyunu geliştirmeyi amaçlar.

- **Küçük Modül:** Kullanıcı ve Oyun İstatistik Panelleri. Bu alt modülde, bireysel kullanıcılar ve oyun oturumları için istatistikleri gösteren paneller sunmak amaçlanır. Ana özellikler ve hedefler şunlardır:
  - Kullanıcıların kendi oyun istatistiklerine dair bilgiler edinmelerini sağlayacak kullanıcı dostu paneller oluşturun.
  - Her maç için ayrıntılı istatistikleri, sonuçları ve geçmiş verileri gösteren ayrı bir oyun oturumu paneli geliştirin.
  - Panellerin, verileri takip etmek ve analiz etmek için sezgisel ve bilgilendirici bir kullanıcı arayüzü sunduğundan emin olun.
  - İstatistikleri net ve görsel olarak çekici bir şekilde sunmak için grafikler ve tablolar gibi veri görselleştirme tekniklerini uygulayın.
  - Kullanıcıların kendi oyun geçmişlerine ve performans metriklerine kolayca erişip keşfetmelerini sağlayın.
  - Yararlı olduğunu düşündüğünüz ek metrikleri eklemekten çekinmeyin.

Bu alt modül, kullanıcıların oyun istatistiklerini ve oyun oturumu detaylarını takip etmelerini sağlayarak oyun deneyimlerine kapsamlı bir bakış sunmayı amaçlar.

#### IV.6 Siber Güvenlik

Bu siber güvenlik modülleri, projeyi güçlendirmek için tasarlanmıştır. Ana modül, Web Uygulama Güvenlik Duvarı (WAF) ve ModSecurity yapılandırmalarıyla birlikte HashiCorp Vault'u kullanarak güvenlik önlemlerini artırmaya odaklanırken, alt modüller GDPR uyumluluğu, kullanıcı verilerinin anonimleştirilmesi, hesap silme, iki faktörlü kimlik doğrulama (2FA) ve JSON Web Tokens (JWT) seçenekleri sunarak veri koruma, gizlilik ve kimlik doğrulama güvenliğine olan bağlılığı pekiştirir.

- **Büyük Modül:** WAF/ModSecurity ve HashiCorp Vault ile Güçlendirilmiş Yapılandırma ve Güvenlik Yönetimi Uygulayın.

  - Bu ana modülde, projeye çeşitli önemli bileşenleri entegre ederek güvenlik altyapısını geliştirmek amaçlanır. Ana özellikler ve hedefler şunlardır:
    - Web tabanlı saldırılara karşı koruma sağlamak için sıkı ve güvenli bir yapılandırma ile Web Uygulama Güvenlik Duvarı (WAF) ve ModSecurity yapılandırın ve dağıtın.
    - API anahtarları, kimlik bilgileri ve ortam değişkenleri gibi hassas bilgileri güvenli bir şekilde yönetmek ve depolamak için HashiCorp Vault'u entegre edin, bu sırada bu sırların uygun şekilde şifrelenip izole edildiğinden emin olun.
  - Bu ana modül, web uygulama koruması için WAF/ModSecurity ve güvenli bir ortam sağlamak için HashiCorp Vault kullanarak projenin güvenlik altyapısını güçlendirmeyi amaçlar.

- **Küçük Modül:** Kullanıcı Anonimleştirme, Yerel Veri Yönetimi ve Hesap Silme ile GDPR Uyumluluğu Seçenekleri.

  - Bu alt modülde, kullanıcıların veri gizliliği haklarını kullanmalarını sağlayan GDPR uyumluluğu seçenekleri sunmak amaçlanır. Ana özellikler ve hedefler şunlardır:

    - Kullanıcıların kişisel verilerinin anonimleştirilmesini talep etmelerini sağlayacak GDPR uyumlu özellikler uygulayın ve böylece kimliklerinin ve hassas bilgilerinin korunduğundan emin olun.
    - Kullanıcıların sistemde saklanan kişisel bilgilerini görüntüleme, düzenleme veya silme yeteneği de dahil olmak üzere yerel veri yönetim araçları sağlayın.
    - Kullanıcılara, hesaplarının ve ilişkili tüm verilerin kalıcı olarak silinmesini talep etmeleri için basit bir süreç sunarak veri koruma düzenlemelerine uyumluluğu sağlayın.
    - Kullanıcılara veri gizliliği hakları konusunda net ve şeffaf bir iletişim sağlayarak bu hakları kullanma seçeneklerini kolay erişilebilir hale getirin.

  - Bu alt modül, kullanıcılara sistemdeki kişisel bilgilerini kontrol etme ve veri gizliliği haklarını kullanma imkanı sunarak kullanıcı gizliliğini ve veri korumasını geliştirmeyi amaçlar.

  - Genel Veri Koruma Yönetmeliği'ni (GDPR) tanımıyorsanız, özellikle kullanıcı verileri yönetimi ve gizliliği konularında bu düzenlemenin ilkelerini ve etkilerini anlamak önemlidir. GDPR, Avrupa Birliği (AB) ve Avrupa Ekonomik Alanı (EEA) içindeki bireylerin kişisel verilerini ve gizliliğini korumayı amaçlayan bir düzenlemedir. Kuruluşların kişisel verileri nasıl ele alması ve işlemesi gerektiği konusunda katı kurallar ve yönergeler belirler.
  - GDPR ve gereksinimlerini daha iyi anlamak için, Avrupa Komisyonu'nun veri koruma konusundaki resmi web sitesini ziyaret etmek şiddetle tavsiye edilir. Bu web sitesi, GDPR'nin ilkeleri, hedefleri ve kullanıcı hakları hakkında kapsamlı bilgiler sağlar. Ayrıca, bu konuyu daha ayrıntılı incelemek ve düzenlemeye uyum sağlamak için ek kaynaklar da sunar.
  - GDPR'yi tanımıyorsanız, lütfen sağlanan bağlantıyı ziyaret edin ve bu projeye başlamadan önce düzenlemeleri öğrenin.

- **Büyük Modül:** İki Faktörlü Kimlik Doğrulama (2FA) ve JWT Uygulaması

  - Bu ana modülde, kullanıcı hesaplarının güvenliğini artırmak amacıyla İki Faktörlü Kimlik Doğrulama (2FA) ve JSON Web Tokens (JWT) kullanımı hedeflenir. Ana özellikler ve hedefler şunlardır:
    - Kullanıcı hesapları için ek bir güvenlik katmanı olarak İki Faktörlü Kimlik Doğrulama (2FA) uygulayın, kullanıcıların şifrelerinin yanı sıra bir seferlik kod gibi ikincil bir doğrulama yöntemi sağlamalarını gerektirin.
    - Kullanıcı oturumlarını ve kaynaklara erişimi güvenli bir şekilde yönetmek için JSON Web Tokens (JWT) kullanarak kimlik doğrulama ve yetkilendirme işlemlerini güvence altına alın.
    - SMS kodları, kimlik doğrulama uygulamaları veya e-posta tabanlı doğrulama gibi seçeneklerle 2FA etkinleştirme sürecini kullanıcı dostu hale getirin.
    - Kullanıcı hesaplarına ve hassas verilere yetkisiz erişimi önlemek için JWT tokenlarının güvenli bir şekilde verildiğinden ve doğrulandığından emin olun.
  - Bu ana modül, İki Faktörlü Kimlik Doğrulama (2FA) sunarak kullanıcı hesabı güvenliğini güçlendirmeyi ve JSON Web Tokens (JWT) kullanarak kimlik doğrulama ve yetkilendirmeyi geliştirmeyi amaçlar.

#### IV.7 DevOps

Bu modüller, projenin altyapısını ve mimarisini geliştirmeye odaklanır. Ana modüller, günlük yönetimi için ELK (Elasticsearch, Logstash, Kibana) kullanarak altyapı kurulumunu, arka ucu mikroservisler olarak tasarlamayı ve kapsamlı sistem izleme için Prometheus/Grafana uygulamayı içerir.

- **Büyük Modül:** ELK (Elasticsearch, Logstash, Kibana) ile Altyapı Kurulumu
  Bu ana modülün amacı, ELK yığını (Elasticsearch, Logstash, Kibana) kullanarak sağlam bir günlük yönetimi ve analiz altyapısı oluşturmaktır. Temel özellikler ve hedefler şunlardır:

  - Elasticsearch'ü günlük verilerini verimli bir şekilde depolamak ve dizinlemek için dağıtmak, verileri kolayca aranabilir ve erişilebilir hale getirmek.
  - Logstash'i çeşitli kaynaklardan günlük verilerini toplamak, işlemek ve dönüştürmek için yapılandırmak ve bu verileri Elasticsearch'e göndermek.
  - Kibana'yı günlük verilerini görselleştirmek, panolar oluşturmak ve günlük olaylardan içgörüler elde etmek için kurmak.
  - Günlük verilerinin depolanmasını etkili bir şekilde yönetmek için veri saklama ve arşivleme politikalarını tanımlamak.
  - Günlük verilerini ve ELK yığını bileşenlerine erişimi korumak için güvenlik önlemleri uygulamak.
  - Bu ana modül, ELK yığını kullanarak güçlü bir günlük yönetim ve analiz sistemi kurmayı hedefler ve sistemin operasyonu ve performansı hakkında etkili sorun çözme, izleme ve içgörüler sağlar.

- **Küçük Modül:** İzleme Sistemi. Bu küçük modülün amacı, Prometheus ve Grafana kullanarak kapsamlı bir izleme sistemi kurmaktır. Temel özellikler ve hedefler şunlardır:

  - Prometheus'u metrikleri toplamak ve çeşitli sistem bileşenlerinin sağlık ve performansını izlemek için izleme ve uyarı aracı olarak dağıtmak.
  - Farklı hizmetler, veritabanları ve altyapı bileşenlerinden metrikleri yakalamak için veri ihracatçıları ve entegrasyonlar yapılandırmak.
  - Grafana kullanarak sistem metrikleri ve performansı hakkında gerçek zamanlı içgörüler sağlayan özel panolar ve görselleştirmeler oluşturmak.
  - Prometheus'ta kritik sorunları ve anormallikleri proaktif olarak tespit etmek ve yanıtlamak için uyarı kuralları oluşturmak.
  - Tarihsel metrik verileri için uygun veri saklama ve depolama stratejileri sağlamak.
  - Grafana için güvenli kimlik doğrulama ve erişim kontrol mekanizmaları uygulamak ve hassas izleme verilerini korumak.
  - Bu küçük modül, Prometheus ve Grafana kullanarak sağlam bir izleme altyapısı kurmayı ve sistem metriklerinde gerçek zamanlı görünürlük sağlamak ve sistem performansı ile güvenilirliğini artırmak için proaktif sorun tespiti sağlamayı hedefler.

- **Büyük Modül:** Arka Ucu Mikroservisler Olarak Tasarlamak. Bu ana modülün amacı, sistemin arka ucunu mikroservisler yaklaşımı kullanarak mimarilendirmektir. Temel özellikler ve hedefler şunlardır:

  - Arka ucu daha küçük, gevşek bağlı mikroservislere bölmek, her birinin belirli işlevler veya özelliklerden sorumlu olmasını sağlamak.
  - Mikroservisler arasında bağımsız geliştirme, dağıtım ve ölçekleme sağlamak için net sınırlar ve arayüzler tanımlamak.
  - Mikroservisler arasında veri alışverişi ve koordinasyon sağlamak için RESTful API'ler veya mesaj kuyrukları gibi iletişim mekanizmaları uygulamak.
  - Her mikroservisin tek bir, iyi tanımlanmış görev veya iş yeteneğinden sorumlu olmasını sağlamak, bakım ve ölçeklenebilirliği teşvik etmek.
  - Bu ana modül, mikroservisler tasarım yaklaşımını benimseyerek sistemin mimarisini geliştirmeyi ve arka uç bileşenlerinin daha büyük esneklik, ölçeklenebilirlik ve bakım kolaylığı sağlamasını hedefler.

#### IV.8 Oyun

Bu modüller, projenin oyunlaştırma yönünü geliştirmeye odaklanır. Ana modül, yeni oyunlar eklemeyi, kullanıcı geçmişi takibini ve eşleştirmeyi tanıtırken, küçük modül tüm mevcut oyunlar için özelleştirme seçenekleri sunmaya odaklanır.

- **Büyük Modül:** Kullanıcı Geçmişi ve Eşleştirme ile Yeni Bir Oyun Eklemek. Bu ana modülün amacı, Pong'tan farklı yeni bir oyun tanıtmaktır ve kullanıcı geçmişi takibi ve eşleştirme gibi özellikleri içermektir. Temel özellikler ve hedefler şunlardır:

  - Platformun tekliflerini çeşitlendirmek ve kullanıcıları eğlendirmek için yeni, ilgi çekici bir oyun geliştirmek.
  - Bireysel kullanıcıların oyun istatistiklerini kaydetmek ve görüntülemek için kullanıcı geçmişi takibini uygulamak.
  - Kullanıcıların rakip bulmasına ve adil ve dengeli maçlara katılmasına olanak tanıyan bir eşleştirme sistemi oluşturmak.
  - Kullanıcı oyun geçmişi ve eşleştirme verilerinin güvenli bir şekilde saklanmasını ve güncel kalmasını sağlamak.
  - Yeni oyunun performansını ve yanıt verebilirliğini optimize etmek, kullanıcı deneyimini keyifli hale getirmek. Oyunu düzenli olarak güncellemek ve bakımını yapmak, hataları düzeltmek, yeni özellikler eklemek ve oyun oynanışını geliştirmek.
  - Bu ana modül, platformunuzu yeni bir oyun tanıtarak genişletmeyi, kullanıcı etkileşimini oyun geçmişi ile artırmayı ve keyifli bir oyun deneyimi için eşleştirme sağlamayı hedefler.

- **Küçük Modül:** Oyun Özelleştirme Seçenekleri. Bu küçük modülün amacı, platformdaki tüm mevcut oyunlar için özelleştirme seçenekleri sunmaktır. Temel özellikler ve hedefler şunlardır:

  - Oyun deneyimini geliştiren güçlendirmeler, saldırılar veya farklı haritalar gibi özelleştirme özellikleri sunmak.
  - Kullanıcılara daha basit bir deneyim tercih ederlerse oyunun temel özelliklere sahip bir varsayılan sürümünü seçme imkanı vermek.
  - Özelleştirme seçeneklerinin platformdaki tüm oyunlar için mevcut ve uygulanabilir olduğundan emin olmak.
  - Oyun parametrelerini ayarlamak için kullanıcı dostu ayar menüleri veya arayüzleri uygulamak.
  - Özelleştirme özelliklerinde tutarlılığı sağlamak, böylece tüm oyunlarda birleştirilmiş bir kullanıcı deneyimi sunmak.
  - Bu modül, kullanıcıların tüm mevcut oyunlar arasında oyun deneyimlerini özelleştirme esnekliği sunarak, çeşitli özelleştirme seçenekleri sağlamayı ve basit bir oyun deneyimi tercih edenler için varsayılan bir sürüm sunmayı hedefler.

#### IV.9 Grafik

- **Büyük Modül:** Gelişmiş 3D Tekniklerini Uygulamak. Bu ana modül, Pong oyunundaki görsel unsurları geliştirmeye odaklanır. Oyunun daha sürükleyici bir deneyim sunmasını sağlamak için gelişmiş 3D tekniklerinin kullanılmasını tanıtır. Özellikle Pong oyunu ThreeJS/WebGL kullanılarak geliştirilir.

  - Gelişmiş 3D Grafikler: Bu modülün ana hedefi, Pong oyununun görsel kalitesini artırmak için gelişmiş 3D grafik tekniklerini uygulamaktır. ThreeJS/WebGL kullanarak oyuncuları oyun ortamına çekici bir şekilde dahil eden etkileyici görsel efektler yaratmayı amaçlarız.
  - Sürükleyici Oynanış: Gelişmiş 3D tekniklerinin uygulanması, kullanıcıların görsel olarak etkileyici ve ilgi çekici bir Pong oyunu deneyimi yaşamasını sağlar.
  - Teknoloji Entegrasyonu: Bu modül için seçilen teknoloji ThreeJS/WebGL'dir. Bu araçlar 3D grafiklerin oluşturulması için kullanılacak, uyumluluk ve optimum performans sağlanacaktır.
  - Bu ana modül, Pong oyununun görsel unsurlarını devrim niteliğinde değiştirerek, ThreeJS/WebGL kullanarak oyunculara sürükleyici ve görsel olarak etkileyici bir oyun deneyimi sunmayı hedefler.

#### IV.10 Erişilebilirlik

Bu modüller, web uygulamamızın erişilebilirliğini artırmaya odaklanır. Tüm cihazlarla uyumluluğu sağlama, tarayıcı desteğini genişletme, çoklu dil desteği sunma, görme engelli kullanıcılar için erişilebilirlik özellikleri sağlama ve performansı artırmak için Sunucu Tarafı Rendering (SSR) entegrasyonunu içerir.

- **Küçük Modül:** Tüm Cihazlarda Destek. Bu modülün ana odağı, web sitenizin tüm cihazlarda sorunsuz çalışmasını sağlamaktır. Temel özellikler ve hedefler şunlardır:

  - Web sitesinin yanıt verebilir olmasını sağlamak, farklı ekran boyutlarına ve yönlerine uyum sağlamasını, masaüstü, dizüstü bilgisayar, tablet ve akıllı telefonlarda tutarlı bir kullanıcı deneyimi sunmasını sağlamak.
  - Kullanıcıların farklı giriş yöntemleriyle (dokunmatik ekranlar, klavyeler ve fareler) web sitesini kolayca gezinebilmelerini ve etkileşimde bulunmalarını sağlamak.
  - Bu modül, tüm cihazlarda tutarlı ve kullanıcı dostu bir deneyim sunarak erişilebilirliği ve kullanıcı memnuniyetini maksimize etmeyi hedefler.

- **Küçük Modül:** Tarayıcı Uyumluluğunu Genişletme. Bu küçük modülün amacı, web uygulamasının uyumluluğunu artırmak için ek bir web tarayıcısını desteklemektir. Temel özellikler ve hedefler şunlardır:

  - Web uygulamasının ek bir web tarayıcısında çalışmasını sağlamak, böylece kullanıcıların uygulamayı sorunsuz bir şekilde erişmesini ve kullanmasını sağlamak.
  - Yeni desteklenen tarayıcıda web uygulamasının doğru şekilde çalışmasını ve görüntülenmesini sağlamak için kapsamlı testler ve optimizasyonlar yapmak.
  - Eklenen web tarayıcısındaki uyumluluk sorunlarını veya render farklılıklarını gidermek.
  - Tüm desteklenen tarayıcılarda tutarlı bir kullanıcı deneyimi sağlamak, kullanılabilirliği ve işlevselliği korumak.
  - Bu küçük modül, web uygulamasının erişilebilirliğini genişleterek daha fazla tarayıcı seçeneği sunmayı ve kullanıcıların tarayıcı deneyimlerini artırmayı hedefler.

- **Küçük Modül:** Çoklu Dil Desteği, Bu küçük modülün amacı, web sitenizin çeşitli kullanıcı tabanına hitap edebilmesi için birden fazla dili desteklemesini sağlamaktır. Temel özellikler ve hedefler şunlardır:

  - Web sitesinde en az üç dili desteklemek, geniş bir kitleye hitap etmek.
  - Kullanıcıların tercihlerine göre web sitesinin dilini kolayca değiştirebilmeleri için bir dil değiştirme aracı veya seçici sağlamak.
  - Navigasyon menüleri, başlıklar ve ana bilgiler gibi temel web sitesi içeriklerini desteklenen dillere çevirmek.
  - Kullanıcıların seçilen dil ne olursa olsun web sitesini sorunsuz bir şekilde gezinebilmelerini ve etkileşimde bulunmalarını sağlamak.
  - Çeviri sürecini basitleştirmek ve farklı diller arasında tutarlılığı korumak için dil paketleri veya yerelleştirme kütüphanelerini kullanmayı düşünmek.
  - Kullanıcıların tercih ettikleri dili web sitesinin sonraki ziyaretlerinde varsayılan seçim olarak ayarlamalarına izin vermek.
  - Bu küçük modül, web sitenizin erişilebilirliğini ve kapsayıcılığını artırarak içeriği birden fazla dilde sunmayı ve çeşitli uluslararası bir kitleye daha kullanıcı dostu hale getirmeyi hedefler.

- **Küçük Modül:** Görme Engelli Kullanıcılar İçin Erişilebilirlik Sağlama. Bu küçük modülün amacı, web sitenizin görme engelli kullanıcılar için daha erişilebilir hale getirilmesini sağlamaktır. Temel özellikler şunlardır:

  - Ekran okuyucuları ve yardımcı teknolojiler için destek.
  - Görseller için net ve açıklayıcı alternatif metinler.
  - Okunabilirlik için yüksek kontrastlı renk şeması.
  - Klavye navigasyonu ve odak yönetimi.
  - Metin boyutunu ayarlama seçenekleri.
  - Erişilebilirlik standartlarına uygunluğu sağlamak için düzenli güncellemeler.
  - Bu modül, web sitesinin görme engelli bireyler için kullanılabilirliğini artırmayı ve erişilebilirlik standartlarına uygunluğunu sağlamayı hedefler.

- **Küçük Modül:** Sunucu Tarafı Rendering (SSR) Entegrasyonu. Bu küçük modülün odağı, web sitenizin performansını ve kullanıcı deneyimini artırmak için Sunucu Tarafı Rendering (SSR) entegrasyonudur. Temel hedefler şunlardır:

  - Web sitesinin yüklenme hızını ve genel performansını iyileştirmek için SSR uygulamak.
  - İçeriğin sunucuda önceden render edilmesini ve kullanıcılara daha hızlı ilk sayfa yüklemeleri sağlamak.
  - SEO'yu optimize etmek için arama motorlarına önceden render edilmiş HTML içeriği sağlamak.
  - SSR'in avantajlarından yararlanırken tutarlı bir kullanıcı deneyimi sağlamak.
  - Bu modül, web sitesi performansını ve SEO'yu artırarak daha hızlı sayfa yüklemeleri ve geliştirilmiş kullanıcı deneyimi sağlamayı hedefler.

#### IV.11 Sunucu Tarafı Pong

- **Büyük Modül:** Temel Pong'u Sunucu Tarafı Pong ile Değiştirme ve Bir API Uygulama. Bu ana modülün amacı, temel Pong oyununu sunucu tarafı Pong ile değiştirmek ve bir API uygulamaktır. Temel özellikler ve hedefler şunlardır:

  - Pong oyununun sunucu tarafı mantığını geliştirmek, oyun oynanışını, top hareketini, skorlama ve oyuncu etkileşimlerini yönetmek.
  - Pong oyunu ile etkileşimde bulunmak için gerekli kaynakları ve uç noktaları sunan bir API oluşturmak, komut satırı arayüzü (CLI) ve web arayüzü aracılığıyla oyunun kısmi kullanımını sağlamak.
  - Oyun başlatma, oyuncu kontrolleri ve oyun durumu güncellemeleri destekleyen API uç noktalarını tasarlamak ve uygulamak.
  - Sunucu tarafı Pong oyununun yanıt verebilir olmasını sağlamak, ilgi çekici ve keyifli bir oyun deneyimi sunmak.
  - Sunucu tarafı Pong oyununu web uygulaması ile entegre etmek, kullanıcıların oyunu doğrudan web sitesinde oynamalarını sağlamak.
  - Bu ana modül, Pong oyununu sunucu tarafına taşıyarak ve API sunarak oyunun etkileşimli bir web arayüzü ve CLI aracılığıyla erişilebilirliğini artırmayı hedefler.

- **Büyük Modül:** CLI Üzerinden Web Kullanıcılarına Karşı Pong Oynanışını Sağlama ve API Entegrasyonu. Bu ana modülün amacı, kullanıcıların web sürümündeki oyunculara karşı Pong oynayabilecekleri bir Komut Satırı Arayüzü (CLI) geliştirmektir. CLI, web uygulaması ile sorunsuz bir şekilde bağlanmalı ve CLI kullanıcılarının web oyuncuları ile etkileşime girmesine olanak tanımalıdır. Temel özellikler ve hedefler şunlardır:

  - Pong oynanış deneyimini web sitesinde bulunanla benzer şekilde yeniden oluşturan sağlam bir CLI uygulaması oluşturmak, CLI kullanıcılarının Pong maçları başlatmasına ve katılmasına olanak tanımak.
  - CLI ile web uygulaması arasında iletişimi sağlamak için API'yi kullanmak, CLI kullanıcılarının siteye bağlanmasını ve web oyuncuları ile etkileşime girmesini sağlamak.
  - CLI içinde bir kullanıcı kimlik doğrulama mekanizması geliştirmek, CLI kullanıcılarının web uygulamasına güvenli bir şekilde giriş yapmasını sağlamak.
  - CLI ve web kullanıcıları arasında gerçek zamanlı senkronizasyon sağlamak, oyun oynanış etkileşimlerinin sorunsuz ve tutarlı olmasını sağlamak.
  - CLI kullanıcılarının web oyuncuları ile Pong maçlarına katılmasına ve maçlar oluşturmasına izin vermek, platformlar arası oynanışı teşvik etmek.
  - CLI'nin web kullanıcılarına karşı Pong maçları için etkili bir şekilde nasıl kullanılacağına dair kapsamlı belgeler ve kılavuzlar sağlamak.
  - Bu ana modül, CLI kullanıcılarını web oyuncuları ile API entegrasyonu aracılığıyla sorunsuz bir şekilde bağlayarak Pong oyun deneyimini geliştirmeyi hedefler ve birleşik bir etkileşimli oyun ortamı sunar.

```
Bu modülü yapmak istiyorsanız bir önceki modülü yapmanızı şiddetle tavsiye ederiz.
```

### Chapter V

#### Bonus Bölüm

Bu proje için, bonus kısmı oldukça basit bir şekilde tasarlanmıştır. Daha fazla modül eklemeniz gerekmektedir.

- Küçük modüller için beş puan ödüllendirilecektir.
- Ana modüller için on puan ödüllendirilecektir.

```
Bonus kısmı yalnızca zorunlu kısmın MÜKEMMEL olması durumunda değerlendirilecektir. Mükemmel, zorunlu olan kısmın bütünleşik olarak yapılmış olduğu ve arızalanmadan çalıştığı anlamına gelir. TÜM zorunlu şartları geçemediyseniz, bonus bölümünüz hiçbir şekilde değerlendirilmeyecektir.
```
