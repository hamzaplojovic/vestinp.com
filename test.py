
from datetime import datetime
from itertools import groupby
from operator import itemgetter
data = [
        {
            "domain": "sandzakpress.net",
            "url": "https://sandzakpress.net/zoranic-priznao-kradju-telefona-novinaru-feticu-osudjen-na-5-mjeseci-uslovne-kazne/?utm_source=rss&utm_medium=rss&utm_campaign=zoranic-priznao-kradju-telefona-novinaru-feticu-osudjen-na-5-mjeseci-uslovne-kazne",
            "title": "Zorani\u0107 priznao kra\u0111u telefona novinaru Feti\u0107u \u2013 Osu\u0111en na 5 mjeseci uslovne kazne",
            "short_summary": "Direktor Sand\u017eak media centra Salahudin Feti\u0107 saop\u0161tio je danas da mu je nakon 3 godine i 8 mjeseci vo\u0111enja postupka pred policijskim, tu\u017eila\u010dkim i sudskim organima, od strane Osnovnog suda u Novom Pazaru, vra\u0107en mobilni telefon koji mu je otet u Skup\u0161tini grada Novog Pazara 15.10.2018. godine i to u trenutku dok je u svojstvu",
            "views": 1518
        },
        {
            "domain": "sandzakpress.net",
            "url": "https://sandzakpress.net/novi-pazar-u-toku-izgradnja-skoro-1-000-stanova/?utm_source=rss&utm_medium=rss&utm_campaign=novi-pazar-u-toku-izgradnja-skoro-1-000-stanova",
            "title": "Novi Pazar: U toku izgradnja skoro 1.000 stanova",
            "short_summary": "U poslednjih 17 meseci u Novom Pazaru je izdato 15 gra\u0111evinskih dozvola za izgradnju vi\u0161espratnica koje \u0107e ukupno imati 932 stana i 42 lokala, saznaje radio Sto plus. Odeljenje za urbanizam i izgradnju Gradske uprave pro\u0161le godine izdalo je ukupno 11 gra\u0111evinskih dozvola za izgradnju stambenih zgrada, a za prvih pet meseci ove jo\u0161 \u010detiri.",
            "views": 1065
        },
        {
            "domain": "sandzaklive.rs",
            "url": "https://sandzaklive.rs/popularno/branko-ruzic-i-saradnici-priredili-rodendansko-iznenadenje-elmi-elfic-zukorlic-video/",
            "title": "Branko Ru\u017ei\u0107 i saradnici priredili ro\u0111endansko iznena\u0111enje Elmi Elfi\u0107 Zukorli\u0107 (Video)",
            "short_summary": "Proslavila 42. rodjendan u Ministarstvu prosvete, nauke i tehnolo\u0161kog razvoja. Elma Elfi\u0107 Zukorli\u0107 na dru\u0161tvenim mre\u017eama je napisala : \u201cNeka se ove na\u0161e tanane niti prijateljstva, po\u0161tovanja i povjerenja nikada ne prekinu! Hvala vam od srca\u201d View this post on Instagram &#160; A post shared by Elma Elfi\u0107 Zukorli\u0107 (@elf_zu) Pogledajze video :",
            "views": 2659
        },
        {
            "domain": "sandzaklive.rs",
            "url": "https://sandzaklive.rs/novi-pazar/novipazar-drustvo/ovo-je-sandzak-grom-mu-ubio-kravu-anonimni-donator-kupio-kravu-sacirovicima/",
            "title": "Ovo je Sand\u017eak / Grom mu ubio kravu, anonimni donator kupio kravu \u0160a\u0107irovi\u0107ima",
            "short_summary": "Pre dva dana u selu Kominje grom je usmrtio kravu u doma\u0107instvu Senada \u0160a\u0107irovi\u0107a. Sino\u0107 ,nakon emitovanja priloga na na\u0161oj televiziji, javio se donator, koji je \u017eeleo da ostane anoniman i \u0160a\u0107irovi\u0107ima kupio\u00a0 kravu. Zahvaljuju\u0107i anonimnom donatoru, briga porodice \u0160a\u0107irovi\u0107 kako pre\u017eiveti bez krave i omogu\u0107iti normalnu egzistenciju za troje maloletne dece trajala je kratko. ..",
            "views": 1683
        },
        {
            "domain": "rtvnp.rs",
            "url": "https://rtvnp.rs/2022/06/08/anonimni-donator-kupio-kravu-sacirovicima/130538",
            "title": "Anonimni donator kupio kravu \u0160a\u0107irovi\u0107ima",
            "short_summary": "Pre dva dana u selu Kominje grom je usmrtio kravu u doma\u0107instvu Senada \u0160a\u0107irovi\u0107a. Sino\u0107 ,nakon emitovanja priloga na na\u0161oj televiziji, javio se donator, koji je \u017eeleo da ostane anoniman i \u0160a\u0107irovi\u0107ima kupio\u00a0 kravu.",
            "views": 713
        },
        {
            "domain": "rtvnp.rs",
            "url": "https://rtvnp.rs/2022/06/08/savremena-autobuska-stajalista-na-jos-nekoliko-lokacija/130526",
            "title": "Savremena autobuska stajali\u0161ta na jo\u0161 nekoliko lokacija",
            "short_summary": "Slu\u017ei\u0107e kao skloni\u0161ta od jakog sunca i ki\u0161e za one koji \u010dekaju autobuse, nekada mnogo du\u017ee od plana vo\u017enje, zbog velikih gu\u017evi u saobra\u0107aju.",
            "views": 226
        }
    ]

content = []
for k,v in groupby(data, lambda x: x['domain']):
	content.extend(sorted(v, key=itemgetter('views'), reverse=True)[:2])

print(datetime.today().isoformat())